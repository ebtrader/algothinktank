# https://realpython.com/python3-object-oriented-programming/

class Dog:
    # Leave other parts of Dog class as-is
    species = "Canis familiaris"

    def __init__(self, name, age):
        self.name = name
        self.age = age

    # Instance method
 #   def description(self):
 #       return f"{self.name} is {self.age} years old"

    # Another instance method
    def speak(self, sound):
        return f"{self.name} says {sound}"

    # Replace .description() with __str__()
    def __str__(self):
        return f"{self.name} is {self.age} years old"

names = ['Fletcher', 'David', 'Dan']
print(names)

miles = Dog('Miles', 4)
print(miles)

