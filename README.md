# while-lang
A small Parser and Interpreter for the Educational WHILE - Programming Language by Uwe Schoening. 

# Syntax:

```
Program -> (Assign | Add | Sub | While) | Program ; Program
Assign -> Var := Integer
Add -> Var := Var + Integer
Sub -> Var := Var - Integer
While -> WHILE Var DO Program END
Var -> x0 | x1 | x2 | [a-z][A-Za-z0-9_]
```

# Example

Multiplies two numbers.
```
x0 := 0;
WHILE x1 DO
    ctr := x2 + 0;
    WHILE ctr DO
        x0 := x0 + 1;
        ctr := ctr - 1
    END;
    x1 := x1 - 1
END
```