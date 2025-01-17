import overload

@overload.overload_namespace
def add():

    @overload.overload_func((int, int))
    def f1(a, b, sub=False):
        if sub:
            print("Subtracting integers")
            b = -b
        else:
            print("Adding integers")
        return a + b

    @overload.overload_func((float, float))
    def f2(a, b, sub=False):
        if sub:
            print("Subtracting floats")
            b = -b
        else:
            print("Adding floats")
        return a + b

    return [f1, f2]

# Keywords arguments are keywords only, and not in signature
print(add(2, 3))
print(add(2.0, 3.0))
print(add(2, 3, sub=True))
print(add(2.0, 3.0, sub=True))
