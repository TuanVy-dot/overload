import overload

@overload.overload_namespace
def add():

    @overload.overload_func((int, int))
    def f1(a, b):
        print("Adding integers")
        return a + b

    @overload.overload_func((float, float))
    def f2(a, b):
        print("Adding floats")
        return a + b

    return [f1, f2]

print(add(2, 3))
print(add(2.0, 3.0))
try:
    print(add(2, 3.0))
except overload.exceptions.UnmatchedError as e:
    print(e)
