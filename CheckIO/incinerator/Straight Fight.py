"""
A new unit type won’t be added in this mission, but instead we’ll add a new tactic - straight_fight(army_1, army_2).
It should be the method of the Battle class and it should work as follows:
at the beginning there will be a few duels between each pair of soldiers from both armies (the first unit against the
first, the second against the second and so on). After that all dead soldiers will be removed and the process repeats
until all soldiers of one of the armies will be dead. Armies might not have the same number of soldiers. If a warrior
doesn’t have an opponent from the enemy army - we’ll automatically assume that he’s won a duel (for example - 9th and
10th units from the first army, if the second has only 8 soldiers).
"""

from itertools import zip_longest


class Warrior:
    def __init__(self, health=50, attack=5, defense=0, vampirism=0, penetration=0):
        self._health = health
        self._max_health = health
        self._attack = attack
        self._defense = defense
        self._vampirism = vampirism
        self._penetration = penetration

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'H:{self._health!r},A:{self._attack!r},D:{self._defense!r})')

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
    def max_health(self):
        return self._max_health

    @max_health.setter
    def max_health(self, value):
        self._max_health = value

    @property
    def penetration(self):
        return self._penetration

    @penetration.setter
    def penetration(self, value):
        self._penetration = value

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

    def do_attack(self, enemy, enemy_units, ally_units, points):
        damage = Warrior._calculate_damage(enemy, points)
        enemy.health -= damage
        self._vampire_healing(damage)
        self._heal_ally_by_healer(ally_units)
        self._penetrate_enemy(enemy_units, damage)

    def _heal_ally_by_healer(self, ally_units):
        if ally_units and isinstance(ally_units[0], Healer):
            ally_units[0].heal(self)

    def _penetrate_enemy(self, enemy_units, damage):
        if enemy_units and isinstance(self, Lancer):
            self.penetrate_enemy(enemy_units, damage)

    def _vampire_healing(self, damage):
        if isinstance(self, Vampire):
            self.bite(damage)

    @staticmethod
    def _calculate_damage(enemy, points):
        if enemy.defense < points:
            damage = points - enemy.defense
        else:
            damage = 0
        return damage

    @staticmethod
    def _find_alive_warrior_index(units):
        unit_index = 0
        for index, unit in enumerate(units):
            if unit.is_alive:
                unit_index = index
                break
        return unit_index

    # DRY principle. Vampire and Healer both heal to maximum health
    @staticmethod
    def _check_max_heal(current_health, max_health, health_points):
        return min(current_health+health_points, max_health)


class Knight(Warrior):
    def __init__(self):
        super().__init__(attack=7)


class Defender(Warrior):
    def __init__(self):
        super().__init__(health=60, attack=3, defense=2)


class Vampire(Warrior):
    def __init__(self):
        super().__init__(health=40, attack=4, vampirism=50)

    def bite(self, damage):
        estimate_health_points = int(damage * (self._vampirism / 100))
        self._health = super()._check_max_heal(self.health, self.max_health, estimate_health_points)


class Lancer(Warrior):
    def __init__(self):
        super().__init__(health=50, attack=6, penetration=50)

# TODO подумать, а половину чего он должен наносить 2-му? Половину урона по первому,
# TODO или половину своего урона - защита 2-го?
    def penetrate_enemy(self, enemy_units, damage):
        second_line_enemy_index = super()._find_alive_warrior_index(enemy_units)
        enemy_units[second_line_enemy_index].health -= int(damage * (self._penetration / 100))


class Healer(Warrior):
    def __init__(self):
        super().__init__(health=60, attack=0)
        self._heal_points = 2

    def heal(self, ally_unit):
        ally_unit.health = super()._check_max_heal(ally_unit.health, ally_unit.max_health, self._heal_points)


class Army:
    def __init__(self):
        self._units = []

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, value):
        self._units = value

    def add_units(self, fighter, count):
        self._units.extend([fighter() for _ in range(count)])

    @property
    def get_unit(self):
        return self._units.pop(0)

    @property
    def len_army(self):
        return len(self._units)

    def __repr__(self):
        composition = ''
        for unit in self._units[:-1]:
            composition += str(unit) + ', '
        composition = composition + str(self._units[-1])
        return (f'{self.__class__.__name__}('
                f':{composition})')


class Battle:
    def __init__(self):
        pass

    @staticmethod
    def fight(*armyes):
        first_fighter = armyes[0].get_unit
        second_fighter = armyes[1].get_unit
        while first_fighter.is_alive and second_fighter.is_alive:
            winner = Battle.fight_units(armyes[0], armyes[1], first_fighter, second_fighter)
            if first_fighter is winner and armyes[1].len_army > 0:
                second_fighter = armyes[1].get_unit
            elif second_fighter is winner and armyes[0].len_army > 0:
                first_fighter = armyes[0].get_unit
        return first_fighter.is_alive and armyes[1].len_army == 0

    @staticmethod
    def straight_fight(army_1, army_2):
        while min(army_1.len_army, army_2.len_army) > 0:
            army_1.units = [unit for unit in army_1.units if unit.is_alive]
            army_2.units = [unit for unit in army_2.units if unit.is_alive]
            for unit1, unit2 in list(zip_longest(army_1.units, army_2.units)):
                fight(unit1, unit2)
        return army_1.len_army > 0

    @staticmethod
    def fight_units(army1, army2, *units):
        while min(unit.health for unit in units) > 0:
            if units[0].is_alive:
                units[0].do_attack(units[1], army2.units, army1.units, units[0].attack)
            if units[1].is_alive:
                units[1].do_attack(units[0], army1.units, army2.units, units[1].attack)
        winner = units[0] if units[0].is_alive else units[1]
        return winner


