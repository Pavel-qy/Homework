# Task.= 7.8
#
# Implement your custom iterator class called MySquareIterator 
# which gives squares of elements of collection it iterates 
# through.

class MySquareIterator:
    def __init__(self, lst):
        self.lst = lst

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        try:
            res = self.index
            self.index += 1
            return self.lst[res]**2
        except IndexError:
            raise StopIteration
        

lst = [1, 2, 3, 4, 5]
itr = MySquareIterator(lst)
for item in itr:
    print(item)
