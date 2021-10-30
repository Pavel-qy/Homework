
# Task 7.1
#
# Implement class-based context manager for opening 
# and working with file, including handling exceptions. 
# Do not use 'with open()'. Pass filename and mode via 
# constructor.

class ContextManager:
    """
    A class-based context manager for opening and working with a file.

    Parameters
    ----------
    filename : str
        the path and name of the file

    mode : str
        a string, define which mode you want to open the file in            
        "r" - Read - Default value. Opens a file for reading, error if the file does not exist
        "a" - Append - Opens a file for appending, creates the file if it does not exist
        "w" - Write - Opens a file for writing, creates the file if it does not exist
        "x" - Create - Creates the specified file, returns an error if the file exist            
        In addition you can specify if the file should be handled as binary or text mode
        "t" - Text - Default value. Text mode
        "b" - Binary - Binary mode
    """
    def __init__(self, filename, mode):
        self.filename = self.is_string(filename, "filename")
        self.mode = self.mode_validation(mode)

    def __enter__(self):
        file = open(self.filename, self.mode)
        return file

    def __exit__(self, exc_type, exc_value, exc_traceback):
        file.close()
    
    def is_string(self, value, parameter_name):
        """
        Checks if the passed argument is a string.

        Parameters
        ----------
        value : str
            value of the passed argument

        parameter_name : str
            name of the passed argument
            used for better readability of the exception
        """
        if not isinstance(value, str):
            raise AttributeError(f"'{parameter_name}' takes only a string. '{value}' – is not a string!")
        return value

    def mode_validation(self, mode):
        """
        Check if the passed mode is correct.

        Parameters
        ----------
        mode : str
            a string, define which mode you want to open the file in   
        """
        self.is_string(mode, "mode")
        if len(mode) < 0 or len(mode) > 3:
            raise AttributeError("The mod parameter takes one to three characters!")
        elif len(mode) == 1 and mode not in "rwaxtb":
            raise AttributeError(f"'{mode}' – there is no such parameter!")
        elif len(mode) == 2 and (mode[0] not in "rwax" or mode[1] not in "+tb"):
            raise AttributeError(f"'{mode}' – there is no such combination of parameters!")
        elif len(mode) == 3 and (mode[0] not in "rwax" or \
            mode[1] not in "+" or mode[2] not in "tb"):
            raise AttributeError(f"'{mode}' – there is no such combination of parameters!")
        return mode


with ContextManager("text.txt", "a") as file:
    file.write("Test text.")
    # print(file.read())
