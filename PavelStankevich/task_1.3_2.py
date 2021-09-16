num, result = int(input()), list()

for i in range(1, num + 1):
    if num % i == 0:
        result.append(i)

print(result)
