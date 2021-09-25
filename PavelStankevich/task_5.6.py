# Task 5.6
def call_once(func):
    """Run a function or method once and caches the result. All consecutive calls 
    to this function return cached result no matter the arguments."""
    def wrapper(*args, **kwargs):
        if wrapper.result is None:
            wrapper.result = func(*args, **kwargs)
        return wrapper.result
    wrapper.result = None
    return wrapper


@call_once
def sum_of_numbers(a, b):
    return a + b

print(sum_of_numbers(13, 42))
print(sum_of_numbers(999, 100))
print(sum_of_numbers(134, 412))
print(sum_of_numbers(856, 232))