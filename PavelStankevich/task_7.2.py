# Task 7.2
#
# Implement context manager for opening and working with file, 
# including handling exceptions with @contextmanager decorator.

from contextlib import contextmanager


@contextmanager
def context_manager(filename, mode):
    file = open(filename, mode)
    yield file
    file.close()


with context_manager("text.txt", "w") as file:
    file.write("@contextmanager, test text.")
    # print(file.read())