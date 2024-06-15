from libs.common.commands import MessageType, Command
import libs.common.formatter as MessageFormatter
import socket

LOCAL_HOST = "127.0.0.1"  # standard loopback interface address (localhost)
GENERAL_HOST = "0.0.0.0"
PORT = 55357

END_STRING = 'end'


class Server:
    def __init__(self) -> None:
        self.host = GENERAL_HOST
        self.port = PORT

    def connect(self) -> None:
        """
        opens server and accepts a connection
        :return: None
        """
        print('Opening server...')
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()

            client, addr = s.accept()
            with client:
                print(f'Connected by {addr}')
                while True:
                    data = MessageFormatter.receive(client)
                    if not data or data[0] == "":
                        break

                    if data[1] == MessageType.COMMAND and data[0] == Command.OPEN_STRING_STREAM:
                        inp = ''
                        while END_STRING not in inp.lower():
                            inp = input('[INPUT DATA] ')
                            MessageFormatter.send(client, inp)
                        break

                    else:  # default case
                        if data[1] == MessageType.STR:
                            to_send = data[0] + "LOOPBACK_ERROR"
                        else:
                            to_send = "LOOPBACK_ERROR"
                        print(f'[SENT] {to_send}')
                        MessageFormatter.send(client, to_send)
