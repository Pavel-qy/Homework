# Task 7.5
#
# Implement function for check that number is even and 
# is greater than 2. Throw different exceptions for this 
# errors. Custom exceptions must be derived from custom 
# base exception(not Base Exception class).

class NumberIsNotMoreThanTwo(ValueError):
    pass

class NumberIsOdd(ValueError):
    pass

def validate(num):
    if num <= 2:
        raise NumberIsNotMoreThanTwo(num)
    elif num % 2:
        raise NumberIsOdd(num)


validate(1)
validate(5)
