"""
So we have 3 types of units: the Warrior, Knight and Defender. Let's make the battles even more epic and add another
type - the Vampire!
Vampire should be the subclass of the Warrior class and have the additional vampirism parameter, which helps him to heal
 himself. When the Vampire hits the other unit, he restores his health by +50% of the dealt damage (enemy defense makes
 the dealt damage value lower).
The basic parameters of the Vampire:
health = 40
attack = 4
vampirism = 50%
You should store vampirism attribute as an integer (50 for 50%). It will be needed to make this solution evolutes to fit
 one of the next challenges of this saga.
"""


class Warrior:
    def __init__(self, health=50, attack=5, defense=0, vampirism=0):
        self._health = health
        self._attack = attack
        self._defense = defense
        self._vampirism = vampirism

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
    def vampirism(self):
        return self._vampirism

    @vampirism.setter
    def vampirism(self, value):
        self._vampirism = value

    @property
    def defense(self):
        return self._defense

    @defense.setter
    def defense(self, value):
        self._defense = value

    @property
    def attack(self):
        return self._attack

    @attack.setter
    def attack(self, value):
        self._attack = value

    def get_hit(self, points):
        if self._defense < points:
            damage = points-self._defense
        else:
            damage = 0
        heal = int(damage*(self._vampirism/100))
        self._health = self._health - damage + heal


class Knight(Warrior):
    def __init__(self):
        super().__init__(attack=7)


class Defender(Warrior):
    def __init__(self):
        super().__init__(health=60, attack=3, defense=2)


class Vampire(Warrior):
    def __init__(self):
        super().__init__(health=40, attack=4, vampirism=50)


class Army:
    def __init__(self):
        self._army = []

    def add_units(self, fighter, count):
        self._army.extend([fighter() for _ in range(count)])

    @property
    def get_unit(self):
        return self._army.pop(0)

    @property
    def len_army(self):
        return len(self._army)


class Battle:
    def __init__(self):
        pass

    @staticmethod
    def fight(*armyes):
        first_fighter = armyes[0].get_unit
        second_fighter = armyes[1].get_unit
        while first_fighter.is_alive and second_fighter.is_alive:
            winner = Battle.fight_units(first_fighter, second_fighter)
            if first_fighter is winner and armyes[1].len_army > 0:
                second_fighter = armyes[1].get_unit
            elif second_fighter is winner and armyes[0].len_army > 0:
                first_fighter = armyes[0].get_unit

        return first_fighter.is_alive and armyes[1].len_army == 0

    @staticmethod
    def fight_units(*units):
        while min(unit.health for unit in units) > 0:
            if units[0].is_alive:
                units[1].get_hit(units[0].attack)
            if units[1].is_alive:
                units[0].get_hit(units[1].attack)
        winner = units[0] if units[0].is_alive else units[1]
        return winner


my_army = Army()
my_army.add_units(Defender, 2)
my_army.add_units(Vampire, 2)
my_army.add_units(Warrior, 1)

enemy_army = Army()
enemy_army.add_units(Warrior, 2)
enemy_army.add_units(Defender, 2)
enemy_army.add_units(Vampire, 3)

army_3 = Army()
army_3.add_units(Warrior, 1)
army_3.add_units(Defender, 4)

army_4 = Army()
army_4.add_units(Vampire, 3)
army_4.add_units(Warrior, 2)

battle = Battle()

assert battle.fight(my_army, enemy_army) is False
assert battle.fight(army_3, army_4) is True