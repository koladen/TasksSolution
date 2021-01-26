"""
Паттерн Снимок
"""

class Text:
    def __init__(self):
        self.text = ''
        self.current_font = ''

    def write(self, text):
        self.text += text

    def set_font(self, font):
        self.current_font = font

    def show(self):
        return f'[{self.current_font}]' + self.text + f'[{self.current_font}]' if self.current_font else self.text

    def restore(self, snapshot):
        self.text = snapshot.text
        self.current_font = snapshot.font


class Snapshot:
    def __init__(self, text_object):
        self.text = text_object.text
        self.font = text_object.current_font


class SavedText:
    def __init__(self):
        self.versions = []

    def save_text(self, text_object):
        self.versions.append(Snapshot(text_object))

    def get_version(self, number):
        return self.versions[number]


text = Text()
saver = SavedText()

text.write("At the very beginning ")
saver.save_text(text)
text.set_font("Arial")
saver.save_text(text)
text.write("there was nothing.")
print(text.show()) # == "[Arial]At the very beginning there was nothing.[Arial]"

text.restore(saver.get_version(0))
print(text.show()) #== "At the very beginning "