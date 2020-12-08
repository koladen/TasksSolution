"""
You are the owner of a cafe where 3 chefs work: a JapaneseCook, RussianCook and ItalianCook. Each of them can prepare
the national food and beverage:
- JapaneseCook: Sushi and Tea;
- RussianCook: Dumplings and Compote;
- ItalianCook: Pizza and Juice.
Your task is to create 3 different subclasses (one for each chef) which are the children of an AbstractCook and have
these methods:
- add_food(food_amount, food_price), which add to the client's order the value of the food which he had chosen;
- add_drink(drink_amount, drink_price), which add to the client's order the value of the drink which he had chosen;
- total(), which returns a string like: 'Foods: 150, Drinks: 50, Total: 200', and for the each chef instead of the Foods
 and Drinks will be the national food and drink that he’s used.
Every client can choose only one chef. In this mission the Abstract Factory design pattern could help.
"""
#####################SOLUTION ONE#########################################

# from abc import ABC, abstractmethod
#
#
# class AbstractCook(ABC):
#
#     @abstractmethod
#     def add_food(self, food_amount, food_price):
#         raise NotImplementedError()
#
#     @abstractmethod
#     def add_drink(self, drink_amount, drink_price):
#         raise NotImplementedError()
#
#     @abstractmethod
#     def total(self):
#         raise NotImplementedError()
#
#
# class JapaneseCook(AbstractCook):
#
#     def __init__(self):
#         self.food = 'Sushi'
#         self.drink = 'Tea'
#         self.meals = {self.food: 0, self.drink: 0, 'Total': 0}
#
#     def add_food(self, amount, price):
#         value = amount * price
#         self.meals[self.food] = self.meals.setdefault(self.food, 0) + value
#         self.calculate_total(value)
#
#     def add_drink(self, amount, price):
#         value = amount * price
#         self.meals[self.drink] = self.meals.setdefault(self.drink, 0) + value
#         self.calculate_total(value)
#
#     def total(self):
#         result = f'{self.food}: {self.meals[self.food]}, {self.drink}: {self.meals[self.drink]}, Total: {self.meals["Total"]}'
#         return result
#
#     def calculate_total(self, value):
#         self.meals['Total'] = self.meals.setdefault('Total', 0) + value
#
#
# class RussianCook(AbstractCook):
#     def __init__(self):
#         self.food = 'Dumplings'
#         self.drink = 'Compote'
#         self.meals = {self.food: 0, self.drink: 0, 'Total': 0}
#
#     def add_food(self, amount, price):
#         value = amount * price
#         self.meals[self.food] = self.meals.setdefault(self.food, 0) + value
#         self.calculate_total(value)
#
#     def add_drink(self, amount, price):
#         value = amount * price
#         self.meals[self.drink] = self.meals.setdefault(self.drink, 0) + value
#         self.calculate_total(value)
#
#     def total(self):
#         result = f'{self.food}: {self.meals[self.food]}, {self.drink}: {self.meals[self.drink]}, Total: {self.meals["Total"]}'
#         return result
#
#     def calculate_total(self, value):
#         self.meals['Total'] = self.meals.setdefault('Total', 0) + value
#
#
# class ItalianCook(AbstractCook):
#     def __init__(self):
#         self.food = 'Pizza'
#         self.drink = 'Juice'
#         self.meals = {self.food: 0, self.drink: 0, 'Total': 0}
#
#     def add_food(self, amount, price):
#         value = amount * price
#         self.meals[self.food] = self.meals.setdefault(self.food, 0) + value
#         self.calculate_total(value)
#
#     def add_drink(self, amount, price):
#         value = amount * price
#         self.meals[self.drink] = self.meals.setdefault(self.drink, 0) + value
#         self.calculate_total(value)
#
#     def total(self):
#         result = f'{self.food}: {self.meals[self.food]}, {self.drink}: {self.meals[self.drink]}, Total: {self.meals["Total"]}'
#         return result
#
#     def calculate_total(self, value):
#         self.meals['Total'] = self.meals.setdefault('Total', 0) + value



#####################SOLUTION TWO#########################################

from abc import ABC, abstractmethod


class AbstractCook(ABC):

    @abstractmethod
    def __init__(self):
        self.total_amount = 0

    @abstractmethod
    def add_food(self, amount, price):
        value = amount * price
        self.food.amount += value
        self.calculate_total(value)

    @abstractmethod
    def add_drink(self, amount, price):
        value = amount * price
        self.drink.amount += value
        self.calculate_total(value)

    @abstractmethod
    def total(self):
        result = f'{self.food.name}: {self.food.amount}, {self.drink.name}: {self.drink.amount}, Total: {self.total_amount}'
        return result

    def calculate_total(self, value):
        self.total_amount += value


class Food(ABC):
    def __init__(self, name):
        self.amount = 0
        self.name = name


class Drink(ABC):
    def __init__(self, name):
        self.amount = 0
        self.name = name


# class Sushi(Food):
#     def __init__(self, name):
#         super().__init__(name)
#
#
# class Tea(Drink):
#     def __init__(self, name):
#         super().__init__(name)
#
#
# class Dumplings(Food):
#     def __init__(self, name):
#         super().__init__(name)
#
#
# class Compote(Drink):
#     def __init__(self, name):
#         super().__init__(name)
#
#
# class Pizza(Food):
#     def __init__(self, name):
#         super().__init__(name)
#
#
# class Juice(Drink):
#     def __init__(self, name):
#         super().__init__(name)


class JapaneseCook(AbstractCook):

    def __init__(self):
        super().__init__()
        # self.food = Sushi('Sushi')
        # self.drink = Tea('Tea')
        self.food = Food('Sushi')
        self.drink = Drink('Tea')
        self.total_amount = 0

    def add_food(self, amount, price):
        super().add_food(amount, price)

    def add_drink(self, amount, price):
        super().add_drink(amount, price)

    def total(self):
        result = super().total()
        return result

    def calculate_total(self, value):
        super().calculate_total(value)


class RussianCook(AbstractCook):

    def __init__(self):
        super().__init__()
        # self.food = Dumplings('Dumplings')
        # self.drink = Compote('Compote')
        self.food = Food('Dumplings')
        self.drink = Drink('Compote')
        self.total_amount = 0

    def add_food(self, amount, price):
        super().add_food(amount, price)

    def add_drink(self, amount, price):
        super().add_drink(amount, price)

    def total(self):
        result = super().total()
        return result

    def calculate_total(self, value):
        super().calculate_total(value)


class ItalianCook(AbstractCook):

    def __init__(self):
        super().__init__()
        # self.food = Pizza('Pizza')
        # self.drink = Juice('Juice')
        self.food = Food('Pizza')
        self.drink = Drink('Juice')
        self.total_amount = 0

    def add_food(self, amount, price):
        super().add_food(amount, price)

    def add_drink(self, amount, price):
        super().add_drink(amount, price)

    def total(self):
        result = super().total()
        return result

    def calculate_total(self, value):
        super().calculate_total(value)


client_1 = JapaneseCook()
client_1.add_food(2, 20)
client_1.add_drink(5, 4)
assert client_1.total() == "Sushi: 40, Tea: 20, Total: 60"

client_2 = RussianCook()
client_2.add_food(1, 40)
client_2.add_drink(5, 20)
assert client_2.total() == "Dumplings: 40, Compote: 100, Total: 140"

client_3 = ItalianCook()
client_3.add_food(2, 20)
client_3.add_drink(2, 10)
assert client_3.total() == "Pizza: 40, Juice: 20, Total: 60"