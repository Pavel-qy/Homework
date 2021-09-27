# Task 6.4
class Bird:
    def __init__(self, name):
        self.name = name
  
    def __str__(self):
        return str(f"{self.name} bird can fly and walk")
  
    def fly(self):
        print(f"{self.name} bird can fly")
    
    def walk(self):
        print(f"{self.name} bird can walk")
  

class FlyingBird(Bird):
    def __init__(self, name, ration="grains"):
        super().__init__(name)
        self.ration = ration
  
    def __str__(self):
        return str(print(f"{self.name} can fly and walk"))
  
    def eat(self):
        print(f"It eats mostly {self.ration}")


class NonFlyingBird(FlyingBird):
    def __init__(self, name, ration="fish"):
        super().__init__(name, ration)
    
    def swim(self):
        print(f"{self.name} bird can swim")
    
    def fly(self):
        raise AttributeError(f"'{self.name}' object has no attribute 'fly'")
  
    def eat(self):
        print(f"It eats {self.ration}")


class SuperBird(NonFlyingBird, FlyingBird):
    def __str__(self):
      return str(print(f"{self.name} bird can fly, swim and walk"))


b = Bird("Any")
b.walk()
print()

p = NonFlyingBird("Penguin", "fish")
p.swim()
# p.fly()
p.eat()
print()

c = FlyingBird("Canary")
str(c)
c.eat()
print()

s = SuperBird("Gull")
str(s)
s.eat()