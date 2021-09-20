# Task 4.7
from math import prod

def foobar(digits):
    '''Return a new list such that each element at index i of the new list 
    is the product of all the numbers in the original array except the one at i.'''
    return [int(prod(digits) / i) for i in digits]

print(foobar([1, 2, 3, 4, 5]))
print(foobar([3, 2, 1]))
