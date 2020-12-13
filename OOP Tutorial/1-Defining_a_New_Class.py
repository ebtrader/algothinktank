# OOP tutorial
# https://towardsdatascience.com/understand-o-o-p-in-python-with-one-article-bfa76f3ba48c

class Car:
    def __init__(self, brand, color):
        self.brand = brand
        self.color = color

    def __repr__(self):
        return 'My car is {} and was produced by {}'.format(self.color, self.brand)
#instance #1 of the car class
my_car = Car('Tesla', 'black')

print(my_car)

print(my_car.color)

print(my_car.brand)

print(my_car.brand.upper())

print(my_car.color.capitalize())

#instance #2 of the car class

my_friends_car = Car('Lambo', 'yellow')

print (my_friends_car.brand.upper())