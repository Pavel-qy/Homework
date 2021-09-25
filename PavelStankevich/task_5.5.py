# Task 5.5
def remember_result(func):
    """Remember last result of function it decorates and prints it before next call."""
    def wrapper(*args):
        print(f"Last result = '{wrapper.last_result}'")
        wrapper.last_result = func(*args)
    wrapper.last_result = None
    return wrapper

@remember_result
def sum_list(*args):
    if args and type(args[0]) == int:
        result = 0
    elif type(args[0]) == str:
        result = ""
    
    for item in args:
        result += item
    print(f"Current result = '{result}'")
    return result

sum_list("a", "b")
sum_list("abc", "cde")
sum_list(3, 4, 5)
