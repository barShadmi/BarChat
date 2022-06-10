import socket
import time
import pickle
import cryptography
from cryptography.fernet import Fernet
from cryptography.fernet import Fernet
import rsa



"""
this object takes care of connecting to server and recv and send massages
"""
class Client:
    def __init__(self, IP_Address, PORT_Address):
        self.IP = IP_Address
        self.PORT = PORT_Address
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        flag = True
        while flag:
            try:
                self.socket.connect((self.IP, self.PORT))
                flag = False
            except:
                flag = True

    """
    create secure connection between client and server
    """
    def StartConnection(self, Key):
        PublicKey = self.socket.recv(4096)
        PublicKey = pickle.loads(PublicKey)
        self.socket.send(rsa.encrypt(Key,PublicKey))

    def close_connenction(self):
        self.socket.close()

    def sendStart(self, massage):
        self.socket.send(massage.encode())

    def recvStart(self):
        return self.socket.recv(4096)

    def send(self, Massage, Key):
        self.socket.send(Fernet(Key).encrypt(Massage.encode()))

    def recv(self, Key):
        return Fernet(Key).decrypt(self.socket.recv(4096)).decode()


    def sendByte(self, Massage):
        self.socket.send(Massage)

    def recvPickle(self):
        return pickle.loads(self.socket.recv(4096))

    def recvByte(self, Length):
        return self.socket.recv(Length)


    """
    recv file from server (FTP)
    """
    def recvFile(self, Key):
        Length = int(self.recv(Key))
        file = self.recvByte(Length)
        while len(file) < Length:
            file = file + self.recvByte(Length)
        return file

    """
    send file to server (FTP)
    """
    def sendFile(self, File, Key):
        self.send(str(len(File)), Key)
        time.sleep(0.0000001)
        self.sendByte(File)




