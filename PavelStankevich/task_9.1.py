# Task 9.1
#
# Implement the [dining philosophers problem]

from threading import Thread, Lock
from time import sleep


class Deadlock:
    def __init__(self):
        self.lock_1 = Lock()
        self.lock_2 = Lock()
        self.lock_3 = Lock()

    def fork_1(self, name):
        self.lock_1.acquire()
        print(f"{name} took 'fork_1'. {self.lock_1.locked()=}")

    def fork_2(self, name):
        self.lock_2.acquire()
        print(f"{name} took 'fork_2'. {self.lock_2.locked()=}")

    def fork_3(self, name):
        self.lock_3.acquire()
        print(f"{name} took 'fork_3'. {self.lock_3.locked()=}")


deadlock = Deadlock()

def thinker_1():
    while True:
        flag = 0
        if not deadlock.lock_1.locked():
            deadlock.fork_1("Thinker #1")
            flag += 1
        if not deadlock.lock_2.locked():
            deadlock.fork_2("Thinker #1")
            flag += 1
        
        if flag == 2:
            deadlock.lock_1.release()
            print(f"'Thinker #1' put down 'fork_1'. {deadlock.lock_1.locked()=}")
            sleep(1)
            deadlock.lock_2.release()
            print(f"'Thinker #1' put down 'fork_2'. {deadlock.lock_2.locked()=}")

def thinker_2():
    while True:
        flag = 0
        if not deadlock.lock_2.locked():
            deadlock.fork_2("Thinker #2")
            flag += 1
        if not deadlock.lock_3.locked():
            deadlock.fork_3("Thinker #2")
            flag += 1
        
        if flag == 2:
            deadlock.lock_2.release()
            print(f"'Thinker #2' put down 'fork_2'. {deadlock.lock_2.locked()=}")
            sleep(0.9)
            deadlock.lock_3.release()
            print(f"'Thinker #2' put down 'fork_3'. {deadlock.lock_3.locked()=}")

def thinker_3():
    flag = 0
    while True:
        if not deadlock.lock_3.locked():
            deadlock.fork_3("Thinker #3")
            flag += 1
        if not deadlock.lock_1.locked():
            deadlock.fork_1("Thinker #3")
            flag += 1
        
        if flag == 2:
            deadlock.lock_3.release()
            print(f"'Thinker #3' put down 'fork_3'. {deadlock.lock_1.locked()=}")
            sleep(0.95)
            deadlock.lock_1.release()
            print(f"'Thinker #3' put down 'fork_1'. {deadlock.lock_2.locked()=}")


th_1 = Thread(target=thinker_1)
th_2 = Thread(target=thinker_2)
th_3 = Thread(target=thinker_3)

th_1.start()
th_2.start()
th_3.start()
