# OOP tutorial
# https://towardsdatascience.com/understand-o-o-p-in-python-with-one-article-bfa76f3ba48c

class Dog:
    def barks(self):  # this is defining the method.  the function is receiving the parameter 'self'.
        bark = ''
        print(self.bark)

my_dog = Dog()

my_dog.bark = 'ruff-ruff!'

my_dog.barks()

my_dog.bark = 'woof-woof!'

my_dog.barks()

