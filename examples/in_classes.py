import overload

class Arithmetics:
    def __init__(self):
        self.result = 0

    @overload.overload_method
    def add(self):
        
        @overload.overload_func((int, int))
        def addii(self, a, b):
            print(f"Adding int: {a + b=}")
            self.result = a + b
        @overload.overload_func((float, float))
        def addff(self, a, b):
            print(f"Adding floats: {a + b=}")
            self.result = a + b

        return [addii, addff]

arthm = Arithmetics()

arthm.add(2, 3)
print(arthm.result)
arthm.add(2.0, 3.0)
print(arthm.result)
