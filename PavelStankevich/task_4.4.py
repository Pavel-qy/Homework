# Task 4.4
def split_by_index(string, indexes):
    '''Split the s string by indexes specified in indexes. Wrong indexes are ignored.'''
    indexes.sort()
    result, index_start = list(), 0

    while indexes and max(indexes) >= len(string):
        del indexes[-1]
    
    for index_end in indexes:
        result.append(string[index_start:index_end])
        index_start = index_end
    
    result.append(string[index_start:])
    return result

print(split_by_index("pythoniscool,isn'tit?", [26, 6, 8, 12, 13, 18, 32]))
print(split_by_index("no luck", [42]))
