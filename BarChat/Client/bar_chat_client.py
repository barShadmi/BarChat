import socket
import time
import threading
import pickle
from datetime import datetime
from Client import *
import cryptography
from cryptography.fernet import Fernet
from cryptography.fernet import Fernet
import rsa

IP = "127.0.0.8"
PORT = 8321
SIGN_IN = "Sign in"
FINISH_LOG_IN = "Finish_Log_In"
IS_USER = "Is User"
LOG_IN = "Log In"
FALSE = "FALSE"
READY = "Ready"
STOP_KEY = "Stop_Key"
STOP_KEY2 = "Stop_Key2"
STOP = "Stop"
MASSAGE = "Massage"
FRIEND_REQUEST = "Friend_Request"
ACCEPT_FRIEND_REQUESDT = "Accept_Friend_Request"
REMOVE_FRIEND = "Remove_Friend"
MASSAGE_FILE = "Massage_File"
INSERT_GROUP = "Insert_Group"
DELETE_GROUP = "Delete_Group"
ADD_GROUP_MEMBER = "Add_Group_Member"
SEND_DELETE_GROUP_MEMBER = "Send_Delete_Group_Member"
LEAVE_GROUP = "Leave_Group"

"""
this object handles the connection with the server
"""


class BarChatClient:
    def __init__(self):
        self.Key = Fernet.generate_key()
        self.Client = Client(IP, PORT)
        self.start_point()
        self.Client.StartConnection(self.Key)
        self.UserID = None

    def start_point(self):
        flag = False
        while not flag:
            try:
                self.Client.recvStart()
                flag = True
            except:
                print(1)

    """
    sends the server the new user info
    """

    def Sign_in(self, UserName, PassWord, FilePath):
        self.Client.recv(self.Key)
        self.Client.send(SIGN_IN, self.Key)
        time.sleep(0.001)
        self.Client.sendFile(open(FilePath, "rb").read(), self.Key)  # send Image
        time.sleep(0.001)
        self.Client.send(FilePath.split("\\")[-1][-1:-32:-1][::-1], self.Key)  # send File Name
        time.sleep(0.001)
        self.Client.send(UserName, self.Key)  # send UserName
        time.sleep(0.001)
        self.Client.send(PassWord, self.Key)  # send PassWord
        time.sleep(0.001)
        return int(self.Client.recv(self.Key))  # return UserID

    """
    sends the server the user info
    """

    def Log_in(self, UserName, PassWord):
        self.Client.recv(self.Key)
        time.sleep(0.001)
        self.Client.send(LOG_IN, self.Key)
        time.sleep(0.001)
        self.Client.send(UserName, self.Key)
        time.sleep(0.0000000000000001)
        self.Client.send(PassWord, self.Key)
        massage = self.Client.recv(self.Key)
        if massage == FALSE:
            return False
        else:
            return int(massage)

    def IsUserNameUsed(self, UserName):
        self.Client.recv(self.Key)
        time.sleep(0.001)
        self.Client.send(IS_USER, self.Key)
        time.sleep(0.001)
        self.Client.send(UserName, self.Key)
        time.sleep(0.001)
        massage = self.Client.recv(self.Key)
        if massage == FALSE:
            return False
        else:
            return True

    def Finish_Log_In(self):
        time.sleep(0.001)
        self.Client.send(FINISH_LOG_IN, self.Key)

    """
    recv the user data
    """

    def Load_Data(self, UserID):
        self.Client.recv(self.Key)
        time.sleep(0.001)
        self.Client.send(str(UserID), self.Key)
        self.Client.recv(self.Key)
        self.Client.recv(self.Key)

        UserName = self.Client.recv(self.Key)
        UserPicture = self.Client.recv(self.Key)
        Picture = self.Client.recvFile(self.Key)
        UserInfo = [UserName, UserPicture, Picture]
        massage = self.Client.recv(self.Key)
        FriendsList = []
        while massage != STOP:
            massage = self.Client.recv(self.Key)
            if massage != STOP:
                FriendID = int(massage)
                UserName = self.Client.recv(self.Key)
                UserPicture = self.Client.recv(self.Key)
                Picture = self.Client.recvFile(self.Key)
                FriendsList.append([FriendID, UserName, UserPicture, Picture])
        for f in FriendsList:
            print(f[0], f[1], f[2])
        Groups = []  # [[GroupID, GroupName, GroupPicture, PictureVal, OwnerID], [[UserID, UserName],[]],[[SenderID, Date, MassageName, Massage],[]]]
        massage = self.Client.recv(self.Key)
        while massage != STOP:
            massage = self.Client.recv(self.Key)
            if massage != STOP:
                GroupID = int(massage)
                GroupName = self.Client.recv(self.Key)
                GroupPicture = self.Client.recv(self.Key)
                PictureVal = self.Client.recvFile(self.Key)
                OwnerID = int(self.Client.recv(self.Key))

                massage = self.Client.recv(self.Key)
                MemberList = []
                while massage != STOP_KEY:
                    massage = self.Client.recv(self.Key)
                    if massage != STOP_KEY:
                        MemberID = int(massage)
                        MemberName = self.Client.recv(self.Key)
                        MemberList.append([MemberID, MemberName])
                massage = self.Client.recv(self.Key)
                MassageList = []

                while massage != STOP_KEY:
                    massage = self.Client.recv(self.Key)
                    if massage != STOP_KEY:
                        SenderID = int(massage)
                        Date = self.Client.recvPickle()
                        MassageName = self.Client.recv(self.Key)
                        MassageFile = self.Client.recvFile(self.Key)
                        MassageList.append([SenderID, Date, MassageName, MassageFile])
                Groups.append([[GroupID, GroupName, GroupPicture, PictureVal, OwnerID], MemberList, MassageList])

        Communities = []  # [[[CID, CNAME, CPIC, CPICVAL, COWN],[MemberID, MemberName] ,[[GID, GNAME],[SenderID,Date,MassageName,MassageFile]],[[],[]]]]
        massage = self.Client.recv(self.Key)
        while massage != STOP:
            massage = self.Client.recv(self.Key)
            if massage != STOP:
                CommunityID = int(massage)
                CommunityName = self.Client.recv(self.Key)
                CommunityPicture = self.Client.recv(self.Key)
                CommunityPictureVal = self.Client.recvFile(self.Key)
                OwnerID = int(self.Client.recv(self.Key))

                massage = self.Client.recv(self.Key)
                MemberList = []
                while massage != STOP_KEY:
                    massage = self.Client.recv(self.Key)
                    if massage != STOP_KEY:
                        MemberID = int(massage)
                        MemberName = self.Client.recv(self.Key)
                        MemberList.append([MemberID, MemberName])

                CommunityGroups = []
                massage = self.Client.recv(self.Key)
                while massage != STOP_KEY2:
                    massage = self.Client.recv(self.Key)
                    if massage != STOP_KEY2:
                        GroupID = int(massage)
                        GroupName = self.Client.recv(self.Key)
                        MassageList = []
                        massage = self.Client.recv(self.Key)
                        while massage != STOP_KEY:
                            massage = self.Client.recv(self.Key)
                            if massage != STOP_KEY:
                                SenderID = int(massage)
                                Date = self.Client.recvPickle()
                                MassageName = self.Client.recv(self.Key)
                                MassageFile = self.Client.recvFile(self.Key)
                                MassageList.append([SenderID, Date, MassageName, MassageFile])
                        CommunityGroups.append([[GroupID, GroupName], MassageList])
                Communities.append(
                    [[CommunityID, CommunityName, CommunityPicture, CommunityPictureVal, OwnerID], MemberList,
                     CommunityGroups])
        PublicCommunities = []
        massage = self.Client.recv(self.Key)
        while massage != STOP:
            massage = self.Client.recv(self.Key)
            if massage != STOP:
                CommunityID = int(massage)
                CommunityName = self.Client.recv(self.Key)
                PublicCommunities.append([CommunityID, CommunityName])
        return UserInfo, FriendsList, Groups, Communities, PublicCommunities

    def OpenListener(self):
        time.sleep(0.001)
        self.Client.send(READY, self.Key)
        self.serverListener = ServerListener(self.Client, self.Key)

    """
    send massage for group to server
    """

    def send_massage(self, massage, GroupID):
        try:
            self.Client.send(MASSAGE, self.Key)
            time.sleep(0.00001)
            self.Client.sendFile(massage.encode(), self.Key)
            time.sleep(0.00001)
            self.Client.send(str(GroupID), self.Key)
        except Exception as e:
            print(e)

    """
    send friend request to server
    """

    def send_friend_request(self, UserName):
        try:
            self.Client.send(FRIEND_REQUEST, self.Key)
            self.Client.send(UserName, self.Key)
        except Exception as e:
            print(e)

    """
    send accept friend request to server
    """

    def send_accept_friend_request(self, UserID):
        try:
            self.Client.send(ACCEPT_FRIEND_REQUESDT, self.Key)
            self.Client.send(str(UserID), self.Key)
        except Exception as e:
            print(e)

    """
    send massage file to server
    """

    def send_massage_file(self, GroupID, FileName):
        try:
            self.Client.send(MASSAGE_FILE, self.Key)
            self.Client.send(str(GroupID), self.Key)
            time.sleep(0.00001)
            self.Client.send(FileName.split("\\")[-1][-1:-32:-1][::-1], self.Key)
            time.sleep(0.00001)
            self.Client.sendFile(open(FileName, "rb").read(), self.Key)
            time.sleep(0.00001)

        except Exception as e:
            print(e)

    """
    send add group member to server
    """

    def send_add_group_member(self, GroupID, UsersList):
        self.Client.send(ADD_GROUP_MEMBER, self.Key)
        time.sleep(0.001)
        self.Client.send(str(GroupID), self.Key)
        for x in UsersList:
            time.sleep(0.001)
            print(x.ID)
            self.Client.send(str(x.ID), self.Key)
        time.sleep(0.001)
        self.Client.send("Stop", self.Key)

    """
    send insert group to server
    """

    def send_insert_group(self, GroupName, GroupPictureName, Picture, OwnerID, MemberList):
        self.Client.send(INSERT_GROUP, self.Key)
        time.sleep(0.001)
        self.Client.send(GroupName.split("\\")[-1][-1:-32:-1][::-1], self.Key)
        time.sleep(0.001)
        self.Client.send(GroupPictureName.split("\\")[-1][-1:-32:-1][::-1], self.Key)
        time.sleep(0.001)
        self.Client.sendFile(Picture, self.Key)
        time.sleep(0.001)
        self.Client.send(str(OwnerID), self.Key)
        for member in MemberList:
            time.sleep(0.001)
            self.Client.send(str(member.ID), self.Key)
        time.sleep(0.001)
        self.Client.send(str(self.UserID), self.Key)
        self.Client.send("Stop", self.Key)

    """
    send remove friend to server
    """

    def send_remove_friend(self, UserID):
        try:
            self.Client.send(REMOVE_FRIEND, self.Key)
            self.Client.send(str(UserID), self.Key)
        except Exception as e:
            print(e)

    """
    send delete group to server
    """

    def send_delete_group(self, GroupID):
        self.Client.send(DELETE_GROUP, self.Key)
        self.Client.send(str(GroupID), self.Key)

    """
    send delete group member to server
    """

    def send_delete_group_member(self, GroupID, UserID):
        self.Client.send(SEND_DELETE_GROUP_MEMBER, self.Key)
        time.sleep(0.001)
        self.Client.send(str(GroupID), self.Key)
        time.sleep(0.001)
        self.Client.send(str(UserID), self.Key)

    """
    send leave group to server
    """

    def send_leave_group(self, GroupID):
        self.Client.send(LEAVE_GROUP, self.Key)
        self.Client.send(str(GroupID), self.Key)

    """
    close connection with server
    """

    def Clost_Connection(self):
        self.Client.send("End", self.Key)
        time.sleep(0.001)
        self.Client.close_connenction()


class ServerListener(threading.Thread):
    def __init__(self, Client, Key):
        self.Client = Client
        self.Key = Key
        self.RUN = True
        threading.Thread.__init__(self)

    def run(self):
        while self.RUN:
            print(self.Client.recv(self.Key))


def main():
    b = BarChatClient()
    UserID = b.Log_in("Bar", "APY")
    print(UserID)
    b.UserID = UserID
    b.Finish_Log_In()
    print(b.Load_Data(UserID)[4])
    b.OpenListener()
    b.serverListener.start()


if __name__ == '__main__':
    main()
