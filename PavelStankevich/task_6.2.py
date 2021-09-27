# Task 6.2
class HistoryDict:
    """
    Custom dictionary that memorize 10 latest changed keys.
    Using method 'get_history' return this keys.
    """
    def __init__(self, dct):
        self.dct = dct
    
    def set_value(self, *args):
        self.history = list()
        for i in range(0, len(args), 2):
            self.dct[args[i]] = args[i+1]
            self.history.append(args[i])
    
    def get_history(self):
        print(self.history[-10:])


d = HistoryDict({"foo": 42})
d.set_value("bar", 43, "baz", 44, "foo", 49)
d.get_history()