def find_winner(units):
    return units[0].is_alive


def fight(*units):
    if units[0] is None:
        return False
    elif units[1] is None:
        return True
    else:
        while min(unit.health for unit in units) > 0:
            if units[0].is_alive:
                units[0].do_attack(units[1], [], [], units[0].attack)
            if units[1].is_alive:
                units[1].do_attack(units[0], [], [], units[1].attack)

        return find_winner(units)


if __name__ == '__main__':
    # These "asserts" using only for self-checking and not necessary for auto-testing

    # fight tests
    chuck = Warrior()
    bruce = Warrior()
    carl = Knight()
    dave = Warrior()
    mark = Warrior()

    assert fight(chuck, bruce) is True
    assert fight(dave, carl) is False
    assert chuck.is_alive is True
    assert bruce.is_alive is False
    assert carl.is_alive is True
    assert dave.is_alive is False
    assert fight(carl, mark) is False
    assert carl.is_alive is False

    # battle tests
    my_army = Army()
    my_army.add_units(Knight, 3)

    enemy_army = Army()
    enemy_army.add_units(Warrior, 3)

    army_3 = Army()
    army_3.add_units(Warrior, 20)
    army_3.add_units(Knight, 5)

    army_4 = Army()
    army_4.add_units(Warrior, 30)

    battle = Battle()

    assert battle.fight(my_army, enemy_army) is True
    assert battle.fight(army_3, army_4) is False
    print("Coding complete? Let's try tests!")

if __name__ == '__main__':
    # These "asserts" using only for self-checking and not necessary for auto-testing

    # fight tests
    chuck = Warrior()
    bruce = Warrior()
    carl = Knight()
    dave = Warrior()
    mark = Warrior()
    bob = Defender()
    mike = Knight()
    rog = Warrior()
    lancelot = Defender()

    assert fight(chuck, bruce) is True
    assert fight(dave, carl) is False
    assert chuck.is_alive is True
    assert bruce.is_alive is False
    assert carl.is_alive is True
    assert dave.is_alive is False
    assert fight(carl, mark) is False
    assert carl.is_alive is False
    assert fight(bob, mike) is False
    assert fight(lancelot, rog) is True

    # battle tests
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
    print("Coding complete? Let's try tests!")

if __name__ == '__main__':
    # These "asserts" using only for self-checking and not necessary for auto-testing

    # fight tests
    chuck = Warrior()
    bruce = Warrior()
    carl = Knight()
    dave = Warrior()
    mark = Warrior()
    bob = Defender()
    mike = Knight()
    rog = Warrior()
    lancelot = Defender()
    eric = Vampire()
    adam = Vampire()
    richard = Defender()
    ogre = Warrior()

    # battle tests
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
    print("Coding complete? Let's try tests!")

if __name__ == '__main__':
    # These "asserts" using only for self-checking and not necessary for auto-testing

    # fight tests
    chuck = Warrior()
    bruce = Warrior()
    carl = Knight()
    dave = Warrior()
    mark = Warrior()
    bob = Defender()
    mike = Knight()
    rog = Warrior()
    lancelot = Defender()
    eric = Vampire()
    adam = Vampire()
    richard = Defender()
    ogre = Warrior()
    freelancer = Lancer()
    vampire = Vampire()

    assert fight(chuck, bruce) is True
    assert fight(dave, carl) is False
    assert chuck.is_alive is True
    assert bruce.is_alive is False
    assert carl.is_alive is True
    assert dave.is_alive is False
    assert fight(carl, mark) is False
    assert carl.is_alive is False
    assert fight(bob, mike) is False
    assert fight(lancelot, rog) is True
    assert fight(eric, richard) is False
    assert fight(ogre, adam) is True
    assert fight(freelancer, vampire) is True
    assert freelancer.is_alive is True

    # battle tests
    my_army = Army()
    my_army.add_units(Defender, 2)
    my_army.add_units(Vampire, 2)
    my_army.add_units(Lancer, 4)
    my_army.add_units(Warrior, 1)

    enemy_army = Army()
    enemy_army.add_units(Warrior, 2)
    enemy_army.add_units(Lancer, 2)
    enemy_army.add_units(Defender, 2)
    enemy_army.add_units(Vampire, 3)

    army_3 = Army()
    army_3.add_units(Warrior, 1)
    army_3.add_units(Lancer, 1)
    army_3.add_units(Defender, 2)

    army_4 = Army()
    army_4.add_units(Vampire, 3)
    army_4.add_units(Warrior, 1)
    army_4.add_units(Lancer, 2)

    battle = Battle()

    assert battle.fight(my_army, enemy_army) is True
    assert battle.fight(army_3, army_4) is False
    print("Coding complete? Let's try tests!")

