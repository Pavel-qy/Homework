# Task 4.9
from string import ascii_lowercase
from functools import reduce

def test_1_1(*strings):
    '''Return characters that appear in all strings.'''
    return reduce(lambda x, y: set(x) & set(y), strings)

def test_1_2(*strings):
    '''Return characters that appear in at least one string.'''
    return reduce(lambda x, y: set(x) | set(y), strings)

def test_1_3(*strings):
    '''Return characters that appear at least in two strings.'''
    strings = list(map(set, strings))
    result = set()

    for i in range(len(strings) - 1):
        for j in range(i + 1, len(strings)):
            result |= set(strings[i]) & set(strings[j])
    
    return result

def test_1_4(*strings):
    '''Return characters of alphabet, that were not used in any string.'''
    return reduce(lambda x, y: set(x) - set(y), strings, ascii_lowercase)

print(test_1_1("hello", "world", "python", ))
print(test_1_2("hello", "world", "python", ))
print(test_1_3("hello", "world", "python", ))
print(test_1_4("hello", "world", "python", ))
