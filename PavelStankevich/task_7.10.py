# Task 4.10
#
# Implement a generator which will generate odd numbers endlessly.

def endless_generator():
    n = 1
    while True:
        yield n
        n += 2


gen = endless_generator()
while True:
    print(next(gen))