if __name__ == '__main__':
    # These "asserts" using only for self-checking and not necessary for auto-testing

    # fight tests
    chuck = Warrior()
    bruce = Warrior()
    carl = Knight()
    dave = Warrior()
    mark = Warrior()
    bob = Defender()
    mike = Knight()
    rog = Warrior()
    lancelot = Defender()
    eric = Vampire()
    adam = Vampire()
    richard = Defender()
    ogre = Warrior()
    freelancer = Lancer()
    vampire = Vampire()
    priest = Healer()

    assert fight(chuck, bruce) is True
    assert fight(dave, carl) is False
    assert chuck.is_alive is True
    assert bruce.is_alive is False
    assert carl.is_alive is True
    assert dave.is_alive is False
    assert fight(carl, mark) is False
    assert carl.is_alive is False
    assert fight(bob, mike) is False
    assert fight(lancelot, rog) is True
    assert fight(eric, richard) is False
    assert fight(ogre, adam) is True
    assert fight(freelancer, vampire) is True
    assert freelancer.is_alive is True
    assert freelancer.health == 14
    priest.heal(freelancer)
    assert freelancer.health == 16

    # battle tests
    my_army = Army()
    my_army.add_units(Defender, 2)
    my_army.add_units(Healer, 1)
    my_army.add_units(Vampire, 2)
    my_army.add_units(Lancer, 2)
    my_army.add_units(Healer, 1)
    my_army.add_units(Warrior, 1)

    enemy_army = Army()
    enemy_army.add_units(Warrior, 2)
    enemy_army.add_units(Lancer, 4)
    enemy_army.add_units(Healer, 1)
    enemy_army.add_units(Defender, 2)
    enemy_army.add_units(Vampire, 3)
    enemy_army.add_units(Healer, 1)

    army_3 = Army()
    army_3.add_units(Warrior, 1)
    army_3.add_units(Lancer, 1)
    army_3.add_units(Healer, 1)
    army_3.add_units(Defender, 2)

    army_4 = Army()
    army_4.add_units(Vampire, 3)
    army_4.add_units(Warrior, 1)
    army_4.add_units(Healer, 1)
    army_4.add_units(Lancer, 2)

    battle = Battle()

    assert battle.fight(my_army, enemy_army) is False
    assert battle.fight(army_3, army_4) is True
    print("Coding complete? Let's try tests!")

if __name__ == '__main__':
    # These "asserts" using only for self-checking and not necessary for auto-testing

    # fight tests
    chuck = Warrior()
    bruce = Warrior()
    carl = Knight()
    dave = Warrior()
    mark = Warrior()
    bob = Defender()
    mike = Knight()
    rog = Warrior()
    lancelot = Defender()
    eric = Vampire()
    adam = Vampire()
    richard = Defender()
    ogre = Warrior()
    freelancer = Lancer()
    vampire = Vampire()
    priest = Healer()

    assert fight(chuck, bruce) is True
    assert fight(dave, carl) is False
    assert chuck.is_alive is True
    assert bruce.is_alive is False
    assert carl.is_alive is True
    assert dave.is_alive is False
    assert fight(carl, mark) is False
    assert carl.is_alive is False
    assert fight(bob, mike) is False
    assert fight(lancelot, rog) is True
    assert fight(eric, richard) is False
    assert fight(ogre, adam) is True
    assert fight(freelancer, vampire) is True
    assert freelancer.is_alive is True
    assert freelancer.health == 14
    priest.heal(freelancer)
    assert freelancer.health == 16

    # battle tests
    my_army = Army()
    my_army.add_units(Defender, 2)
    my_army.add_units(Healer, 1)
    my_army.add_units(Vampire, 2)
    my_army.add_units(Lancer, 2)
    my_army.add_units(Healer, 1)
    my_army.add_units(Warrior, 1)

    enemy_army = Army()
    enemy_army.add_units(Warrior, 2)
    enemy_army.add_units(Lancer, 4)
    enemy_army.add_units(Healer, 1)
    enemy_army.add_units(Defender, 2)
    enemy_army.add_units(Vampire, 3)
    enemy_army.add_units(Healer, 1)

    army_3 = Army()
    army_3.add_units(Warrior, 1)
    army_3.add_units(Lancer, 1)
    army_3.add_units(Healer, 1)
    army_3.add_units(Defender, 2)

    army_4 = Army()
    army_4.add_units(Vampire, 3)
    army_4.add_units(Warrior, 1)
    army_4.add_units(Healer, 1)
    army_4.add_units(Lancer, 2)

    army_5 = Army()
    army_5.add_units(Warrior, 10)

    army_6 = Army()
    army_6.add_units(Warrior, 6)
    army_6.add_units(Lancer, 5)

battle = Battle()

assert battle.fight(my_army, enemy_army) is False
assert battle.fight(army_3, army_4) is True
assert battle.straight_fight(army_5, army_6) is False
print("Coding complete? Let's try tests!")