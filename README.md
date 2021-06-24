# while-lang
A small Parser and Interpreter for the Educational WHILE - Programming Language by Uwe Schoening. 
# Installation
Install the latest Version with pip
```
pip install while-lang
```

# Using the CLI

After a successful installation you can use the `whilelang` script.
```
whilelang pathto/prog.while 1 2
```
where `1` and `2` are the inputs for `x1` and `x2` respectively.

Use `-h` for help.

```
usage: whilelang [-h] [-p] [-i] file [x1] [x2]

WHILE lang interpreter.

positional arguments:
  file              The File containing the Program
  x1                First argument.
  x2                Second argument.

optional arguments:
  -h, --help        show this help message and exit
  -p, --parse-only  Only parse the file without running. Useful for testing if the file format is correct.
  -i                Run in interpret mode. (Don't JIT Compile the While Code)
```

# Syntax:
```
File -> [SubroutineDef]* Program 

SubroutineDef -> DEFINE RoutineName AS Program END

Program -> (Assign | AssignSub | Add | Sub | While) | Program ; Program
Assign -> Var := Integer
Add -> Var := Var + Integer
Sub -> Var := Var - Integer
While -> WHILE Var DO Program END
AssignSub -> Var := RoutineName ( Var , Var )

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
