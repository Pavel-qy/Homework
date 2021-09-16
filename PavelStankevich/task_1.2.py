string = input().lower()
result = dict()

for c in string:
    result[c] = string.count(c)

print(result)
