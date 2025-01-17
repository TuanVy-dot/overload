from typing import Any
import pydoc


def param_mangle(args: tuple[Any, ...]) -> str:
    # The first C C enclose the parameters count
    # P P enclose a single parameter
    # The L L enclose parameter name length
    # PL9LninecharlP for example
    name: str = f"C{len(args)}C"
    for arg in args:
        name += f"PL{len(type(arg).__name__)}L{type(arg).__name__}P"
    return name

def param_mangle_t(args: tuple[type, ...]) -> str:
    # The first C C enclose the parameters count
    # P P enclose a single parameter
    # The L L enclose parameter name length
    # PL9LninecharlP for example
    name: str = f"C{len(args)}C"
    for t in args:
        name += f"PL{len(t.__name__)}L{t.__name__}P"
    return name

def param_unmangle(s: str) -> tuple[type, ...]:
    args: list[type] = list()
    kwargs: list[tuple[str, type]] = list()

    # current index in s
    i: int = 0

    slen: int = len(s)

    # skip parameters count (not needed)
    while i < slen:
        # skip the first C (assume legit string)
        i += 1
        if s[i] == "C":
            # skip the C
            i += 1
            break

    while i < slen:
        tlen: int = 0
        tlens: str = ""
        i += 2 # skip first P and L
        while i < slen:
            if s[i] == "L":
                i += 1
                break
            tlens += s[i]
            i += 1
        tlen = int(tlens)
        typename: str = ""
        for j in range(tlen):
            typename += s[i]
            i += 1
        t = pydoc.locate(typename)
        if not t or not isinstance(t, type):
            raise ValueError(f"Overload: No such type {t}")
        
        args.append(t)

        i += 1
    
    return tuple(args)
