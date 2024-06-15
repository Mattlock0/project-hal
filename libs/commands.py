from enum import Enum


class Command(int, Enum):
    OPEN_STRING_STREAM = 1
    SEND_IP_DATA = 2
    OPEN_STT_STREAM = 3


class MessageType(str, Enum):
    INTEGER = 'uint'
    COMMAND = 'cmd'
    STR = 'str'
