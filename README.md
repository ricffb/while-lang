# while-lang
A small Parser and Interpreter for the Educational WHILE - Programming Language by Uwe Schoening. 

# Syntax:
```
File -> {SubroutineDef} Program 

SubroutineDef -> DEFINE RoutineName AS Program END

Program -> (Assign | AssignSub | Add | Sub | While) | Program ; Program
Assign -> Var := Integer
Add -> Var := Var + Integer
Sub -> Var := Var - Integer
While -> WHILE Var DO Program END
AssignSub -> RoutineName ( Var , Var )

RoutineName ->  [A-Za-z_][A-Za-z0-9_]*
Var -> x0 | x1 | x2 | [a-z][A-Za-z0-9_]*
```
Comments can be made using `#`.


# Example

Multiplies two numbers with subroutines.
```
# Define a Subroutine
DEFINE M AS
x0 := x1 - 1
END

# Calculate x1 times x2
x0 := 0;
WHILE x1 DO
    ctr := x2 + 0;
    WHILE ctr DO
     x0 := x0 + 1;
     ctr := M(ctr,ctr) # decrement the counter
    END;
    x1 := M(x1,x1)
END
```
Take a look at the `examples` folder for more examples. 