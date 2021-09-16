words = input().strip("['']").split("', '")
words = set(words)
print(sorted(words))
