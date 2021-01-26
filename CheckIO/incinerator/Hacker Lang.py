import re
BIT_COUNT = 7

class HackerLanguage:
    def __init__(self):
        self.message = []

    def write(self, text):
        self.message.extend(text)

    @staticmethod
    def encode(text):
       return [bin(ord(letter))[2:] if letter.isalpha() else letter for letter in text]

    def delete(self, n):
        self.message = self.message[:(-1*n)]

    def send(self):
        return ''.join(self.encode(self.message)).replace(' ', '1000000')

    def decode(self, text):
        counter = 0
        return_text = ''
        text_len = len(text)
        while counter < text_len:
            return_text += chr(int(text[counter:counter+BIT_COUNT],2))
            counter += BIT_COUNT
        return return_text

    def decode_if_remainder_of_division_not_zero(self, text):
        text_len = len(text)
        start_of_offset = text_len - (text_len // BIT_COUNT * BIT_COUNT)
        return_text = text[:start_of_offset] + self.decode(text[start_of_offset:])
        return return_text

    def read(self, text):
        splitted_text = re.split(r'([.:!?$%@2-9 ])', text.replace('1000000', ' '))
        return_text = []
        for part_of_text in splitted_text:
            if len(part_of_text) > BIT_COUNT-1:
                if len(part_of_text) % BIT_COUNT == 0:
                    return_text.append(self.decode(part_of_text))
                else:
                    return_text.append(self.decode_if_remainder_of_division_not_zero(part_of_text))
            else:
                return_text.append(part_of_text)
        return ''.join(return_text)


#####################################РЕШЕНИЕ с maketrans###########################################

# letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
# coder = dict(zip(letters, map(lambda x: format(ord(x), 'b'), letters)))
# coder[' '] = '1000000'
# str_coder = str.maketrans(coder)
# reverse = dict(zip(map(lambda x: format(ord(x), 'b'), letters), letters))
# reverse['1000000'] = ' '
#
#
# class HackerLanguage:
#     def __init__(self):
#         self.data = ''
#
#     def write(self, text):
#         self.data += text
#
#     def delete(self, number):
#         self.data = self.data[0:-number]
#
#     def send(self):
#         return self.data.translate(str_coder)
#
#     def read(self, text):
#         i = 0
#         res = ''
#         while i < len(text):
#             try:
#                 res += reverse[text[i:i + 7]]
#                 i += 7
#             except KeyError:
#                 res += text[i]
#                 i += 1
#         return res

#############################################РЕШЕНИЕ С ОТКУСЫВАНИЕМ КУСКА ТЕКСТА#######################################
# class HackerLanguage:
#     def __init__(self):
#         self.text = ""
#
#     def write(self, text):
#         self.text += text
#
#     def delete(self, n):
#         self.text = self.text[:-n]
#
#     def send(self):
#         message = ""
#         for c in self.text:
#             if c.isalpha():
#                 message += format(ord(c), "b")
#             elif c == " ":
#                 message += "1000000"
#             else:
#                 message += c
#         return message
#
#     def read(self, text):
#         message = ""
#         while text:
#             if set(text[:7]) <= {"0", "1"}:
#                 message += chr(int(text[:7], 2)).replace("@", " ")
#                 text = text[7:]
#             else:
#                 message += text[0]
#                 text = text[1:]
#         return message