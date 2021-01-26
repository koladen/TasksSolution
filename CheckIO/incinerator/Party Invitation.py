class Friend:
    def __init__(self, name):
        self.current_invite = None
        self.name = name

    def update_invite(self, current_party):
        self.current_invite = current_party

    def show_invite(self):
        return "No party..." if self.current_invite is None else self.current_invite


class Party:
    def __init__(self, name):
        self.name = name
        self.observers = []

    def add_friend(self, friend):
        self.observers.append(friend)

    def del_friend(self, friend):
        self.observers.remove(friend)

    def send_invites(self, message):
        invite = self.name + ': ' + message
        [observer.update_invite(invite) for observer in self.observers]

party = Party("Midnight Pub")
nick = Friend("Nick")
john = Friend("John")
lucy = Friend("Lucy")
chuck = Friend("Chuck")

party.add_friend(nick)
party.add_friend(john)
party.add_friend(lucy)
party.send_invites("Friday, 9:00 PM")
party.del_friend(nick)
party.send_invites("Saturday, 10:00 AM")
party.add_friend(chuck)

print(john.show_invite()) #== "Midnight Pub: Saturday, 10:00 AM"
print(lucy.show_invite()) #== "Midnight Pub: Saturday, 10:00 AM"
print(nick.show_invite()) #== "Midnight Pub: Friday, 9:00 PM"
print(chuck.show_invite()) #== "No party..."