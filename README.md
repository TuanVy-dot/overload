A simple (really simple) function overloading implementation for python

Errors may still exist. Only supports positional arguments (for now)

Usage:

```py
# Import the overload module (clone the repo and build using setup.py)
import overload
# Define a namespace using the namespace decorator
@overload.overload_namespace
def add():
    # define functions using the overload_func decorator
    # Along with the types signature (make sure it matches)
    @overload.overload_func((int, int))
    def addii(a, b):
        print(f"Adding integers {a + b=}")

    # Repeat
    @overload.overload_func((int, float))
    def addif(a, b):
        print(f"Adding integer a and float b {a + b=}")
    @overload.overload_func((float, float))
    def addff(a, b):
        print(f"Adding floats {a + b=}")

    # Return a list of overload_func decorated functions
    return [addii, addif, addff]

# Call them
add(5, 7) # int, int
add(5.0, 2.0) # int, float
add(5.0, 9) # float, int (undefined)
```

The output should be something like

```py
Adding integers a + b=12
Adding floats a + b=7.0
Traceback (most recent call last):
  File "path/to/src", line 19, in <module>
    add(5.0, 9)
  File "path/to/mod", line 38, in __call__
    raise UnmatchedError(f"Unmatched call to function {mangled}")
overload.exceptions.UnmatchedError: Unmatched call to function C2CPL5LfloatPPL3LintP
```

Simple as that

## Installation:

Use setup.py (tutorial all over the internet), it may or may not in PYPI already

(Depends on how lazy I am)
