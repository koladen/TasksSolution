"""
In the previous mission - Warriors - you've learned how to make a duel between 2 warriors happen. Great job! But let's
move on to something that feels a little more epic - armies! In this mission your task is to add new classes and
functions to the existing ones. The new class should be the Army and have the method add_units() - for adding the
chosen amount of units to the army. The first unit added will be the first to go to fight, the second will be the
second, ...
Also you need to create a Battle() class with a fight() function, which will determine the strongest army.
The battles occur according to the following principles:
at first, there is a duel between the first warrior of the first army and the first warrior of the second army. As soon
as one of them dies - the next warrior from the army that lost the fighter enters the duel, and a new fight begins
 between him and the surviving warrior, who keeps his remaining health. This continues until all the soldiers of one
 of the armies die. In this case, the fight() function should return True, if the first army won, or False, if the
 second one was stronger.
Note that army 1 has the advantage to start every fight!
"""
class Warrior:
    def __init__(self, health=50, attack=5):
        self._health = health
        self._attack = attack


    @property
    def is_alive(self):
        return self._health > 0

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = value

    @property
    def attack(self):
        return self._attack

    @attack.setter
    def attack(self, value):
        self._attack = value

    def get_hit(self, points):
        self._health -= points


class Knight(Warrior):
    def __init__(self):
        super().__init__(attack=7)


class Army:
    def __init__(self):
        self._army = []

    def add_units(self, fighter, count):
        self._army = [fighter() for _ in range(count)]

    @property
    def get_unit(self):
        return self._army.pop(0)

    @property
    def len_army(self):
        return len(self._army)


class Battle:
    def __init__(self):
        pass

    def fight(self, *armyes):

        first_fighter = armyes[0].get_unit
        second_fighter = armyes[1].get_unit
        while first_fighter.is_alive and second_fighter.is_alive:#armyes[1].len_army > 0:#min(army.len_army for army in armyes) > 0:
            winner = fight_units(first_fighter, second_fighter)
            if first_fighter is winner:
                if armyes[1].len_army > 0:
                    second_fighter = armyes[1].get_unit
            elif second_fighter is winner:
                if armyes[0].len_army > 0:
                    first_fighter = armyes[0].get_unit

        return first_fighter.is_alive and armyes[1].len_army == 0

def fight_units(*units):
    # print('ПЕРВЫЙ  ' + str(units[0]), 'ВТОРОЙ  ' + str(units[1]))
    # print('здоровье 1-го ' + str(units[0].health), ' здоровье 2-го ' + str(units[1].health), ' НАЧИНАЕМ!')
    while min(unit.health for unit in units) > 0:
        if units[0].is_alive:
            units[1].get_hit(units[0].attack)
            # print('здоровье 1-го ' + str(units[0].health), ' здоровье 2-го ' + str(units[1].health), ' тюк второго!')
        if units[1].is_alive:
            units[0].get_hit(units[1].attack)
            # print('здоровье 1-го ' + str(units[0].health), ' здоровье 2-го ' + str(units[1].health), ' тюк первого!')
    winner = units[0] if units[0].is_alive else units[1]

    # print('ППППООБББЕДДДИЛЛЛЛ ' + str(winner))
    return winner

army_1 = Army()
army_2 = Army()
army_1.add_units(Warrior, 2)
print(army_1._army)
print(army_1.len_army)
army_2.add_units(Warrior, 2)
print(army_2._army)
print(army_2.len_army)
battle = Battle()
print(battle.fight(army_1, army_2))

