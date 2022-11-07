class MyClass:
    class Shit:
        pass

    def __init__(self):
        self.Shit = self.Shit()
        pass


my_class = MyClass()

print(vars(my_class))
for i in vars(my_class):
    print(i)