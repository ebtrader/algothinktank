# https://realpython.com/python3-object-oriented-programming/

class Dog:
    species = 'Canis familiaris'
    def __init__(self, name, age):
        self.name = name
        self.age = age

buddy = Dog('Buddy', 9)
miles = Dog('Miles', 4)

print (buddy.name)

print (buddy.age)

print (miles.name)
print (miles.age)

print (buddy.species)

buddy.age = 10

print(buddy.age)

miles.species = 'Felis silvestris'
print (miles.species)
