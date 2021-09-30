
# Task 7.1
#
# Implement class-based context manager for opening 
# and working with file, including handling exceptions. 
# Do not use 'with open()'. Pass filename and mode via 
# constructor.

class ContextManager:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode

    def __enter__(self):
        file = open(self.filename, self.mode)
        return file

    def __exit__(self, exc_type, exc_value, exc_traceback):
        file.close()


with ContextManager("text.txt", "w") as file:
    file.write("Test text.")
    # print(file.read())
