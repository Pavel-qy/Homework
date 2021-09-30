# Task 7.9
#
# Implement an iterator class EvenRange, which accepts start 
# and end of the interval as an init arguments and gives 
# only even numbers during iteration. If user tries to 
# iterate after it gave all possible numbers Out of 
# numbers! should be printed.
# Note: Do not use function range() at all.

class EvenRange:
    def __init__(self, start_num, stop_num):
        if start_num % 2:
            self.start_num = start_num + 1
        elif not start_num % 2:
            self.start_num = start_num
        self.stop_num = stop_num

    def __iter__(self):
        return self

    def __next__(self):
        if self.start_num < self.stop_num:
            tmp = self.start_num
            self.start_num += 2
            return tmp
        else:
            print("Out of numbers!")
            raise StopIteration


er1 = EvenRange(7, 11)
print(next(er1))
print(next(er1))
# print(next(er1))
er2 = EvenRange(3, 14)
for number in er2:
    print(number)
