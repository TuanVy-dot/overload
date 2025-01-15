from typing_extensions import Callable
from overload.exceptions import UnmatchedError
from overload.name_mangling import param_mangle, param_mangle_t

class FuncNparam:
    def __init__(self, func: Callable, param_t: tuple[type, ...]) -> None:
        if not callable(func):
            raise TypeError(f"Overload: {func} is not a callable")
        for p in param_t:
            if not isinstance(p, type):
                raise TypeError(f"Overload: Expected type objects in param")
        self.func: Callable = func
        self.param_t: tuple[type, ...] = param_t

class Overload:
    def __init__(self, funcs: list[FuncNparam]) -> None:
        self.children: dict[str, Callable] = {}
        for func in funcs:
            if not isinstance(func, FuncNparam):
                raise TypeError(f"Overload: Expected FuncNParam type")
            self.children[param_mangle_t(func.param_t)] = func.func

    def add_func(self, func: FuncNparam) -> None:
        self.children[param_mangle_t(func.param_t)] = func.func

    def remove_func(self, param_t: tuple[type]) -> None:
        for p in param_t:
            if not isinstance(p, type):
                raise TypeError(f"Overload: Expected type objects in param")
        self.children.pop(param_mangle_t(param_t))

    def __call__(self, *args):
        mangled = param_mangle(args)
        f = self.children.get(mangled, None)
        if not f:
            raise UnmatchedError(f"Unmatched call to function {mangled}")
        return f(*args)
