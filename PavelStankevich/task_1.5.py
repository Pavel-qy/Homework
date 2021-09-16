dicts = input().strip("[]").split(",")
values = list()

for item in dicts:
    values.append(item.split('"')[-2])

print(set(values))
