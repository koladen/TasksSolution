"""
In this mission you should create a new class Weapon(health, attack, defense, vampirism, heal_power) which will equip
your soldiers with weapons. Every weapon's object will have the parameters that will show how the soldier's
characteristics change while he uses this weapon. Assume that if the soldier doesn't have some of the characteristics
(for example, defense or vampirism), but the weapon have those, these parameters don't need to be added to the soldier.
The parameters list:
health - add to the current health and the maximum health of the soldier this modificator;
attack - add to the soldier's attack this modificator;
defense - add to the soldier's defense this modificator;
vampirism - increase the soldier’s vampirism to this number (in %. So vampirism = 20 means +20%);
heal_power - increase the amount of health which the healer restore for the allied unit.
All parameters could be positive or negative, so when a negative modificator is being added to the soldier’s stats,
they are decreasing, but none of them can be less than 0.
Let’s look at this example: vampire (basic parameters: health = 40, attack = 4, vampirism = 50%)
equip the Weapon(20, 5, 2, -60, -1). The vampire has the health and the attack, so they will change - health will grow
up to 60 (40 + 20), attack will be 9 (4 + 5). The vampire doesn’t have defense or the heal_power, so these weapon
modificators will be ignored. The weapon's vampirism modificator -60% will work as well. The standard vampirism value
is only 50%, so we’ll get -10%. But, as we said before, the parameters can’t be less than 0, so the vampirism after all
manipulations will be just 0%.
Also you should create a few standard weapons classes, which should be the subclasses of the Weapon. Here’s their list:
Sword - health +5, attack +2
Shield - health +20, attack -1, defense +2
GreatAxe - health -15, attack +5, defense -2, vampirism +10%
Katana - health -20, attack +6, defense -5, vampirism +50%
MagicWand - health +30, attack +3, heal_power +3
And finally, you should add an equip_weapon(weapon_name) method to all of the soldiers classes. It should equip the
chosen soldier with the chosen weapon.
This method also should work for the units in the army. You should hold them in the list and use it like this:
my_army.units[0].equip_weapon(Sword()) - equip the first soldier with the sword.
Notes:
While healing (both vampirism and health restored by the healer), the health can’t be greater than the maximum amount
of health for this unit (with consideration of all of the weapon's modificators).
If the heal from vampirism is float (for example 3.6, 1.1, 2.945), round it down in any case.
So 3.6 = 3, 1.1 = 1, 2.945 = 2.
Every soldier can be equipped with any number of weapons and get all their bonuses, but if he wears too much weapons
with the negative health modificator and his health is lower or equal 0 - he is as good as dead, which is actually
pretty dead in this case.
"""

from itertools import zip_longest


class Warrior:
    def __init__(self, health=50, attack=5):
        self._health = health
        self._max_health = health
        self._attack = attack
        self._weapon_list = []

    def __repr__(self):
        defense = self.__dict__.get('_defense', 0)
        vamp = self.__dict__.get('_vampirism', 0)
        return (f'{self.__class__.__name__}('
                f'H:{self._health!r},A:{self._attack!r},D:{defense!r},Vamp:{vamp!r})')

    @property
    def weapon_list(self):
        return self._weapon_list

    @weapon_list.setter
    def weapon_list(self, value):
        self._weapon_list = value

    def equip_weapon(self, weapon_name):
        for parametr, value in weapon_name.__dict__.items():
            if parametr in self.__dict__ and (self.__dict__.get(parametr, None) is not None):
                self.__dict__[parametr] = Warrior._check_max_parametr(self.__dict__[parametr],
                                                                      weapon_name.__dict__[parametr])
                if parametr == '_health':
                    self._max_health = self._health
        self._weapon_list.append(weapon_name)

    @property
    def len_weapon_list(self):
        return len(self._weapon_list)

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
    def attack(self):
        return self._attack

    @attack.setter
    def attack(self, value):
        self._attack = value

    def do_attack(self, enemy, enemy_units, ally_units, points):
        damage = Warrior._calculate_damage(enemy, points)
        enemy.health -= damage
        self._heal_ally_by_healer(ally_units)
        return damage

    def _heal_ally_by_healer(self, ally_units):
        if ally_units and isinstance(ally_units[0], Healer):
            ally_units[0].heal(self)

    @staticmethod
    def _calculate_damage(enemy, points):
        defense = enemy.__dict__.get('_defense', 0)
        if defense < points:
            damage = points - defense
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

    @staticmethod
    def _check_max_parametr(current_parametr, add_to_parametr):
        return max(0, current_parametr + add_to_parametr)


class Knight(Warrior):
    def __init__(self):
        super().__init__(attack=7)


class Rookie(Warrior):
    def __init__(self):
        super().__init__(health=30, attack=0)


class Defender(Warrior):
    def __init__(self):
        super().__init__(health=60, attack=3)
        self._defense = 2

    @property
    def defense(self):
        return self._defense

    @defense.setter
    def defense(self, value):
        self._defense = value


