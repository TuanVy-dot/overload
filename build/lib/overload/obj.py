from typing_extensions import Callable
from .exceptions import UnmatchedError
from .name_mangling import param_mangle_t, param_unmangle, param_mangle

class FuncNparam:
    def __init__(self, func: Callable, param_t: tuple[type, ...]) -> None:
        if not callable(func):
            raise TypeError(f"Overload: {func} is not a callable")
        if not isinstance(param_t, tuple):
            raise TypeError(f"Overload: Expected tuple[type, ...]")
        for p in param_t:
            if not isinstance(p, type):
                raise TypeError(f"Overload: Expected type objects in param")
        self.func: Callable = func
        self.param_t: tuple[type, ...] = param_t

class Overload:
    def __init__(self, name: str, funcs: list[FuncNparam]) -> None:
        self.children: dict[str, Callable] = {}
        for func in funcs:
            if not isinstance(func, FuncNparam):
                raise TypeError(f"Overload: Expected FuncNParam type")
            self.children[param_mangle_t(func.param_t)] = func.func
        self.__name = name;

    def __call__(self, *args, **kwargs):
        mangled = param_mangle(args)
        f = self.children.get(mangled, None)
        if not f:
            raise UnmatchedError(f"Unmatched call to function \'{self.__name}\' with signature {tuple(t.__name__ for t in (param_unmangle(mangled)))}")
        return f(*args, **kwargs)

    def __getitem__(self, signature: tuple[type, ...]):
        if not isinstance(signature, tuple):
            raise TypeError("Overload: expected tuple of types")
        for t in signature:
            if not isinstance(t, type):
                raise TypeError("Overload: expected tuple of types")
        mangled = param_mangle_t(signature)
        f = self.children.get(mangled, None)
        if not f:
            raise UnmatchedError(f"Unmatched access to function \'{self.__name}\' with signature {tuple(t.__name__ for t in (param_unmangle(mangled)))}")
        return f
