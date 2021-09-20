# Task 4.3
def func_split(string, separator=" "):
    '''A function which works the same as str.split method.'''
    result, i = list(), 0
    if separator == " ":
        string = string.lstrip()
        
    while separator in string:
        result.append(string[:string.find(separator)])
        string = string.replace(result[i] + separator, "", 1)
        if separator == " ":
            string = string.lstrip()
        i += 1
    
    result.append(string)
    return result

print(func_split(",A man, a plan, a canal – Panama", ","))
print(",A man, a plan, a canal – Panama".split(","))
print(func_split("  A  man,  a  plan,  a   canal –  Panama"))
print("  A  man,  a  plan,  a   canal –  Panama".split())
