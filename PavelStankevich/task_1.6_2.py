nums = []

for _ in range(4):
    nums.append(int(input()[-1]))

for i in range(nums[0] - 1, nums[1] + 1):
    if i == nums[0] - 1:
        print(' ', end='   ')

        for j in range(nums[2], nums[3] + 1):
            print(f'{j: ^5}', end=' ')

        print()
        continue

    print(i, end='   ')

    for j in range(nums[2], nums[3] + 1):
        print(f'{i * j: ^5}', end=' ')

    print()
