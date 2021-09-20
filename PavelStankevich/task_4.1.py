# Task 4.1
def quotes_inverter(string):
    '''Return a string and replaces all " characters with ' and vice versa.'''
    return string.replace("'", "*").replace("\"", "'").replace("*", "\"")

print(quotes_inverter("Single quotes – \", \", \". Double quotes – ', ', '."))
