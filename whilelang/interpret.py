from .parse import PProgram
from .models import Program, Assign, Seq, Add, Sub, While, AssignSub
from collections import defaultdict
from typing import DefaultDict, Dict


def _interpret(p: Program, var: DefaultDict[str, int],
               subroutines: Dict[str, Program]):
    if isinstance(p, Assign):
        var[p.lvar] = p.rval
        return var
    if isinstance(p, AssignSub):
        subr = subroutines[p.routine]
        a1 = var[p.arg1]
        a2 = var[p.arg2]
        var[p.lvar] = interpret(subr, a1, a2, subroutines)["x0"]
        return var
    if isinstance(p, Add):
        var[p.lvar] = var[p.rvar] + p.rval
        return var
    if isinstance(p, Sub):
        var[p.lvar] = max(0, var[p.rvar] - p.rval)
        return var
    if isinstance(p, Seq):
        var = _interpret(p.p1, var, subroutines)
        return _interpret(p.p2, var, subroutines)
    if isinstance(p, While):
        while var[p.cond] != 0:
            var = _interpret(p.body, var, subroutines)
        return var
    return var


def interpret(p: Program, x1=0, x2=0, subroutines: Dict[str, Program] = None):
    var = defaultdict(lambda: 0, {"x0": 0, "x1": x1, "x2": x2})
    subroutines = subroutines or {}
    return _interpret(p, var, subroutines)


def run(program, x1=0, x2=0):
    if hasattr(program, "read"):
        Subs, P = PProgram.parse(program.read())
    else:
        Subs, P = PProgram.parse(program)

    return interpret(P, x1, x2, Subs)