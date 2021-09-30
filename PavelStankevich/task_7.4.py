# Task 7.4
#
# Implement decorator for supressing exceptions. 
# If exception not occure write log to console.

def supression(func):
    def wrap(*args):
        result = None
        try:
            result = func(*args)
        except:
            pass
        else:
            print("No exceptions occurred")
        return print(result)
            
    return wrap

@supression
def division(a, b):
    return a / b


division(3, 0)
