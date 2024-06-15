from socket import socket
from libs.common.commands import Command, MessageType

FORMAT = 'utf-8'
TAG_SEPARATOR = '::'


def send(s: socket, data: int | Command | str) -> None:
    """
    send a formatted message over socket

    :param socket s: The socket to send the message over
    :param int | Command | str data: The message to format and send
    """
    if type(data) is int:
        data = str(data) + TAG_SEPARATOR + MessageType.INTEGER
    elif type(data) is Command:
        data = str(int(data)) + TAG_SEPARATOR + MessageType.COMMAND
    elif type(data) is str:
        data = data + TAG_SEPARATOR + MessageType.STR
    else:
        print(f"[ERROR] Incompatible type was sent: {type(data)}")
        return

    s.send(data.encode(FORMAT))


def receive(s: socket) -> tuple:
    """
    receive a formatted message from socket

    :param socket s: The socket to receive the message from
    :return tuple: The received message and tag
    """
    data = s.recv(1024).decode(FORMAT)
    data = data.split(TAG_SEPARATOR)  # split based on tag separator

    print(f'[RECEIVED] {data[0]}')

    match data[-1]:  # checks the last value; should be the message's tag
        case MessageType.INTEGER:
            return int(''.join(data[:-1])), MessageType.INTEGER
        case MessageType.COMMAND:
            return Command(int(''.join(data[:-1]))), MessageType.COMMAND
        case MessageType.STR:
            return ''.join(data[:-1]), MessageType.STR
        case _:
            print(f'Bad data type! Received {data}')
            return str(''), MessageType.STR
