"""
...the clashes between different soldiers occurred here and there, and the new troops kept coming. The conflict
gradually was starting to look more like a small war.
"Knights, hear my command! Take your shields! Strengthen the armor! We are taking too much beating," - Sir Ronald
shouted.
Nobody’s expected that Umbert's soldiers could compete with the well-trained knights, so at the beginning of the
battle the knights used exclusively two-handed swords - no one even thought of being on the defensive. But it seems
that it's time to back down and take one-handed swords and shields instead of the former deadly weapons. This will
slightly reduce the assault capacity of knights, but will allow them to better defend themselves against the dangerous
attacks of enemy soldiers.
In the previous mission - Army battles, you've learned how to make a battle between 2 armies. But we have only 2 types
of units - the Warriors and Knights. Let's add another one - the Defender. It should be the subclass of the Warrior
class and have an additional defense parameter, which helps him to survive longer. When another unit hits the defender,
he loses a certain amount of his health according to the next formula:
enemy attack - self defense (if enemy attack > self defense). Otherwise, the defender doesn't lose his health.
The basic parameters of the Defender:
health = 60
attack = 3
defense = 2
"""
class Warrior:
    def __init__(self, health=50, attack=5, defense=0):
        self._health = health
        self._attack = attack
        self._defense = defense


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
        self._health -= (points-self._defense) if points > self._defense else 0


class Knight(Warrior):
    def __init__(self):
        super().__init__(attack=7)


class Defender(Warrior):
    def __init__(self):
        super().__init__(health=60, attack=3, defense=2)


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


chuck = Warrior()
bruce = Warrior()
carl = Knight()
dave = Warrior()
mark = Warrior()
bob = Defender()
mike = Knight()
rog = Warrior()
lancelot = Defender()


my_army = Army()
my_army.add_units(Defender, 1)

enemy_army = Army()
enemy_army.add_units(Warrior, 2)

army_3 = Army()
army_3.add_units(Warrior, 1)
army_3.add_units(Defender, 1)

army_4 = Army()
army_4.add_units(Warrior, 2)

battle = Battle()

assert battle.fight(my_army, enemy_army) is False
assert battle.fight(army_3, army_4) is True
