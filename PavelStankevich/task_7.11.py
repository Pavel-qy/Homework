# Task 4.11
#
# Implement a generator which will geterate Fibonacci numbers endlessly.

def endless_fib_generator():
    nums = [0, 1]
    i = 1
    while True:
        yield nums[i]
        nums.append(nums[i] + nums[i - 1])
        i += 1


gen = endless_fib_generator()
while True:
    print(next(gen))
