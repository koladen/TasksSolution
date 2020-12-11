###################  SOLUTION BY CLASS #####################
# class Capital:
#     _instance = None
#
#     def __new__(cls, name):
#         if cls._instance is None:
#             cls._instance = object.__new__(cls)
#             cls._instance._name = name
#         return cls._instance
#
#     def name(self):
#         return self._name

###################  SOLUTION BY DECORATOR ##################

def singleton(cls):
    instances = {}

    def getinstance(*args):
        if cls not in instances:
            cls_instance = cls()
            cls_instance._name = args[0]
            instances[cls] = cls_instance

        return instances[cls]
    return getinstance


@singleton
class Capital:
    def name(self):
        return self._name


ukraine_capital_1 = Capital("Kyiv")
ukraine_capital_2 = Capital("London")
ukraine_capital_3 = Capital("Marocco")
assert ukraine_capital_2.name() == "Kyiv"
assert ukraine_capital_3.name() == "Kyiv"