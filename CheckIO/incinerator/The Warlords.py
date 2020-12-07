"""
In this mission you should add a new class Warlord(), which should be the subclass of the Warrior class and have the
next characteristics:
health = 100
attack = 4
defense = 2

Also, when the Warlord is included in any of the armies, that particular army gets the new move_units() method which
allows to rearrange the units of that army for the better battle result. The rearrangement is done not only before the
battle, but during the battle too, each time the allied units die. The rules for the rearrangement are as follow:
If there are Lancers in the army, they should be placed in front of everyone else.
If there is a Healer in the army, he should be placed right after the first soldier to heal him during the fight. If the
 number of Healers is > 1, all of them should be placed right behind the first Healer.
If there are no more Lancers in the army, but there are other soldiers who can deal damage, they also should be placed
in first position, and the Healer should stay in the 2nd row (if army still has Healers).
Warlord should always stay way in the back to look over the battle and rearrange the soldiers when it's needed.
Every army can have no more than 1 Warlord.
If the army doesn’t have a Warlord, it can’t use the move_units() method.
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


class Warlord(Warrior):
    def __init__(self):
        super().__init__(health=100, attack=4)
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
        self._warlord_count = 0

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, value):
        self._units = value

    def add_units(self, fighter, count):
        for _ in range(count):
            unit = fighter()
            if isinstance(unit, Warlord):
                if self.check_only_one_warlord():
                    self._units.append(unit)
                    self._warlord_count = 1
            else:
                self._units.append(unit)

    @property
    def get_unit(self):
        return self._units.pop(0)

    @property
    def len_army(self):
        return len(self._units)

    @staticmethod
    def sort_order(class_name):
        order = {Lancer: 0, Defender: 1, Vampire: 1, Warrior: 1, Knight: 1, Rookie: 2, Healer: 3, Warlord: 9}
        return order.get(class_name.__class__, 1)

    def move_units(self):
        if self._warlord_count:
            self._units.sort(key=Army.sort_order)
            if not isinstance(self._units[0].__class__, Healer):
                first_healer_index = self._find_first_healer_index()
                if first_healer_index is not None:
                    last_healer_index = self._find_last_healer_index(first_healer_index+1)
                    not_healers_part = self._units[1:first_healer_index]
                    self._units = self._units[0:1] + self._units[first_healer_index:last_healer_index] + \
                                  not_healers_part + self._units[last_healer_index:]

    def _find_first_healer_index(self):
        for index, unit in enumerate(self._units):
            if unit.__class__ is Healer:
                return index

    def _find_last_healer_index(self, start_index):
        for i in range(start_index, self.len_army):
            if self._units[i].__class__ is not Healer:
                return i

    def check_only_one_warlord(self):
        return self._warlord_count == 0

    def __repr__(self):
        composition = ''
        for unit in self._units[:-1]:
            composition += str(unit) + ', '
        composition = composition + str(self._units[-1]) if self._units else ''
        return (f'{self.__class__.__name__}('
                f':{composition})')

class Battle:
    def __init__(self):
        pass

    @staticmethod
    def remove_dead_units(army_1, army_2):
        army_1.units = [unit for unit in army_1.units if unit.is_alive]
        army_2.units = [unit for unit in army_2.units if unit.is_alive]
        if army_1.units:
            army_1.move_units()
        if army_2.units:
            army_2.move_units()

    @staticmethod
    def fight(*armyes):
        first_fighter = armyes[0].get_unit
        second_fighter = armyes[1].get_unit
        while first_fighter.is_alive and second_fighter.is_alive:
            winner = Battle.fight_units(armyes[0], armyes[1], first_fighter, second_fighter)
            if armyes[1].len_army > 0:
                second_fighter = armyes[1].get_unit
            if armyes[0].len_army > 0:
                first_fighter = armyes[0].get_unit
        return first_fighter.is_alive and armyes[1].len_army == 0

    @staticmethod
    def straight_fight(army_1, army_2):
        while min(army_1.len_army, army_2.len_army) > 0:
            Battle.remove_dead_units(army_1, army_2)
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
        army1.units.insert(0, units[0])
        army2.units.insert(0, units[1])
        Battle.remove_dead_units(army1, army2)
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


army_1 = Army()
army_2 = Army()
army_1.add_units(Warrior, 2)
army_1.add_units(Lancer, 3)
army_1.add_units(Defender, 1)
army_1.add_units(Warlord, 4)
army_2.add_units(Warlord, 1)
army_2.add_units(Vampire, 1)
army_2.add_units(Rookie, 1)
army_2.add_units(Knight, 1)
army_1.units[0].equip_weapon(Sword())
army_2.units[0].equip_weapon(Shield())
army_1.move_units()
army_2.move_units()
battle = Battle()
print(battle.fight(army_1, army_2))