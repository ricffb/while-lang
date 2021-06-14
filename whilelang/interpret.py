from .parse import PProgram
from .models import Program, Assign, Seq, Add, Sub, While
from collections import defaultdict
from typing import DefaultDict


def _interpret(p: Program, var: DefaultDict[str, int]):
    if isinstance(p, Assign):
        var[p.lvar] = p.rval
        return var
    if isinstance(p, Add):
        var[p.lvar] = var[p.rvar] + p.rval
        return var
    if isinstance(p, Sub):
        var[p.lvar] = var[p.rvar] - p.rval
        return var
    if isinstance(p, Seq):
        var = _interpret(p.p1, var)
        return _interpret(p.p2, var)
    if isinstance(p, While):
        while var[p.cond] != 0:
            var = _interpret(p.body, var)
        return var


def interpret(p: Program, x1=0, x2=0):
    var = defaultdict(lambda: 0, {"x0": 0, "x1": x1, "x2": x2})
    return _interpret(p, var)


def run(program, x1=0, x2=0):
    if hasattr(program, "read"):
        P = PProgram.parse(program.read())
    else:
        P = PProgram.parse(program)

    return interpret(P, x1, x2)