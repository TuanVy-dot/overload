import overload
from overload.obj import FuncNparam

@overload.overload_namespace
def add() -> list[FuncNparam]:
    @overload.overload_func((int, int))
    def addii(a, b):
        print(f"Adding integers {a + b=}")
    @overload.overload_func((int, float))
    def addif(a, b):
        print(f"Adding integer a and float b {a + b=}")
    @overload.overload_func((float, float))
    def addff(a, b):
        print(f"Adding floats {a + b=}")
    return [addii, addif, addff]

add(5, 7)
add(5.0, 2.0)
add(5.0, 9)
