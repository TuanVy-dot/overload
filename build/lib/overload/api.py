from typing_extensions import Any, Callable
from functools import cached_property

from .obj import FuncNparam, Overload


def overload_namespace(func: Callable[[], list[FuncNparam]]) -> Overload:
    funcs: list[FuncNparam] = func()
    if not isinstance(funcs, list):
        raise TypeError("Overload: Expected the overload function to return\
                        a list of type FuncNparam")
    return Overload(funcs)

def overload_func(param_t: tuple[type, ...]=()):
    def decorator(func: Callable):
        return FuncNparam(func, param_t)
    return decorator

def overload_method(func: Callable[[Any], list[FuncNparam]]) -> cached_property:
    def getter(self):
        funcs: list[FuncNparam] = func(self)
        if not isinstance(funcs, list):
            raise TypeError("Overload: Expected the overload function to return a list of type FuncNparam")
        
        # Bind the functions to the instance
        bound_funcs = []
        for f in funcs:
            def create_bound_method(f):
                def bound_method(*args, **kwargs):
                    return f.func(self, *args, **kwargs)
                return bound_method
            bound_funcs.append(FuncNparam(create_bound_method(f), f.param_t))
            
        return Overload(bound_funcs)
    
    return cached_property(getter)
