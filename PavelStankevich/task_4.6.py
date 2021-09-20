# Task 4.6
def get_longest_word(string):
    '''Return the longest word in the given string.'''
    return max(string.split(), key=len)

print(get_longest_word("Python is simple and effective!"))
print(get_longest_word("Any pythonista like namespaces a lot."))
