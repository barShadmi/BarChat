import socket
import hashlib
import time
from mysql_interface import *
from Server import *
import threading
from datetime import datetime
import cryptography
from cryptography.fernet import Fernet
from cryptography.fernet import Fernet
import rsa

PUBLIC_KEY, PRIVATE_KEY = rsa.newkeys(512)  # Public and Private permanent Keys with Asymmetric Encryption Method
IP = "0.0.0.0"
PORT = 8321
SIGN_IN = "Sign in"
LOG_IN = "Log In"
IS_USER = "Is User"
READY = "Ready"
TRUE = "TRUE"
FALSE = "FALSE"
STOP_KEY = "Stop_Key"
FINISH_LOG_IN = "Finish_Log_In"
STOP = "Stop"
STOP_KEY2 = "Stop_Key2"
TEXT = "Text"
MASSAGE = "Massage"
FRIEND_REQUEST = "Friend_Request"
ACCEPT_FRIEND_REQUESDT = "Accept_Friend_Request"
REMOVE_FRIEND = "Remove_Friend"
MASSAGE_FILE = "Massage_File"
INSERT_GROUP = "Insert_Group"
DELETE_GROUP = "Delete_Group"
ADD_GROUP_MEMBER = "Add_Group_Member"
ADD_NEW_GROUP_Member = "Add_New_Group_Member"
SEND_DELETE_GROUP_MEMBER = "Send_Delete_Group_Member"
LEAVE_GROUP = "Leave_Group"


lock = threading.Lock()
lock2 = threading.Lock()
condition = threading.Condition()

Massages = {}
Online = []
Waiting = []


class BarChatServer:
    def __init__(self):
        self.Server = Server()
        self.Server.Start(IP, PORT)
        self.RUN = True

    def run(self):
        while self.RUN:
            try:
                client_socket, client_adress = self.Server.AcceptClient(self.Server.server_socket)
                ClientListener(client_socket, client_adress).start()
            except Exception as e:
                pass


