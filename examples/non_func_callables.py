import overload

class SumCallable:
    def __init__(self):
        pass
    def __call__(self, a, b):
        return a + b
class DiffCallable:
    def __init__(self):
        pass
    def __call__(self, a, b):
        return a - b

@overload.overload_namespace
def func():

    # (int, int) call sum
    # (float, float) call difference
    return [
        overload.overload_func((int, int))(SumCallable()),
        overload.overload_func((float, float))(DiffCallable())
    ]

print(func(5, 6))
print(func(5.0, 6.0))
