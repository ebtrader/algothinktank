# OOP tutorial
# 3 Instance Methods
# https://towardsdatascience.com/understand-o-o-p-in-python-with-one-article-bfa76f3ba48c

class Dog:
    def barks(self):  # this is defining the method.  the function is receiving the parameter 'self'.
        print("Woof-woof")

my_dog = Dog()

print (my_dog.barks())