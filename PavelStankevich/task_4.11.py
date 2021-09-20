# Task 4.11
def combine_dicts(*dicts):
    '''Receive changeable number of dictionaries (keys - letters, values - numbers) 
    and combines them into one dictionary.
    Dictionary values are summed in case of identical keys.'''
    result = dict()

    for dct in dicts:
        for key, value in dct.items():
            if key in result:
                result[key] += value
            else:
                result[key] = value
    
    return result

dict_1 = {'a': 100, 'b': 200}
dict_2 = {'a': 200, 'c': 300}
dict_3 = {'a': 300, 'd': 100}
print(combine_dicts(dict_1, dict_2))
print(combine_dicts(dict_1, dict_2, dict_3))
