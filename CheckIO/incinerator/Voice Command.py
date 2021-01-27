"""
Паттерн Итератор
I made it so that the iterator could be changed to another one
"""


class ListIterator:
    def __init__(self, channels):
        self.current_channel = 1
        self.channels = channels
        self.channels_len = len(self.channels)

    def first_channel(self):
        self.current_channel = 1
        return self.channels[0]

    def last_channel(self):
        self.current_channel = self.channels_len
        return self.channels[-1]

    def turn_channel(self, n):
        self.current_channel = n
        return self.channels[n-1]

    def next_channel(self):
        if self.current_channel == self.channels_len:
            self.current_channel = 1
        else:
            self.current_channel += 1
        return self.channels[self.current_channel-1]

    def previous_channel(self):
        if self.current_channel == 1:
            self.current_channel = self.channels_len
        else:
            self.current_channel -= 1
        return self.channels[self.current_channel-1]

    def actual_channel(self):
        return self.channels[self.current_channel-1]

    def is_exist(self, channel):
        if isinstance(channel, int):
            return 'Yes' if channel <= self.channels_len else 'No'
        else:
            return 'Yes' if channel in self.channels else 'No'


class VoiceCommand:
    def __init__(self, channels):
        self.iterator = ListIterator(channels)

    def first_channel(self):
        return self.iterator.first_channel()

    def last_channel(self):
        return self.iterator.last_channel()

    def turn_channel(self, n):
        return self.iterator.turn_channel(n)

    def next_channel(self):
        return self.iterator.next_channel()

    def previous_channel(self):
        return self.iterator.previous_channel()

    def current_channel(self):
        return self.iterator.actual_channel()

    def is_exist(self, channel):
        return self.iterator.is_exist(channel)


#######################################ИНТЕРЕСНОЕ РЕШЕНИЕ###############################################################
# class VoiceCommand:
#     def __init__(self, channels):
#         self.channels = channels
#         self.current = 0  # Zero based!
#
#     def is_exist(self, channel):
#         if isinstance(channel, str):
#             return 'Yes' if channel in self.channels else 'No'
#         else:
#             return 'Yes' if 1 <= channel <= len(self.channels) else 'No'
#
#     def current_channel(self):
#         return self.channels[self.current]
#
#     def turn_channel(self, channel):
#         if self.is_exist(channel) == 'Yes':
#             self.current = channel - 1 if isinstance(channel, int) else self.channels.index(channel)
#         return self.current_channel()
#
#     def first_channel(self):
#         return self.turn_channel(1)
#
#     def last_channel(self):
#         return self.turn_channel(len(self.channels))
#
#     def previous_channel(self):
#         return self.turn_channel((self.current - 1) % len(self.channels) + 1)
#
#     def next_channel(self):
#         return self.turn_channel((self.current + 1) % len(self.channels) + 1)



##############################################РЕШЕНИЕ ЧЕРЕЗ ФУНКЦИОНАЛЬНОЕ ПР-РОВАНИЕ###################################
# from dataclasses import dataclass, field
# from functools import singledispatchmethod, wraps
# from typing import List
# Channel = str
#
#
# def _channel(method):
#     @wraps(method)
#     def _method(self, *args, **kwargs):
#         method(self, *args, **kwargs)
#         return self.channels[self.n % len(self.channels)]
#     return _method
#
#
# def _bool2text(method):
#     @wraps(method)  # Necessary to keep annotations for singledispatchmethod.
#     def _method(self, *args, **kwargs):
#         return 'Yes' if method(self, *args, **kwargs) else 'No'
#     return _method
#
#
# @dataclass
# class VoiceCommand:
#     channels: List[Channel] = field(default_factory=list)
#     n: int = 0
#
#     @_channel
#     def first_channel(self) -> Channel:
#         self.n = 0
#
#     @_channel
#     def last_channel(self) -> Channel:
#         self.n = -1
#
#     @_channel
#     def turn_channel(self, n: int) -> Channel:
#         self.n = n - 1
#
#     @_channel
#     def next_channel(self) -> Channel:
#         self.n += 1
#
#     @_channel
#     def previous_channel(self) -> Channel:
#         self.n -= 1
#
#     @_channel
#     def current_channel(self) -> Channel:
#         pass
#
#     @singledispatchmethod
#     @_bool2text
#     def is_exist(self, *args, **kwargs):
#         return False
#
#     @is_exist.register
#     @_bool2text
#     def _(self, n: int) -> str:
#         return 0 <= n - 1 < len(self.channels)
#
#     @is_exist.register
#     @_bool2text
#     def _(self, channel: Channel) -> str:
#         return channel in self.channels
#
