from libs.commands import Command, MessageType
import libs.formatter as formatter
import socket

SERVER_HOST = "MATTHEW-ALIEN"  # The server's hostname or IP address
PORT = 55357  # The port used by the server

END_STRING = 'end'


class Client:
    def __init__(self) -> None:
        self.host = SERVER_HOST
        self.port = PORT

    def connect(self):
        """
        connect to server
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            print('Connected to server.')
            formatter.send(s, Command.OPEN_STRING_STREAM)

            data = "", ""

            while END_STRING not in data[0]:
                data = formatter.receive(s)
