# Task 6.4
#
# Create hierarchy out of birds. 
# Implement 4 classes:
# * class `Bird` with an attribute `name` and methods `fly` and `walk`.
# * class `FlyingBird` with attributes `name`, `ration`, and with the same methods. 
# `ration` must have default value. 
# Implement the method `eat` which will describe its typical ration.
# * class `NonFlyingBird` with same characteristics but which obviously without attribute `fly`.
# Add same "eat" method but with other implementation regarding the swimming bird tastes.
# * class `SuperBird` which can do all of it: walk, fly, swim and eat.
# But be careful which "eat" method you inherit.
#
# Implement str() function call for each class.


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
    
    def fly(self):
        print(AttributeError(f"'{self.name}' object has no attribute 'fly'"))

    def swim(self):
        print(f"{self.name} bird can swim")
  
    def eat(self):
        print(f"It eats {self.ration}")


class SuperBird(NonFlyingBird, FlyingBird):
    def __str__(self):
        return str(print(f"{self.name} bird can fly, swim and walk"))

    def fly(self):
        super(NonFlyingBird, self).fly()


b = Bird("Any")
b.walk()
print()

p = NonFlyingBird("Penguin", "fish")
p.swim()
p.fly()
p.eat()
print()

c = FlyingBird("Canary")
str(c)
c.eat()
print()

s = SuperBird("Gull")
str(s)
s.eat()
s.fly()