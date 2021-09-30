# Task 7.6
#
# Create console program for proving Goldbach's conjecture. 
# Program accepts number for input and print result. For 
# pressing 'q' program succesfully close. Use function 
# from Task 5.5 for validating input, handle all exceptions 
# and print user friendly output.

def input_validation(func):
    def wrap(*args):
        if len(args) > 1:
            raise ValueError("The function takes only one argument.")
        if not isinstance(args[0], int):
            raise ValueError("The function takes only a real number.")
        if args[0] < 4 or args[0] % 2 != 0:
            raise ValueError("The hypothesis is valid for an even number equal to or greater than four.")
        nums = func(args[0])
        return print(f"'{args[0]}' is the sum of two primes: '{nums[0]}' and '{nums[1]}'")

    return wrap

def is_prime(num):
    for i in range(2, num):
        if num % i == 0:
            return False
    return True

@input_validation
def goldbach_hypothesis_check(num):
    for i in range(2, int(num / 2) + 1):
        if is_prime(i):
            if is_prime(num - i):
                return (i, num - i)


goldbach_hypothesis_check(154)
