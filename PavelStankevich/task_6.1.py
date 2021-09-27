# Task 6.1
class Counter:
    """
    The Counter object optionally accept the start value and the counter
    stop value. If the start value is not specified the counter begin with 0.
    If the stop value is not specified it count up infinitely.
    If the counter reache the stop value, print 'Maximal value is reached'.
    """
    def __init__(self, start=0, stop=float("inf")):
        self.start = start
        self.stop = stop
  
    def increment(self):
        if self.start < self.stop:
            self.start += 1
        else:
            print("Maximal value is reached.")
        
    def get(self):
        print(self.start)


c = Counter(start=42)
c.increment()
c.get()

c = Counter()
c.increment()
c.get()
c.increment()
c.get()

c = Counter(start=42, stop=43)
c.increment()
c.get()
c.increment()
c.get()
