from enum import Enum


class MessageType(int, Enum):
    NULL = 0
    STRING = 1
    DICTIONARY = 2
    STT_REQUEST = 3
    STT_RESPONSE = 4
    TTS_REQUEST = 5
    TTS_RESPONSE = 6
    SP_FUNCTION = 7
    CLIENT_CONNECTION = 8
    END_CONNECTION = 100


class Message:
    def __init__(self, message_type: MessageType, message_data, tags=()) -> None:
        self.type = message_type
        self.data = message_data
        self.tags = tags