class Sender(threading.Thread):
    def __init__(self, ID, Client, fernet, server):
        global Massages
        self.db = database("localhost", "bar", "barpass", "yessdoluahd")
        self.Server = server
        self.ID = ID
        self.Client = Client
        self.fernet = fernet
        self.RUN = True
        Massages[self.ID] = [threading.Condition(), []]
        threading.Thread.__init__(self)

    def run(self):
        global Massages
        while self.RUN:
            Massages[self.ID][0].acquire()
            if Massages[self.ID][1] == []:
                Massages[self.ID][0].wait()
            m = Massages[self.ID][1].pop()
            Massages[self.ID][0].release()
            if m == ["Finish"]:
                Massages.pop(self.ID)
                self.RUN = False
            self.db = database("localhost", "bar", "barpass", "yessdoluahd")
            if len(m) == 5 and m[2] == MASSAGE:
                time.sleep(0.0000001)
                self.Server.send(self.Client, MASSAGE, self.fernet)
                time.sleep(0.0000001)
                self.Server.send(self.Client, str(m[0]), self.fernet)
                time.sleep(0.0000001)
                self.Server.sendFile(self.Client, m[1], self.fernet)
                time.sleep(0.0000001)
                self.Server.send(self.Client, str(m[4]), self.fernet)
                time.sleep(0.0001)
                self.Server.sendPickle(self.Client, m[3])

            if len(m) == 5 and m[0] == FRIEND_REQUEST:
                time.sleep(0.00001)
                self.Server.send(self.Client, FRIEND_REQUEST, self.fernet)
                time.sleep(0.00001)
                self.Server.send(self.Client, str(m[1]), self.fernet)
                time.sleep(0.00001)
                self.Server.send(self.Client, m[2], self.fernet)
                time.sleep(0.00001)
                self.Server.send(self.Client, m[3], self.fernet)
                time.sleep(0.001)
                self.Server.sendFile(self.Client, m[4], self.fernet)

            if len(m) == 5 and m[0] == ACCEPT_FRIEND_REQUESDT:
                time.sleep(0.00001)
                self.Server.send(self.Client, ACCEPT_FRIEND_REQUESDT, self.fernet)
                time.sleep(0.00001)
                self.Server.send(self.Client, str(m[1]), self.fernet)
                time.sleep(0.00001)
                self.Server.send(self.Client, m[2], self.fernet)
                time.sleep(0.00001)
                self.Server.send(self.Client, m[3], self.fernet)
                time.sleep(0.0001)
                self.Server.sendFile(self.Client, m[4], self.fernet)

            if len(m) == 2 and m[0] == REMOVE_FRIEND:
                time.sleep(0.00001)
                self.Server.send(self.Client, REMOVE_FRIEND, self.fernet)
                time.sleep(0.00001)
                self.Server.send(self.Client, str(m[1]), self.fernet)

            if len(m) == 6 and m[0] == MASSAGE_FILE:
                time.sleep(0.00001)
                self.Server.send(self.Client, MASSAGE_FILE, self.fernet)
                time.sleep(0.00001)
                self.Server.send(self.Client, str(m[1]), self.fernet)
                time.sleep(0.00001)
                self.Server.send(self.Client, str(m[2]), self.fernet)
                time.sleep(0.00001)
                self.Server.sendPickle(self.Client, m[3])
                time.sleep(0.00001)
                self.Server.send(self.Client, m[4], self.fernet)
                time.sleep(0.001)
                self.Server.sendFile(self.Client, m[5], self.fernet)

            if len(m) == 7 and m[0] == INSERT_GROUP:
                time.sleep(0.00001)
                self.Server.send(self.Client, INSERT_GROUP, self.fernet)
                time.sleep(0.00001)
                self.Server.send(self.Client, str(m[1]), self.fernet)
                time.sleep(0.00001)
                self.Server.send(self.Client, m[2], self.fernet)
                time.sleep(0.00001)
                self.Server.send(self.Client, m[3], self.fernet)
                time.sleep(0.0001)
                self.Server.sendFile(self.Client, m[4], self.fernet)
                time.sleep(0.00001)
                self.Server.send(self.Client, str(m[5]), self.fernet)
                for user in m[6]:
                    time.sleep(0.00001)
                    self.Server.send(self.Client, str(user[0]), self.fernet)
                    time.sleep(0.00001)
                    self.Server.send(self.Client, user[1], self.fernet)
                time.sleep(0.00001)
                self.Server.send(self.Client, "Stop", self.fernet)

            if len(m) == 2 and m[0] == DELETE_GROUP:
                time.sleep(0.00001)
                self.Server.send(self.Client, DELETE_GROUP, self.fernet)
                time.sleep(0.00001)
                self.Server.send(self.Client, str(m[1]), self.fernet)

            if len(m) == 3 and m[0] == ADD_GROUP_MEMBER:
                time.sleep(0.00001)
                self.Server.send(self.Client, ADD_GROUP_MEMBER, self.fernet)
                time.sleep(0.00001)
                self.Server.send(self.Client, str(m[1]), self.fernet)
                for user in m[2]:
                    time.sleep(0.00001)
                    self.Server.send(self.Client, str(user[0]), self.fernet)
                    time.sleep(0.00001)
                    self.Server.send(self.Client, user[1], self.fernet)
                time.sleep(0.00001)
                self.Server.send(self.Client, "Stop", self.fernet)

            if len(m) == 3 and m[0] == ADD_NEW_GROUP_Member:
                time.sleep(0.00001)
                self.Server.send(self.Client, ADD_NEW_GROUP_Member, self.fernet)
                time.sleep(0.00001)
                self.Server.send(self.Client, str(m[1]), self.fernet)
                temp = self.db.GetGroupInfo(m[1])
                self.Server.send(self.Client, str(temp[3]), self.fernet)
                time.sleep(0.00001)
                self.Server.send(self.Client, temp[0], self.fernet)
                self.Server.send(self.Client, temp[1], self.fernet)
                time.sleep(0.00001)
                self.Server.sendFile(self.Client, temp[2], self.fernet)
                time.sleep(0.00001)

                for user in m[2]:
                    time.sleep(0.0000001)
                    self.Server.send(self.Client, str(user[0]), self.fernet)
                    time.sleep(0.0000001)
                    self.Server.send(self.Client, user[1], self.fernet)
                time.sleep(0.0000001)
                self.Server.send(self.Client, "Stop", self.fernet)
                time.sleep(0.0001)

                for Massage in self.db.GetGroupMassages(m[1]):
                    if len(Massage) == 3:
                        time.sleep(0.0000001)
                        self.Server.send(self.Client, str(Massage[0]), self.fernet) #senderid
                        time.sleep(0.0001)
                        self.Server.sendPickle(self.Client, Massage[1]) # date
                        time.sleep(0.0001)
                        self.Server.send(self.Client, TEXT, self.fernet) # massage name
                        time.sleep(0.001)
                        self.Server.sendFile(self.Client, Massage[2], self.fernet)  # file
                    else:
                        self.Server.send(self.Client, str(Massage[0]), self.fernet)  # senderid
                        time.sleep(0.0001)
                        self.Server.sendPickle(self.Client, Massage[1])  # date
                        time.sleep(0.0001)
                        self.Server.send(self.Client, Massage[3], self.fernet)  # massage name
                        time.sleep(0.001)
                        self.Server.sendFile(self.Client, Massage[2], self.fernet)  # file
                    time.sleep(0.0001)
                self.Server.send(self.Client, "Stop", self.fernet)

            if len(m) == 3 and m[0] == SEND_DELETE_GROUP_MEMBER:
                time.sleep(0.0000001)
                self.Server.send(self.Client, SEND_DELETE_GROUP_MEMBER, self.fernet)
                time.sleep(0.0000001)
                self.Server.send(self.Client, str(m[1]), self.fernet)
                time.sleep(0.0000001)
                self.Server.send(self.Client, str(m[2]), self.fernet)

            if len(m) == 3 and m[0] == LEAVE_GROUP:
                time.sleep(0.0000001)
                self.Server.send(self.Client, LEAVE_GROUP, self.fernet)
                time.sleep(0.0000001)
                self.Server.send(self.Client, str(m[1]), self.fernet)
                time.sleep(0.0000001)
                self.Server.send(self.Client, str(m[2]), self.fernet)

