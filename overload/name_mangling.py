from typing import Any


def param_mangle(args: tuple[Any, ...]) -> str:
    # The first C C enclose the parameters count
    # P P enclose a single parameter
    # The L L enclose parameter name length
    # PL9LninecharlP for example
    name: str = f"C{len(args)}C"
    for arg in args:
        name += f"PL{len(type(arg).__name__)}L{type(arg).__name__}P"
    return name

def param_mangle_t(types: tuple[type, ...]) -> str:
    # The first C C enclose the parameters count
    # P P enclose a single parameter
    # The L L enclose parameter name length
    # PL9LninecharlP for example
    name: str = f"C{len(types)}C"
    for t in types:
        name += f"PL{len(t.__name__)}L{t.__name__}P"
    return name
