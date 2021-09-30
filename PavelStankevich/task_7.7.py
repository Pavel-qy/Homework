# Task 7.7
#
# Implement your custom collection called MyNumberCollection. 
# It should be able to contain only numbers. It should NOT 
# inherit any other collections. If user tries to add a 
# string or any non numerical object there, exception 
# TypeError should be raised. Method init sholud be 
# able to take either start,end,step arguments, where 
# start - first number of collection, end - last number 
# of collection or some ordered iterable collection 
# (see the example). Implement following functionality:
#
#    * appending new element to the end of collection
#    * concatenating collections together using +
#    * when element is addressed by index(using []), 
#         user should get square of the addressed element.
#    * when iterated using cycle for, elements should be given normally
#    * user should be able to print whole collection as if it was list.

class MyNumberCollection:
    def __init__(self, *args):
        self.list_of_numbers = self.sequencing(*args)

    def __str__(self):
        return f"{self.list_of_numbers}"

    def __add__(self, other):
        return self.list_of_numbers + other.list_of_numbers

    def __getitem__(self, key):
        return self.list_of_numbers[key]**2

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self.list_of_numbers):
            tmp = self.index
            self.index += 1
            return self.list_of_numbers[tmp]
        else:
            raise StopIteration

    def append(self, value):
        if not isinstance(value, int):
            raise TypeError(f"'{value}' – object is not a number!")
        return self.list_of_numbers.append(value)

    def sequencing(self, *args):
        if len(args) == 1 and isinstance(args[0], tuple):
            self.values_validation(args[0])
            return list(args[0])
        elif len(args) == 1 and self.values_validation(args):
            return [i for i in range(args[0] + 1)]
        elif len(args) == 2 and self.values_validation(args):
            return [i for i in range(args[0], args[1] + 1)]
        elif len(args) == 3 and self.values_validation(args):
            list_of_numbers = [i for i in range(args[0], args[1] + 1, args[2])]
            if list_of_numbers[-1] != args[1]:
                list_of_numbers.append(args[1])
            return list_of_numbers

    def values_validation(self, values):
        self.values = values
        for value in self.values:
            if not isinstance(value, int):
                raise TypeError("MyNumberCollection supports only numbers!")
        return True


col1 = MyNumberCollection(0, 5, 2)
print(col1)
col2 = MyNumberCollection((1,2,3,4,5))
print(col2)
# col3 = MyNumberCollection((1,2,3,"4",5))
col1.append(7)
print(col1)
# col2.append("string")
print(col1 + col2)
print(col1)
print(col2)
print(col2[4])
for item in col1:
    print(item)