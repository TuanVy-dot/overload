from typing_extensions import Callable

from overload.obj import FuncNparam, Overload


def overload_namespace(func: Callable[[], list[FuncNparam]]) -> Overload:
    funcs: list[FuncNparam] = func()
    if not isinstance(funcs, list):
        raise TypeError("Overload: Expected the overload function to return\
                        a list of type FuncNparam")
    return Overload(funcs)

def overload_func(param_t: tuple[type, ...]):
    def decorator(func: Callable):
        return FuncNparam(func, param_t)
    return decorator
