from dataclasses import dataclass


@dataclass(frozen=True)
class Program:
    pass


@dataclass(frozen=True)
class Assign(Program):
    lvar: str
    rval: int


@dataclass(frozen=True)
class AssignSub(Program):
    lvar: str
    routine: str
    arg1: str
    arg2: str


@dataclass(frozen=True)
class _BinOp(Program):
    lvar: str
    rvar: str
    rval: int


@dataclass(frozen=True)
class Add(_BinOp):
    pass


@dataclass(frozen=True)
class Sub(_BinOp):
    pass


@dataclass(frozen=True)
class While(Program):
    cond: str
    body: Program


@dataclass(frozen=True)
class Seq(Program):
    p1: Program
    p2: Program