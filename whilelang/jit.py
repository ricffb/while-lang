from .parse import PProgram, parse_while
from .models import Program, Assign, Add, Seq, Sub, While, AssignSub
from llvmlite import ir  #type: ignore
from ctypes import CFUNCTYPE, c_int64
import llvmlite.binding as llvm  #type: ignore
from typing import Dict, Any, Tuple

# All these initializations are required for code generation!
llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()  # yes, even this one

int64 = ir.IntType(64)
zero = ir.Constant(int64, 0)


def create_execution_engine():
    """
    Create an ExecutionEngine suitable for JIT code generation on
    the host CPU.  The engine is reusable for an arbitrary number of
    modules.
    """
    # Create a target machine representing the host
    target = llvm.Target.from_default_triple()
    target_machine = target.create_target_machine()
    # And an execution engine with an empty backing module
    backing_mod = llvm.parse_assembly("")
    engine = llvm.create_mcjit_compiler(backing_mod, target_machine)
    return engine


defaultengine = create_execution_engine()


def build_ir(p, var, builder: ir.IRBuilder, subroutines: Dict[str, Any]):
    if not p:
        return var, builder

    if isinstance(p, Assign):

        try:
            ptr = var[p.lvar]
        except KeyError:
            ptr = builder.alloca(int64, name=p.lvar)
            var[p.lvar] = ptr

        builder.store(ir.Constant(int64, p.rval), ptr)

        return var, builder
    if isinstance(p, AssignSub):

        try:
            lvar = var[p.lvar]
        except KeyError:
            lvar = builder.alloca(int64, name=p.lvar)
            var[p.lvar] = lvar

        x1 = builder.load(var[p.arg1])
        x2 = builder.load(var[p.arg2])

        res = builder.call(subroutines[p.routine], (x1, x2))
        builder.store(res, lvar)
        return var, builder

    if isinstance(p, Add):
        try:
            lvar = var[p.lvar]
        except KeyError:
            lvar = builder.alloca(int64, name=p.lvar)
            var[p.lvar] = lvar

        irVar = builder.load(var[p.rvar])
        rhs = ir.Constant(int64, p.rval)
        res = builder.add(irVar, rhs)
        builder.store(res, lvar)
        return var, builder
    if isinstance(p, Sub):
        try:
            lvar = var[p.lvar]
        except KeyError:
            lvar = builder.alloca(int64, name=p.lvar)
            var[p.lvar] = lvar

        irVar = builder.load(var[p.rvar])
        rhs = ir.Constant(int64, p.rval)
        sval = builder.sub(irVar, rhs)
        cmp = builder.icmp_signed("<", sval, zero)
        res = builder.select(cmp, zero, sval)
        builder.store(res, lvar)
        return var, builder
    if isinstance(p, Seq):
        var, builder = build_ir(p.p1, var, builder, subroutines)
        return build_ir(p.p2, var, builder, subroutines)
    if isinstance(p, While):
        ptr = var[p.cond]

        if len(builder.block.instructions):
            while_cmp = builder.append_basic_block()
            builder.branch(while_cmp)
        else:
            while_cmp = builder.block
        while_block = builder.append_basic_block()
        after = builder.append_basic_block()

        with builder.goto_block(while_cmp):
            sval = builder.load(ptr)
            cmp = builder.icmp_signed("==", sval, zero)
            builder.cbranch(cmp, after, while_block)
        with builder.goto_block(while_block):
            var, newbuilder = build_ir(p.body, var, builder, subroutines)
            newbuilder.branch(while_cmp)
        return var, ir.IRBuilder(after)


def declare_while_routine(module, name):
    whileProgTy = ir.FunctionType(int64, (int64, int64))
    func = ir.Function(module, whileProgTy, name=name)
    return func


def build_while_routine(prog, func, subr):

    block = func.append_basic_block(name="entry")
    builder = ir.IRBuilder(block)
    in_x1, in_x2 = func.args

    x0 = builder.alloca(int64, name="x0")
    x1 = builder.alloca(int64, name="x1")
    x2 = builder.alloca(int64, name="x2")

    builder.store(zero, x0)
    builder.store(in_x1, x1)
    builder.store(in_x2, x2)

    var = {"x0": x0, "x1": x1, "x2": x2}

    var, builder = build_ir(prog, var, builder, subr)

    builder.ret(builder.load(var["x0"]))
    return func


def emit_ir(prog: Program, subroutines: Dict[str, Program] = None):
    subroutines = {} if subroutines is None else subroutines

    module = ir.Module(name="while_main")

    decl_subr = {
        name: declare_while_routine(module, name)
        for name in subroutines.keys()
    }

    for name, func in decl_subr.items():
        build_while_routine(subroutines[name], func, decl_subr)

    main = declare_while_routine(module, "while_main")
    build_while_routine(prog, main, decl_subr)

    return module


def optimize_ir(module, opt_level=3):
    pm = llvm.PassManagerBuilder()
    pm.opt_level = opt_level
    pm.disable_unroll_loops = True
    pm.size_level = 0
    pm.inlining_threshold = 50
    mpm = llvm.ModulePassManager()
    pm.populate(mpm)
    mod = llvm.parse_assembly(str(module))
    mpm.run(mod)

    return mod


def compile_module(mod, engine=defaultengine):
    mod.verify()
    # Now add the module and make sure it is ready for execution
    engine.add_module(mod)
    engine.finalize_object()
    engine.run_static_constructors()
    return mod


def get_main_func(prog: Tuple[Dict[str, Program], Program],
                  engine=defaultengine):
    mod_ir = emit_ir(prog[1], dict(prog[0]))
    mod = optimize_ir(mod_ir, opt_level=3)
    # engine = create_execution_engine()
    cmp = compile_module(mod, engine)

    # Look up the function pointer (a Python int)
    func_ptr = engine.get_function_address("while_main")
    # Run the function via ctypes
    cfunc = CFUNCTYPE(c_int64, c_int64, c_int64)(func_ptr)
    return cfunc


def compile_while_prog(program, engine=defaultengine):
    P = parse_while(program)
    return get_main_func(P, engine)


def run_jit(program, x1=0, x2=0):
    return compile_while_prog(program)(x1, x2)