from .models import Assign, Sub, Add, While, Seq
from parsy import regex, string, digit, generate, seq, eof  #type: ignore

whitespace = regex(r'[\s]*')
lexeme = lambda p: p << whitespace

Eq = lexeme(string(":="))
Plus = lexeme(string("+"))
Minus = lexeme(string("-"))
KWhile = lexeme(string("WHILE"))
KDo = lexeme(string("DO"))
KEnd = lexeme(string("END"))
KSeq = lexeme(string(";"))
Int = lexeme(digit.many().concat().map(int))
Var = lexeme(regex("[a-z][A-Za-z0-9_]*"))

PAssign = seq(lvar=Var, _eq=Eq, rval=Int).combine_dict(Assign)


def mapBinOp(lvar, rvar, rval, op):
    if op == "+":
        return Add(lvar=lvar, rvar=rvar, rval=rval)
    else:
        return Sub(lvar=lvar, rvar=rvar, rval=rval)


PBinOp = (seq(lvar=Var, _eq=Eq, rvar=Var, op=(Minus | Plus),
              rval=Int)).combine_dict(mapBinOp)
#PSub = seq(lvar=Var, _eq=Eq, rvar=Var, _minus=Minus, rval=Int).combine_dict(Sub)


@generate
def PWhile():
    yield KWhile
    cond = yield Var
    yield KDo
    P = yield _Program
    yield KEnd
    return While(cond=cond, body=P)


@generate
def PSeq():
    P1 = yield PWhile | PBinOp | PAssign
    yield KSeq
    P2 = yield _Program | whitespace >> eof

    return Seq(P1, P2)


_Program = PSeq | PWhile | PBinOp | PAssign
PProgram = whitespace >> _Program