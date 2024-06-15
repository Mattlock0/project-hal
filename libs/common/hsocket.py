# python includes
import pickle
import socket

# hal includes
from libs.common.message import Message, MessageType

SERVER_HOST = 'MATTHEW-ALIEN'  # computer name of host
GENERAL_HOST = '0.0.0.0'  # general, capture-all host for server
LOCAL_HOST = '127.0.0.1'  # standard loopback interface address (localhost)
PORT = 55357


class Socket:
    def __init__(self, is_server=False) -> None:
        self.server = is_server
        if self.server:
            self.host = GENERAL_HOST
            self.clients = []
        else:
            self.host = SERVER_HOST
            self.clients = None
        self.port = PORT
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __del__(self) -> None:
        self.socket.close()
        if self.server:
            for client in self.clients:
                client[0].close()

    def connect(self):
        print('Opening socket...')
        if self.server:
            self.connect_server()
        else:
            self.connect_client()

        print('')

    def connect_server(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen()

        conn, address = self.socket.accept()
        self.clients.append(conn, address)

        print(f'Connected by {self.clients[0][1]}')

        while True:
            client_message = self.receive()
            if client_message.type == MessageType.CLIENT_CONNECTION:
                print(f'Got an init string from client!')

                server_message = Message(MessageType.STRING, "Welcome to the server!")
                self.send(server_message)

                # then end connection
                server_message = Message(MessageType.END_CONNECTION, "Thank you.")
                self.send(server_message)
                break

    def connect_client(self):
        self.socket.connect((self.host, self.port))

        # create an init message from the client
        init_message = Message(MessageType.CLIENT_CONNECTION, 0)
        self.send(init_message)  # send connection message

        response_message = Message(MessageType.NULL, 0)

        # continue until server ends the connection
        while not response_message.type == MessageType.END_CONNECTION:
            response_message = self.receive()
            print(f'[SERVER] Received: {response_message.data}')

    def send(self, message: Message):
        if self.server:
            for client in self.clients:
                data_string = pickle.dumps(message)
                client.send(data_string)
        else:
            data_string = pickle.dumps(message)
            self.socket.send(data_string)

    def receive(self) -> Message:
        if self.server:
            # only receives from the first client right now
            data_string = self.clients[0][0].recv(4096)
            return pickle.loads(data_string)
        else:
            data_string = self.socket.recv(4096)
            return pickle.loads(data_string)
