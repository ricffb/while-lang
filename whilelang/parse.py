from .models import Assign, Sub, Add, While, Seq, AssignSub
from parsy import regex, string, digit, generate, seq, eof  #type: ignore

whitespace = regex(r'[\s]*')
pad = regex(r'[^\S\r\n]')

Newline = regex(r"\n")
Next = (Newline.at_least(1)
        | eof).desc("at least one newline or the end of file")
Comment = string("#") >> (regex(r'[\S]') | pad).many().concat() >> Next

woc = whitespace << Comment.optional() << whitespace
lexeme = lambda p: p << woc

lbrac = lexeme(string("("))
rbrac = lexeme(string(")"))
comma = lexeme(string(","))

Eq = lexeme(string(":="))
Plus = lexeme(string("+"))
Minus = lexeme(string("-"))
KWhile = lexeme(string("WHILE")).desc("the keyword WHILE")
KAs = lexeme(string("AS")).desc("the keyword AS")
KDefine = lexeme(string("DEFINE")).desc("the keyword DEFINE")
KDo = lexeme(string("DO")).desc("the keyword DO")
KEnd = lexeme(string("END")).desc("the keyword END")
NoKeyWd = (
    KWhile | KDo | KAs | KDefine
    | KEnd).should_fail("not a reserved keyword that cannot be used as value")
KSeq = lexeme(string(";"))
Int = lexeme(digit.at_least(1).concat().map(int))
Var = lexeme(regex("[a-z][A-Za-z0-9_]*"))
Routine = NoKeyWd >> lexeme(regex("[A-Za-z_][A-Za-z0-9_]*"))

PAssignSub = seq(lvar=Var,
                 _eq=Eq,
                 routine=Routine,
                 _lbrac=lbrac,
                 arg1=Var,
                 _comma=comma,
                 arg2=Var,
                 _rbrac=rbrac).combine_dict(AssignSub)

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
    P1 = yield PWhile | PBinOp | PAssign | PAssignSub
    yield KSeq
    P2 = yield _Program | whitespace  #type: ignore

    return Seq(P1, P2)


@generate
def Subroutine():
    yield KDefine
    RName = yield Routine
    yield KAs
    P = yield _Program
    yield KEnd
    return (RName, P)


PSubroutineDef = woc >> Subroutine.many().map(dict)

_Program = PSeq | PWhile | PBinOp | PAssign | PAssignSub

PProgram = seq(PSubroutineDef, _Program)