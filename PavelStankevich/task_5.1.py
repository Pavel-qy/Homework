# Task 5.1
'''Open file `data/unsorted_names.txt` in data folder. 
Sort the names and write them to a new file called `sorted_names.txt`.'''

with open("data/unsorted_names.txt") as unsorted_names, \
    open("data/sorted_names.txt", "w") as sorted_names:
    names = unsorted_names.readlines()
    names.sort()
    sorted_names.writelines(names)
