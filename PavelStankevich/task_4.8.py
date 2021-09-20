# Task 4.8
def get_pairs(lst):
    '''Return a list of tuples containing pairs of elements.
    If there is only one element in the list return None instead. '''
    result = list()

    for i in range(len(lst) - 1):
        result.append(tuple(lst[i:i + 2]))
    
    return result if result else None

print(get_pairs([1, 2, 3, 8, 9]))
print(get_pairs(['need', 'to', 'sleep', 'more']))
print(get_pairs([1]))
