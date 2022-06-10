import time
import socket
import pickle
import cryptography
from cryptography.fernet import Fernet
from cryptography.fernet import Fernet
import rsa


class Server:
    def __init__(self):
        pass

    def Start(self, IP, PORT):
        try:
            self.server_socket = socket.socket()
            self.server_socket.bind((IP, PORT))
            self.server_socket.listen()
        except Exception as e:
            print(e)

    def AcceptClient(self, socket):
        client_socket, client_adress = socket.accept()
        return client_socket, client_adress

    def StartConnection(self, Client, Private_Key, Public_Key):
        Client.send(pickle.dumps(Public_Key))
        data = Client.recv(4096)
        return rsa.decrypt(data, Private_Key)

    def Close_Connection(self, Client):
        Client.close()

    def sendStart(self,Client, massage):
        Client.send(massage.encode())

    def recvStart(self,Client):
        return Client.recv(4096)

    def recv(self, Client, fernet):
        return fernet.decrypt(Client.recv(4096)).decode()

    def send(self, Client, Massage, fernet):
        time.sleep(0.1)
        Client.send(fernet.encrypt(Massage.encode()))


    def recvByte(self, Client, length):
        return Client.recv(length)

    def sendByte(self, Client, Massage):
        time.sleep(0.1)
        Client.send(Massage)

    def sendPickle(self, Client, Massage):
        time.sleep(0.0000001)
        Client.send(pickle.dumps(Massage))

    def sendFile(self, Client, file, fernet):
        time.sleep(1)
        self.send(Client, str(len(file)), fernet)
        time.sleep(1)
        self.sendByte(Client, file)

    def recvFile(self, Client, fernet):
        lenght = int(self.recv(Client, fernet))  # file size
        file = self.recvByte(Client, lenght)
        while len(file) < lenght:
            file = file + self.recvByte(Client, lenght)
        return file
