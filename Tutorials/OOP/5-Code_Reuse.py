# OOP tutorial
# 5 Code Reuse
# https://towardsdatascience.com/understand-o-o-p-in-python-with-one-article-bfa76f3ba48c

class MyTransports():
    def __init__(self, color, brand):
        self.color = color
        self.brand = brand

class Car(MyTransports):
    pass

class Train(MyTransports):
    pass

my_train = Train('gray', 'Tesla')