class ClientListener(threading.Thread):
    def __init__(self, Client, Address):
        self.db = database("localhost", "bar", "barpass", "yessdoluahd")
        self.Client = Client
        self.Address = Address
        self.Server = Server()
        self.RUN = True
        threading.Thread.__init__(self)

    def run(self):
        self.Start_Connection()
        self.fernet = Fernet(self.Server.StartConnection(self.Client, PRIVATE_KEY, PUBLIC_KEY))
        self.Starting_Point()
        flag = self.Load_Data()
        if flag:
            self.Add_To_Online()

    def Add_To_Online(self):
        global Online, Massages, Waiting
        massage = self.Server.recv(self.Client, self.fernet)
        if massage == READY:
            try:
                Waiting.remove(self.UserID)
            except Exception as e:
                print(e)
            Online.append((self.UserID, self.Client))
            self.sender = Sender(self.UserID, self.Client, self.fernet, self.Server)
            self.sender.start()
            print(f"{self.UserID} has been connected")
            self.Recv_Requests()

    def Recv_Requests(self):
        global Massages, Online
        while self.RUN:
            try:
                mass = self.Server.recv(self.Client, self.fernet)
            except:
                print(f"{self.UserID} disconnected")
                Online.remove((self.UserID, self.Client))
                Massages[self.UserID][0].acquire()
                Massages[self.UserID][1].append(["Finish"])
                Massages[self.UserID][0].notify()
                Massages[self.UserID][0].release()
                self.RUN = False
                self.Server.Close_Connection(self.Client)
                break
            if mass == "End":
                print(f"{self.UserID} disconnected")
                Online.remove((self.UserID, self.Client))
                Massages[self.UserID][0].acquire()
                Massages[self.UserID][1].append(["Finish"])
                Massages[self.UserID][0].notify()
                Massages[self.UserID][0].release()
                self.RUN = False
                self.Server.Close_Connection(self.Client)
                break
            print(mass)
            if mass == MASSAGE:
                massage = self.Server.recvFile(self.Client, self.fernet)
                GroupID = self.Server.recv(self.Client, self.fernet)
                Date = datetime.now()
                lock.acquire()
                try:
                    self.db.InsertMassage(GroupID, self.UserID, massage, Date)
                except Exception as e:
                    print(e)
                finally:
                    lock.release()
                for Member in self.db.GetGroupMembers(GroupID):
                    if self.IsOnline(Member):
                        Massages[Member][0].acquire()
                        Massages[Member][1].append([GroupID, massage, MASSAGE, Date, self.UserID])
                        Massages[Member][0].notify()
                        Massages[Member][0].release()
            if mass == FRIEND_REQUEST:
                UserName = self.Server.recv(self.Client, self.fernet)
                if self.db.IsUserName(UserName):
                    UserID = self.db.GetUserID(UserName)
                    if UserID in Massages.keys() and UserID != self.UserID:
                        Massages[UserID][0].acquire()
                        Massages[UserID][1].append([FRIEND_REQUEST, self.UserID, self.db.GetUserName(self.UserID),
                                                    self.db.GetUserPicture(self.UserID),
                                                    self.db.GetFile(int(self.db.GetUserPictureID(self.UserID)))]
                                                   )
                        Massages[UserID][0].notify()
                        Massages[UserID][0].release()
            if mass == ACCEPT_FRIEND_REQUESDT:
                UserID = int(self.Server.recv(self.Client, self.fernet))
                lock.acquire()
                try:
                    self.db.InsertFriends(UserID, self.UserID)
                except Exception as e:
                    print(e)
                finally:
                    lock.release()
                if UserID in Massages.keys():
                    Massages[UserID][0].acquire()
                    Massages[UserID][1].append([ACCEPT_FRIEND_REQUESDT, self.UserID, self.db.GetUserName(self.UserID),
                                                self.db.GetUserPicture(self.UserID),
                                                self.db.GetFile(int(self.db.GetUserPictureID(self.UserID)))])
                    Massages[UserID][0].notify()
                    Massages[UserID][0].release()
            if mass == REMOVE_FRIEND:
                UserID = int(self.Server.recv(self.Client, self.fernet))
                lock.acquire()
                try:
                    self.db.DeleteFriends(UserID, self.UserID)
                except Exception as e:
                    print(e)
                finally:
                    lock.release()
                if UserID in Massages.keys():
                    Massages[UserID][0].acquire()
                    Massages[UserID][1].append([REMOVE_FRIEND, self.UserID])
                    Massages[UserID][0].notify()
                    Massages[UserID][0].release()
            if mass == MASSAGE_FILE:
                GroupID = int(self.Server.recv(self.Client, self.fernet))
                FileName = self.Server.recv(self.Client, self.fernet)
                File = self.Server.recvFile(self.Client, self.fernet)
                Date = datetime.now()
                lock.acquire()
                try:
                    self.db.InsertMassageFile(GroupID, self.UserID, Date, FileName, File)
                except Exception as e:
                    print(e)
                finally:
                    lock.release()
                for Member in self.db.GetGroupMembers(GroupID):
                    if self.IsOnline(Member):
                        Massages[Member][0].acquire()
                        Massages[Member][1].append([MASSAGE_FILE, GroupID, self.UserID, Date, FileName, File])
                        Massages[Member][0].notify()
                        Massages[Member][0].release()

            if mass == INSERT_GROUP:
                GroupName = self.Server.recv(self.Client, self.fernet)
                GroupPictureName = self.Server.recv(self.Client, self.fernet)
                GroupPicture = self.Server.recvFile(self.Client, self.fernet)
                OwnerID = int(self.Server.recv(self.Client, self.fernet))
                Members = []
                m = self.Server.recv(self.Client, self.fernet)
                while m != "Stop":
                    Members.append(int(m))
                    m = self.Server.recv(self.Client, self.fernet)
                lock.acquire()
                try:
                    GroupID = int(self.db.InsertGroup(GroupName, GroupPictureName, GroupPicture, OwnerID))
                    for member in Members:
                        self.db.InsertGroupMember(GroupID, member)
                except Exception as e:
                    print(e)
                finally:
                    lock.release()
                tempL = []
                for user in self.db.GetGroupMembers(GroupID):
                    tempL.append([user, self.db.GetUserName(user)])
                for Member in self.db.GetGroupMembers(GroupID):
                    if self.IsOnline(Member):
                        Massages[Member][0].acquire()
                        Massages[Member][1].append(
                            [INSERT_GROUP, GroupID, GroupName, GroupPictureName, GroupPicture, OwnerID, tempL])
                        Massages[Member][0].notify()
                        Massages[Member][0].release()


            if mass == DELETE_GROUP:
                GroupID = int(self.Server.recv(self.Client, self.fernet))
                x = self.db.GetGroupMembers(GroupID)
                lock.acquire()
                try:
                    self.db.DeleteGroupChat(GroupID)
                except Exception as e:
                    print(e)
                finally:
                    lock.release()
                    for Member in x:
                        if self.IsOnline(Member):
                            Massages[Member][0].acquire()
                            Massages[Member][1].append([DELETE_GROUP, GroupID])
                            Massages[Member][0].notify()
                            Massages[Member][0].release()

            if mass == ADD_GROUP_MEMBER:
                GroupID = int(self.Server.recv(self.Client, self.fernet))
                Members = []
                m = self.Server.recv(self.Client, self.fernet)
                while m != "Stop":
                    Members.append(int(m))
                    m = self.Server.recv(self.Client, self.fernet)
                lock.acquire()
                try:
                    for member in Members:
                        self.db.InsertGroupMember(GroupID, member)
                except Exception as e:
                    print(e)
                finally:
                    lock.release()

                tempL = []
                for x in Members:
                    tempL.append([x, self.db.GetUserName(x)])
                for oldmember in self.db.GetGroupMembers(GroupID):
                    if oldmember not in Members and self.IsOnline(oldmember):
                        Massages[oldmember][0].acquire()
                        Massages[oldmember][1].append([ADD_GROUP_MEMBER, GroupID, tempL])
                        Massages[oldmember][0].notify()
                        Massages[oldmember][0].release()
                tempL = []
                for x in self.db.GetGroupMembers(GroupID):
                    tempL.append([x, self.db.GetUserName(x)])
                for member in Members:
                    if self.IsOnline(member):
                        Massages[member][0].acquire()
                        Massages[member][1].append([ADD_NEW_GROUP_Member, GroupID, tempL])
                        Massages[member][0].notify()
                        Massages[member][0].release()
            if mass == SEND_DELETE_GROUP_MEMBER:
                GroupID = int(self.Server.recv(self.Client, self.fernet))
                UserID = int(self.Server.recv(self.Client, self.fernet))
                l = self.db.GetGroupMembers(GroupID)
                lock.acquire()
                try:
                    self.db.DeleteGroupMember(GroupID, UserID)
                except Exception as e:
                    print(e)
                finally:
                    lock.release()
                for member in l:
                    if self.IsOnline(member):
                        Massages[member][0].acquire()
                        Massages[member][1].append([SEND_DELETE_GROUP_MEMBER, GroupID, UserID])
                        Massages[member][0].notify()
                        Massages[member][0].release()

            if mass == LEAVE_GROUP:
                GroupID = int(self.Server.recv(self.Client, self.fernet))
                l = self.db.GetGroupMembers(GroupID)
                lock.acquire()
                try:
                    self.db.DeleteGroupMember(GroupID, self.UserID)
                except Exception as e:
                    print(e)
                finally:
                    lock.release()
                for member in l:
                    print(member)
                    if self.IsOnline(member):
                        Massages[member][0].acquire()
                        Massages[member][1].append([LEAVE_GROUP, GroupID, self.UserID])
                        Massages[member][0].notify()
                        Massages[member][0].release()



    def IsOnline(self, UserID):
        global Online
        for OnlineUser in Online:
            if UserID == OnlineUser[0]:
                return True
        return False

    def Start_Connection(self):
        flag = False
        while not flag:
            try:
                self.Server.sendStart(self.Client, READY)
                flag = True
            except Exception as e:
                print(e)

    def Starting_Point(self):
        while self.RUN:
            self.Server.send(self.Client, READY, self.fernet)
            massage = self.Server.recv(self.Client, self.fernet)
            if massage == SIGN_IN:
                self.Sign_in()
            elif massage == LOG_IN:
                self.Log_In()
            elif massage == IS_USER:
                self.IsUserNameUsed()
            elif massage == FINISH_LOG_IN:
                break
            massage = ""

    def Load_Data(self):
        try:
            print(1)
            self.Server.send(self.Client, READY, self.fernet)
            time.sleep(0.0000001)
            UserID = int(self.Server.recv(self.Client, self.fernet))
            self.UserID = UserID
            UserInfo = self.db.GetUser(UserID)
            time.sleep(0.0000001)
            UserName, UserPicture, Picture = UserInfo[0]
            self.Server.send(self.Client, READY, self.fernet)
            self.Load_User(UserName, UserPicture, Picture)
            FriendList, GroupList, CommunityList = UserInfo[1], UserInfo[2], UserInfo[3]
            tempList = []
            for UserID in FriendList:
                User = self.db.GetUser(UserID)[0]
                tempList.append([UserID, User[0], User[1], User[2]])
            self.Load_Friends(tempList)
            tempList = []
            for GroupID in GroupList:
                GroupInfo = self.db.GetGroupInfo(GroupID)
                GroupName = GroupInfo[0]
                GroupPicture = GroupInfo[1]
                PictureVal = GroupInfo[2]
                OwnerID = GroupInfo[3]
                GroupInfo = [GroupID, GroupName, GroupPicture, PictureVal, OwnerID]
                MembersInfo = []
                for Member in self.db.GetGroupMembers(GroupID):
                    MembersInfo.append([Member, self.db.GetUserName(Member)])
                Massages = []
                for Massage in self.db.GetGroupMassages(GroupID):
                    if len(Massage) == 3:
                        SenderID = Massage[0]
                        Date = Massage[1]
                        MassageName = TEXT
                        File = Massage[2]
                    else:
                        SenderID = Massage[0]
                        Date = Massage[1]
                        MassageName = Massage[3]
                        File = Massage[2]
                    Massages.append([SenderID, Date, MassageName, File])
                tempList.append([[GroupID, GroupName, GroupPicture, PictureVal, OwnerID], MembersInfo, Massages])
            self.Load_Groups(tempList)
            tempList = []
            for CommunityID in CommunityList:
                CommunityInfo = self.db.GetCommunityInfo(CommunityID)
                CommunityName = CommunityInfo[0][0]
                OwnerID = CommunityInfo[0][1]
                CommunityPicture = CommunityInfo[0][2]
                CommunityPictureVal = CommunityInfo[0][3]
                CommunityGroups = []
                CommunityMembers = []
                for CommunityGroupID in CommunityInfo[1]:
                    Massages = []
                    for Massage in self.db.GetGroupMassages(CommunityGroupID):
                        if len(Massage) == 3:
                            SenderID = Massage[0]
                            Date = Massage[1]
                            MassageName = TEXT
                            File = Massage[2]
                        else:
                            SenderID = Massage[0]
                            Date = Massage[1]
                            MassageName = Massage[3]
                            File = Massage[2]
                        Massages.append([SenderID, Date, MassageName, File])
                    CommunityGroups.append([CommunityGroupID, self.db.GetGroupName(CommunityGroupID), Massages])
                for CommunityMemberID in CommunityInfo[2]:
                    CommunityMembers.append([CommunityMemberID, self.db.GetUserName(CommunityMemberID)])
                tempList.append(
                    [[CommunityID, CommunityName, CommunityPicture, CommunityPictureVal, OwnerID], CommunityMembers,
                     CommunityGroups])
            self.Load_Communities(tempList)
            self.Load_Public_Communities(self.db.GetCommunities())
        except Exception as e:
            print(e)
            Waiting.remove(self.UserID)
            return False
        return True

    def Load_User(self, UserName, UserPicture, Picture):
        time.sleep(0.000001)
        self.Server.send(self.Client, UserName, self.fernet)
        time.sleep(0.000001)
        self.Server.send(self.Client, UserPicture, self.fernet)
        time.sleep(0.001)
        self.Server.sendFile(self.Client, Picture, self.fernet)

    def Load_Friends(self, FriendList):
        time.sleep(0.0000001)
        self.Server.send(self.Client, READY, self.fernet)
        for friend in FriendList:
            time.sleep(0.0000001)
            self.Server.send(self.Client, str(friend[0]), self.fernet)
            self.Load_User(friend[1], friend[2], friend[3])
        time.sleep(0.0000001)
        self.Server.send(self.Client, STOP, self.fernet)

    def Load_Groups(self, GroupList):
        self.Server.send(self.Client, READY, self.fernet)
        time.sleep(0.0000000000000001)
        for Group in GroupList:
            time.sleep(0.0000001)
            self.Server.send(self.Client, str(Group[0][0]), self.fernet)
            time.sleep(0.0000001)
            self.Server.send(self.Client, Group[0][1], self.fernet)
            time.sleep(0.0000001)
            self.Server.send(self.Client, Group[0][2], self.fernet)
            time.sleep(0.0000001)
            self.Server.sendFile(self.Client, Group[0][3], self.fernet)
            time.sleep(0.0000001)
            self.Server.send(self.Client, str(Group[0][4]), self.fernet)
            time.sleep(0.0000001)
            self.Server.send(self.Client, READY, self.fernet)

            for Member in Group[1]:
                time.sleep(0.0000001)
                self.Server.send(self.Client, str(Member[0]), self.fernet)
                time.sleep(0.0000001)
                self.Server.send(self.Client, str(Member[1]), self.fernet)
            time.sleep(0.0000001)
            self.Server.send(self.Client, STOP_KEY, self.fernet)
            time.sleep(0.0000001)
            self.Server.send(self.Client, READY, self.fernet)
            for Massage in Group[2]:
                time.sleep(0.0000001)
                self.Server.send(self.Client, str(Massage[0]), self.fernet)
                time.sleep(0.0000001)
                self.Server.sendPickle(self.Client, Massage[1])
                time.sleep(0.0000001)
                self.Server.send(self.Client, Massage[2], self.fernet)
                time.sleep(0.0000001)
                self.Server.sendFile(self.Client, Massage[3], self.fernet)
            time.sleep(0.0000001)
            self.Server.send(self.Client, STOP_KEY, self.fernet)
        time.sleep(0.0000001)
        self.Server.send(self.Client, STOP, self.fernet)

    def Load_Communities(self, CommunityList):
        self.Server.send(self.Client, READY, self.fernet)
        time.sleep(0.0000000000000001)
        for Community in CommunityList:
            time.sleep(0.0000001)
            self.Server.send(self.Client, str(Community[0][0]), self.fernet)
            time.sleep(0.0000001)
            self.Server.send(self.Client, Community[0][1], self.fernet)
            time.sleep(0.0000001)
            self.Server.send(self.Client, Community[0][2], self.fernet)
            time.sleep(0.0000001)
            self.Server.sendFile(self.Client, Community[0][3], self.fernet)
            time.sleep(0.0000001)
            self.Server.send(self.Client, str(Community[0][4]), self.fernet)
            time.sleep(0.0000001)
            self.Server.send(self.Client, READY, self.fernet)
            time.sleep(0.0000001)
            for Member in Community[1]:
                time.sleep(0.0000001)
                self.Server.send(self.Client, str(Member[0]), self.fernet)
                time.sleep(0.0000001)
                self.Server.send(self.Client, str(Member[1]), self.fernet)
            time.sleep(0.0000001)
            self.Server.send(self.Client, STOP_KEY, self.fernet)
            time.sleep(0.0000001)
            self.Server.send(self.Client, READY, self.fernet)
            for Group in Community[2]:
                time.sleep(0.0000001)
                self.Server.send(self.Client, str(Group[0]), self.fernet)
                time.sleep(0.0000001)
                self.Server.send(self.Client, Group[1], self.fernet)
                time.sleep(0.0000001)
                self.Server.send(self.Client, READY, self.fernet)
                time.sleep(0.0000001)
                for Massage in Group[2]:
                    self.Server.send(self.Client, str(Massage[0]), self.fernet)
                    time.sleep(0.0000001)
                    self.Server.sendPickle(self.Client, Massage[1])
                    time.sleep(0.0000001)
                    self.Server.send(self.Client, Massage[2], self.fernet)
                    time.sleep(0.0000001)
                    self.Server.sendFile(self.Client, Massage[3], self.fernet)
                time.sleep(0.0000001)
                self.Server.send(self.Client, STOP_KEY, self.fernet)
            time.sleep(0.0000001)
            self.Server.send(self.Client, STOP_KEY2, self.fernet)
        time.sleep(0.0000001)
        self.Server.send(self.Client, STOP, self.fernet)

    def Load_Public_Communities(self, CommunityList):
        time.sleep(0.0000001)
        self.Server.send(self.Client, READY, self.fernet)
        time.sleep(0.0000001)
        self.Server.send(self.Client, STOP, self.fernet)

    def Sign_in(self):
        file = self.Server.recvFile(self.Client, self.fernet)
        fileName = self.Server.recv(self.Client, self.fernet)
        UserName = self.Server.recv(self.Client, self.fernet)
        PassWord = self.Server.recv(self.Client, self.fernet)
        lock.acquire()
        try:
            self.db.InsertUser(UserName, self.make_hash(PassWord), fileName, file)
        except Exception as e:
            print(e)
        finally:
            lock.release()

        UserID = self.db.GetUserID(UserName)
        time.sleep(0.0000001)
        self.Server.send(self.Client, str(UserID), self.fernet)

    def Log_In(self):
        global Waiting
        UserName = self.Server.recv(self.Client, self.fernet)
        PassWord = self.Server.recv(self.Client, self.fernet)
        PassWord = self.make_hash(PassWord)
        flag = True
        UserID = self.db.GetUserID(self.db.GetUserName(self.db.GetUserID(UserName)))
        for User in Online:
            if UserID == User:
                flag = False
        if flag and self.db.GetPassWord(self.db.GetUserID(UserName)) == PassWord and self.db.GetUserName(
                self.db.GetUserID(UserName)) == UserName and not self.IsOnline(UserID) and UserID not in Waiting:
            self.Server.send(self.Client, str(self.db.GetUserID(UserName)), self.fernet)
            Waiting.append(UserID)
        else:
            self.Server.send(self.Client, FALSE, self.fernet)

    def IsUserNameUsed(self):
        UserName = self.Server.recv(self.Client, self.fernet)
        if self.db.IsUserName(UserName):
            self.Server.send(self.Client, TRUE, self.fernet)
        else:
            self.Server.send(self.Client, FALSE, self.fernet)

    def make_hash(self, PassWord):
        hash_object = hashlib.md5(str(PassWord).encode())
        md5_hash = hash_object.hexdigest()
        return md5_hash


def main():
    b = BarChatServer()
    b.run()


if __name__ == '__main__':
    main()
