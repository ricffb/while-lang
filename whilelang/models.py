from dataclasses import dataclass


@dataclass
class Program:
    pass


@dataclass
class Assign(Program):
    lvar: str
    rval: int


@dataclass
class _BinOp(Program):
    lvar: str
    rvar: str
    rval: int


@dataclass
class Add(_BinOp):
    pass


@dataclass
class Sub(_BinOp):
    pass


@dataclass
class While(Program):
    cond: str
    body: Program


@dataclass
class Seq(Program):
    p1: Program
    p2: Program