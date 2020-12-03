"""
I'm sure that many of you have some experience with computer games. But have you ever wanted to change the game so
that the characters or a game world would be more consistent with your idea of the perfect game? Probably,
yes. In this mission (and in several subsequent ones, related to it) you’ll have a chance "to sit in the developer's
chair" and create the logic of a simple game about battles. Let's start with the simple task - one-on-one duel. You
need to create the class Warrior, the instances of which will have 2 parameters - health (equal to 50 points) and
attack (equal to 5 points), and 1 property - is_alive, which can be True (if warrior's health is > 0) or False (in
the other case). In addition you have to create the second unit type - Knight, which should be the subclass of the
Warrior but have the increased attack - 7. Also you have to create a function fight(), which will initiate the duel
between 2 warriors and define the strongest of them. The duel occurs according to the following principle: Every
turn, the first warrior will hit the second and this second will lose his health in the same value as the attack of
the first warrior. After that, if he is still alive, the second warrior will do the same to the first one. The fight
ends with the death of one of them. If the first warrior is still alive (and thus the other one is not anymore),
the function should return True, False otherwise.
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


def find_winner(units):
    return units[0].is_alive


def fight(*units):
    while min(unit.health for unit in units) > 0:
        if units[0].is_alive:
            units[1].get_hit(units[0].attack)
        if units[1].is_alive:
            units[0].get_hit(units[1].attack)

    return find_winner(units)


chuck = Warrior()
bruce = Warrior()
carl = Knight()
dave = Warrior()

assert fight(chuck, bruce)
assert fight(dave, carl) is False
assert chuck.is_alive is True
assert bruce.is_alive is False
assert carl.is_alive is True
assert dave.is_alive is False