"""
The modern world is filled with means of communication - the social networks, messengers, phone calls, SMS etc. But
sometimes in every communication channel a flaw can be detected and in the moments like that you think to yourself:
"I should create my own messenger which won’t have problems like this one".
In this mission you’ll get your chance.
Your task is to create a Chat class which could help a Human(name) and Robot(serial_number) to make a conversation. This
 class should have a few methods:
connect_human() - connects human to the chat.
connect_robot() - connects robot to the chat.
show_human_dialogue() - shows the dialog as the human sees it - as simple text.
show_robot_dialogue() - shows the dialog as the robot perceives it - as the set of ones and zeroes. To simplify the
task, just replace every vowel ('aeiouAEIOU') with "0", and the rest symbols (consonants, white spaces and special signs
 like ",", "!", etc.) with "1".
Dialog for the human should be displayed like this:
(human name) said: message text
(robot serial number): message text
For the robot:
(human name) said: 11100100011
(robot serial number) said: 100011100101
Interlocutors should have a send() method for sending messages to the dialog.
In this mission you could use the Mediator design pattern.
"""

VOWELS = "aeiou"


class Chat:
    def __init__(self):
        self.dialogue = []
        self.participants = set()

    def connect_human(self, participant):
        self._add_participant(participant)

    def connect_robot(self, participant):
        self._add_participant(participant)

    def _add_participant(self, participant):
        participant.chat = self
        self.participants.add(participant)

    def show_human_dialogue(self):
        return_message = "".join([message[0].name + ' said: ' + message[1] for message in self.dialogue])
        return return_message

    def show_robot_dialogue(self):
        return_message = "".join([message[0].name + ' said: ' + ''.join(['0' if i.lower() in VOWELS else '1' for i in message[1]]) for message in self.dialogue])
        return return_message


class Human:
    def __init__(self, name):
        self.name = name

    def send(self, message):
        self.chat.dialogue.append((self, message))


class Robot:
    def __init__(self, name):
        self.name = name

    def send(self, message):
        self.chat.dialogue.append((self, message))

chat = Chat()
karl = Human("Karl")
bot = Robot("R2D2")
chat.connect_human(karl)
chat.connect_robot(bot)
karl.send("Hi! What's new?")
bot.send("Hello, human. Could we speak later about it?")
assert chat.show_human_dialogue() == """Karl said: Hi! What's new?R2D2 said: Hello, human. Could we speak later about it?"""
assert chat.show_robot_dialogue() == """Karl said: 101111011111011R2D2 said: 10110111010111100111101110011101011010011011"""