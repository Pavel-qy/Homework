# Task 5.3

def get_top_performers(file_path, number_of_top_students=5):
    """Receive file path and return names of top performer students."""
    with open(file_path) as file:
        file.readline()
        performers = file.readlines()
    
    performers = [string.rstrip().split(",") for string in performers]
    performers.sort(key=lambda elem: float(elem[-1]), reverse=True)
    return [elem[0] for elem in performers[:number_of_top_students]]

def get_sort_by_age(file_path_source, file_path_result):
    """Receive the file path with students info and writes 
    CSV student information to the new file in descending order of age. """
    with open(file_path_source) as file_source, open(file_path_result, "w") as file_result:
        first_line = file_source.readline()
        performers = file_source.readlines()
        performers = [string.split(",") for string in performers]
        performers.sort(key=lambda elem: float(elem[1]), reverse=True)
        file_source.seek(0)
        file_result.write(file_source.readline())
        file_result.writelines([",".join(string) for string in performers])


print(get_top_performers("data/students.csv"))

get_sort_by_age("data/students.csv", "data/students_by_age.csv")