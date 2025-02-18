# PyOverload Documentation

For any questions or suggestions, please contact us at tuanvy860@gmail.com.

## Table of Contents:

1. [Getting Started](#getting-started)

2. [Details](#details)

- [obj.py](#objpy)

    - [FuncNparam](#funcnparam)

    - [Overload](#overload)


- [name_mangling.py](#name_manglingpy)

- [api.py](#apipy)

- [exceptions.py](#exceptionspy)

3. [Classes](#classes)

Why markdown? Well I'm just too lazy for something better, and markdown is good! The code is fairly simple and this should be sufficient. No docstring in source by the way, I'm sorry.

### Getting Started

overload is an easy-to-use Python function overloading implementation that can help streamline function dispatching based on argument types. This can be particularly useful when you need to avoid writing numerous isinstance checks to determine which function to call based on the argument types. All you need to do is apply a few decorators. Here's a practical example:

```py
# Import the overload module (clone the repo and build using setup.py)
import overload

# Define a namespace using the overload_namespace decorator
@overload.overload_namespace
def add():
    # Define overloaded functions using the overload_func decorator
    # Ensure the function signatures match the provided types
    @overload.overload_func((int, int))
    def addii(a, b):
        print(f"Adding integers: {a + b}")

    # Overload for integer and float
    @overload.overload_func((int, float))
    def addif(a, b):
        print(f"Adding integer and float: {a + b}")

    # Overload for floats
    @overload.overload_func((float, float))
    def addff(a, b):
        print(f"Adding floats: {a + b}")

    # Return a list of overloaded functions
    return [addii, addif, addff]

# Call the functions with different types
add(5, 7)      # int, int
add(5.0, 2.0)  # float, float
add(5.0, 9)    # float, int (undefined)
```

The output will be:

```py
Adding integers: a + b = 12
Adding floats: a + b = 7.0
Traceback (most recent call last):
  File "", line 27, in <module>
    add(5.0, 9)  # float, int (undefined)
    ^^^^^^^^^^^
  File "", line 38, in __call__
    raise UnmatchedError(f"Unmatched call to function signature {tuple(t.__name__ for t in (param_unmangle(mangled)))}")
overload.exceptions.UnmatchedError: Unmatched call to function signature ('float', 'int')
```

As demonstrated, the library correctly dispatches the functions and raises a clear exception when no matching function is found. You can now use overload for clean and efficient function overloading.

Keyword arguments are not part of the signature, and everything passed in the namespace will be passed in the matched function, meaning some workaround can be done, you can add kw arguments by adding them in the function argument without them being in the signature.

### Details

Below are the key components within the source code, when you import overload, you only exposed to `api.py` and `exceptions.py`. You can also extend your usage by do some workaround.

#### obj.py

This file contains the definitions of the objects FuncNparam and Overload.

##### FuncNparam

The `FuncNparam` class encapsulates a function and its signature, which is a tuple of types that the function will handle. For example, the signature `(int, int)` represents a function that expects two integers.

##### Overload

The `Overload` class represents an overloaded namespace. It stores a collection of FuncNparam objects in its `children` dictionary, where the keys are the mangled function names.

The Overload class also includes the `__call__` method, which handles function dispatch and raises an UnmatchedError if no matching function is found.

1.2.0: The `__getitem__` or random access `[]` method is added, you can say
```py
add[(int, int)](1.0, 2.0)
```
to call the add function with signature `(int, int)` for floats. This however is discourage, wrong types usage can cause big errors.

#### name_mangling.py

This module provides three functions for mangling and unmangling function signatures:

```py
param_mangle(args: tuple[Any, ...]) -> str
param_mangle_t(args: tuple[type, ...]) -> str
param_unmangle(s: str) -> tuple[type, ...]
```

- `param_mangle_t` generates a unique string based on a function signature (tuple of types) and is used for hashing functions in `Overload`.

- `param_mangle` works similarly but processes argument values, used for dispatch matching in `Overload`.

- `param_unmangle` reverses the mangling process to retrieve the original function signature from a mangled string. This method assumes the string is valid, so using an incorrect string may result in errors.


#### api.py

This module defines the decorator API for overloading functions:

```py
overload_namespace(func: Callable[[], list[FuncNparam]]) -> Overload
overload_func(param_t: tuple[type, ...]=())
overload_method(func: Callable[[Any], list[FuncNparam]]) -> cached_property
```

- `overload_namespace` transforms a "namespace" function into an `Overload` object. The namespace function must return a list of `FuncNparam` objects; otherwise, an exception will be raised.

- `overload_func` is a decorator that takes a tuple of types and returns a decorator to create `FuncNparam` objects for function overloading.

- `overload_method` is analogous to `overload_namespace` but for methods, it uses a smart workaround to bounds the self to Overload, because we are not able to bind self to the method using just simple logic as in `overload_namespace`, `cached_property` and a `getter` is used, and it might be slower. For more infomation for in classes usage, see [Classes](#classes).

#### exceptions.py

This module defines custom exceptions used in the library.


### Classes

Methods overloading was added in 2.0.0. Providing `overload_method` decorator and is analogous to `overload_namespace`, see [overload_method](#apipy) for some more details.

Example in `examples/in_classes.py`.

To use overloading for methods, use `overload_method` to decorate the top level, then decorate other implementations using `overload_func` the same way as in any functions. Do not forget self as the first argument but do not put it in the signature. You would learn best from examples:

```py
@overload_func((int, int))
def func(self, a, b):
    return a + b
```

As demonstrated, the function take an additional argument self, but the signature only includes `(int, int)`.

---
