# Task 4.10
def generate_squares(num):
    '''Return a dictionary, where the key is a number and the value is the square of that number.'''
    return {num: num**2 for num in range(1, num + 1)}

print(generate_squares(5))