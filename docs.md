# PyOverload Documentation

For more questions or suggestions, contact via tuanvy860@gmail.com

## Table of contents:

### Getting started

`overload` is an easy to use Python function overload implementation if it is any useful for you. The most practical usage for it is to avoid 10000 isinstance check to know what argument combinations call which functions. All you have to do is use some decorators. Here is it in practice:

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

The output should look like:

```py
Adding integers a + b=12
Adding floats a + b=7.0
Traceback (most recent call last):
  File "", line 27, in <module>
    add(5.0, 9) # float, int (undefined)
    ^^^^^^^^^^^
  File "", line 38, in __call__
    raise UnmatchedError(f"Unmatched call to function signature {tuple(t.__name__ for t in (param_unmangle(mangled)))}")
overload.exceptions.UnmatchedError: Unmatched call to function signature ('float', 'int')
```

As you can see, it dispatched the function all correctly, and also a clear exception on what've gone wrong. And with that you should be able to use it.

### Details

Here are details about every piece of code within the source. You are exposed to `api.py` and `exceptions.py` only in `__init__.py`. But you can work around with it to access other pieces.

#### obj.py

This source contain objects definition, which are `FuncNparam` and `Overload`

##### FuncNparam

This class defines objects that contain the `function` object and its signature, that is the type combinations that will invoke it. For example `(int, int)` is a signature.

##### Overload

This class defines objects of the overloaded namespace, it is the main interface that you will interact with. Its constructor takes a list of `FuncNparam` and adds into its `children` dictionary, which is the container of all overload functions with the keys of mangled name.

It provides add and remove functions:
```py
add_func(self, func: FuncNparam) -> None
remove_func(self, param_t: tuple[type, ...]) -> None
```
You can add or remove functions using the signature

It also include the `__call__` method, which handles function dispatching and raise UnmatchedError exception.

#### name_mangling.py

Provides 3 functions:
```py
param_mangle(args: tuple[Any, ...]) -> str
param_mangle_t(args: tuple[type, ...]) -> str
param_unmangle(s: str) -> tuple[type, ...]
```

Where:

- `param_mangle_t` generate a unique string for a signature, it then used in hashing the functions in `Overload`. 

- `param_mangle` do the same thing, except for a tuple of arguments, it is used in `Overload` to match and dispatch.

- `param_unmangle` revert the process, generate the signature based on the string. Which it assume to be legit, so it might breaks if the string wasn't from mangle functions

#### api.py

The decorator API for overloading
```py
overload_namespace(func: Callable[[], list[FuncNparam]]) -> Overload
overload_func(param_t: tuple[type, ...]=())
```
- `overload_namespace` process the "namespace" function into an `Overload`, the namespace function must return a list of `FuncNparam` else an exception is raised.

- `overload_func` is a wrapper of another decorator, it takes tuple of types as argument and return a decorator that then be call to generate `FuncNparam`

#### exceptions.py

Just defines exceptions
