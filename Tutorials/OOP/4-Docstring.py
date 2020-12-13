# OOP tutorial
# https://towardsdatascience.com/understand-o-o-p-in-python-with-one-article-bfa76f3ba48c
#4-Add a Docstring

class Dog:
    def barks(self):
        """
        Prints the bark of my dog!

        """
        bark = ''
        print(self.bark)


my_dog = Dog()

help(my_dog.barks)
