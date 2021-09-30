# Task 7.3
#
# Implement decorator with context manager support for 
# writing execution time to log-file. See contextlib module.

from datetime import datetime


def time_logging(func):
    def wrap(*args):
        start_time = datetime.utcnow()
        result = func(*args)
        execution_time = datetime.utcnow() - start_time
        with open("log.txt", "a", encoding="utf-8") as log_file:
            log_file.write(f"\nВходные параметры: {args}\
                \nВремя выполнения: {execution_time}\n")
        return result
    return wrap

DB = {0: 0, 1: 1}

@time_logging
def fibonacci(n):
    for i in range(n + 1):
        if DB.get(i) is None:
            DB[i] = DB[i - 1] + DB[i - 2]
    
    return DB[n]


fibonacci(100000)