class Vampire(Warrior):
    def __init__(self):
        super().__init__(health=40, attack=4)
        self._vampirism = 50

    @property
    def vampirism(self):
        return self._vampirism

    @vampirism.setter
    def vampirism(self, value):
        self._vampirism = value

    def do_attack(self, enemy, enemy_units, ally_units, points):
        damage = super().do_attack(enemy, enemy_units, ally_units, points)
        self.bite(damage)
        return damage

    def bite(self, damage):
        estimate_health_points = int(damage * (self._vampirism / 100))
        self._health = super()._check_max_heal(self.health, self.max_health, estimate_health_points)


class Lancer(Warrior):
    def __init__(self):
        super().__init__(health=50, attack=6)
        self._penetration = 50

    @property
    def penetration(self):
        return self._penetration

    @penetration.setter
    def penetration(self, value):
        self._penetration = value

    def do_attack(self, enemy, enemy_units, ally_units, points):
        damage = super().do_attack(enemy, enemy_units, ally_units, points)
        self.penetrate_enemy(enemy_units, damage)
        return damage

# TODO подумать, а половину чего он должен наносить 2-му? Половину урона по первому,
# TODO или половину своего урона - защита 2-го?
    def penetrate_enemy(self, enemy_units, damage):
        if enemy_units:
            second_line_enemy_index = super()._find_alive_warrior_index(enemy_units)
            enemy_units[second_line_enemy_index].health -= int(damage * (self._penetration / 100))


class Healer(Warrior):
    def __init__(self):
        super().__init__(health=60, attack=0)
        self._heal_power = 2

    @property
    def heal_power(self):
        return self._heal_power

    @heal_power.setter
    def heal_power(self, value):
        self._heal_power = value

    def heal(self, ally_unit):
        ally_unit.health = super()._check_max_heal(ally_unit.health, ally_unit.max_health, self._heal_power)


class Weapon:
    def __init__(self, health=0, attack=0, defense=0, vampirism=0, heal_power=0):
        self._health = health
        self._attack = attack
        self._defense = defense
        self._vampirism = vampirism
        self._heal_power = heal_power

    @property
    def health(self):
        return self._health

    @property
    def attack(self):
        return self._attack

    @property
    def defense(self):
        return self._defense

    @property
    def vampirism(self):
        return self._vampirism

    @property
    def heal_power(self):
        return self._heal_power

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'H:{self._health!r},A:{self._attack!r},D:{self._defense!r},Vamp:{self._vampirism!r},'
                f'HPow:{self._heal_power!r})')


class Sword(Weapon):
    def __init__(self):
        super().__init__(health=5, attack=2)


class Shield(Weapon):
    def __init__(self):
        super().__init__(health=20, attack=-1, defense=2)


class GreatAxe(Weapon):
    def __init__(self):
        super().__init__(health=-15, attack=5, defense=-2, vampirism=10)


class Katana(Weapon):
    def __init__(self):
        super().__init__(health=-20, attack=6, defense=-5, vampirism=50)


class MagicWand(Weapon):
    def __init__(self):
        super().__init__(health=30, attack=3, heal_power=3)


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

if __name__ == '__main__':
    # These "asserts" using only for self-checking and not necessary for auto-testing

    ogre = Warrior()
    lancelot = Knight()
    richard = Defender()
    eric = Vampire()
    freelancer = Lancer()
    priest = Healer()

    sword = Sword()
    shield = Shield()
    axe = GreatAxe()
    katana = Katana()
    wand = MagicWand()
    super_weapon = Weapon(50, 10, 5, 150, 8)

    ogre.equip_weapon(sword)
    ogre.equip_weapon(shield)
    ogre.equip_weapon(super_weapon)
    lancelot.equip_weapon(super_weapon)
    richard.equip_weapon(shield)
    eric.equip_weapon(super_weapon)
    freelancer.equip_weapon(axe)
    freelancer.equip_weapon(katana)
    priest.equip_weapon(wand)
    priest.equip_weapon(shield)

    assert ogre.health == 125
    assert lancelot.attack == 17
    assert richard.defense == 4
    assert eric.vampirism == 200
    assert freelancer.health == 15
    assert priest.heal_power == 5

    assert fight(ogre, eric) is False
    assert fight(priest, richard) is False
    assert fight(lancelot, freelancer) is True

    my_army = Army()
    my_army.add_units(Knight, 1)
    my_army.add_units(Lancer, 1)

    enemy_army = Army()
    enemy_army.add_units(Vampire, 1)
    enemy_army.add_units(Healer, 1)

    my_army.units[0].equip_weapon(axe)
    my_army.units[1].equip_weapon(super_weapon)

    enemy_army.units[0].equip_weapon(katana)
    enemy_army.units[1].equip_weapon(wand)

    battle = Battle()

    assert battle.fight(my_army, enemy_army) is True
print("Coding complete? Let's try tests!")