# Task 4.5
def get_digits(digits):
    '''Return a tuple of a given integer's digits.'''
    return tuple([int(c) for c in str(digits)])

print(get_digits(87178291199))
