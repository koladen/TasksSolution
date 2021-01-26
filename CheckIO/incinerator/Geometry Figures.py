"""
Паттерн Стратегия
"""

from math import sqrt

PI = 3.1415


class Shape:
    @staticmethod
    def convert(x):
        if x-int(x) == 0.0 or x-int(x) == 0:
            return int(x)
        else:
            return round(x, 2)

    def volume(self, parameter):
        return 0


class Parameters:
    def __init__(self, parameter):
        self.parameter = parameter
        self.figure = None

    def choose_figure(self, figure):
        self.figure = figure

    def perimeter(self):
        return self.figure.perimeter(self.parameter)

    def area(self):
        return self.figure.area(self.parameter)

    def volume(self):
        return self.figure.volume(self.parameter)


class Circle(Shape):

    def perimeter(self, parameter):
        x = 2*PI*parameter
        return self.convert(x)

    def area(self, parameter):
        x = PI * (parameter**2)
        return self.convert(x)


class Triangle(Shape):
    def perimeter(self, parameter):
        x = 3*parameter
        return self.convert(x)

    def area(self, parameter):
        x = sqrt(3)/4*(parameter**2)
        return self.convert(x)


class Square(Shape):
    def perimeter(self, parameter):
        x = 4*parameter
        return self.convert(x)

    def area(self, parameter):
        x = parameter**2
        return self.convert(x)


class Pentagon(Shape):
    def perimeter(self, parameter):
        x = 5*parameter
        return self.convert(x)

    def area(self, parameter):
        x = 1.72 * (parameter**2)
        return self.convert(x)


class Hexagon(Shape):
    def perimeter(self, parameter):
        x = 6*parameter
        return self.convert(x)

    def area(self, parameter):
        x = 3*sqrt(3)/2*(parameter**2)
        return self.convert(x)


class Cube(Shape):
    def perimeter(self, parameter):
        x = 12*parameter
        return self.convert(x)

    def area(self, parameter):
        x = 6*(parameter**2)
        return self.convert(x)

    def volume(self, parameter):
        x = parameter**3
        return self.convert(x)


figure = Parameters(10)

figure.choose_figure(Circle())
assert figure.area() == 314.15

figure.choose_figure(Triangle())
assert figure.perimeter() == 30

figure.choose_figure(Square())
assert figure.area() == 100

figure.choose_figure(Pentagon())
assert figure.perimeter() == 50

figure.choose_figure(Hexagon())
assert figure.perimeter() == 60

figure.choose_figure(Cube())
assert figure.volume() == 1000