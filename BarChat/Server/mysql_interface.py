import mysql.connector
from datetime import datetime

Q1 = "Users (UserID int PRIMARY KEY AUTO_INCREMENT, UserName VARCHAR(32), PassWord VARCHAR(32), UserPicture VARCHAR(32), PictureID int)"  # Create Users String
Q2 = "Friends (FirstUserID int, SecondUserID int)"  # Create Friends String
Q3 = "GroupChat (GroupID int PRIMARY KEY AUTO_INCREMENT, GroupName VARCHAR(32), GroupPicture VARCHAR(32), PictureID int, OwnerID int)"  # Create Groups String
Q4 = "GroupMembers (GroupID int, UserID int)"  # Create Group Members String
Q5 = "GroupMassages (GroupID int, MassageID int,  UserID int, SentDate datetime, FileID int)"  # Create Group Massages String
Q6 = "GroupFiles (GroupID int, MassageID int , UserID int, SentDate datetime, File VARCHAR(32), FileID int)"  # Create Groups Files String
Q7 = "Communities (CommunityID int PRIMARY KEY AUTO_INCREMENT, CommunityName VARCHAR(32), OwnerID int, ServerPicture VARCHAR(32), PictureID int)"  # Create Communities String
Q8 = "CommunityChats (CommunityID int, GroupID int)"  # Create Community Chats String
Q9 = "CommunityMembers (CommunityID int, UserID int)"  # Create Community Members String
Q10 = "Files (FileID int, SerialID int, Data BINARY(255))"  # Create Files String


class database:
    def __init__(self, host, user, passwd, database):
        self.__CreateNewEnvironment(host, user, passwd, database)
        self.__CreateTables()

    def __CreateNewEnvironment(self, host, user, passwd, database):
        self.__OpenSQL(host, user, passwd)
        self.cursor = self.data_base.cursor()
        self.__CreateNewDB(database)
        self.__OpenDB(host, user, passwd, database)
        self.cursor = self.data_base.cursor()

    def __CreateTables(self):
        for Q in [Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10]:  # Create All the Tables for the DataBase
            self.__CreateTable(Q)

    def __CreateTable(self, table):
        try:
            self.cursor.execute(f"CREATE TABLE {table}")
        except Exception as e:
            print(e)

    def __OpenSQL(self, host, user, passwd):
        try:
            self.data_base = mysql.connector.connect(
                host=host,
                user=user,
                passwd=passwd
            )
        except Exception as e:
            print(e)

    def __CreateNewDB(self, database):
        try:
            self.cursor.execute(f"CREATE DATABASE {database}")
        except Exception as e:
            print(e)

    def __OpenDB(self, host, user, passwd, database):
        try:
            self.data_base = mysql.connector.connect(
                host=host,
                user=user,
                passwd=passwd,
                database=database
            )
        except Exception as e:
            print(e)

    def IsUserName(self, UserName):
        try:
            self.cursor.execute(f"SELECT * FROM Users WHERE UserName = '{UserName}'")
        except Exception as e:
            print(e)
        flag = False
        for x in self.cursor:
            flag = True
        return flag

    def __GetNextFileID(self):
        self.cursor.execute("SELECT FileID FROM Files ORDER BY FileID")
        indexList = []
        for index in self.cursor:
            if index[0] not in indexList:
                indexList.append(index[0])
        number = 0
        while True:
            number += 1
            if number not in indexList:
                break
        return number

    def InsertUser(self, UserName, PassWord, UserPicture, PictureVal):
        PictureID = self.__GetNextFileID()
        try:
            self.cursor.execute(f"INSERT INTO Users (UserName, PassWord, UserPicture, PictureID) VALUES (%s,%s,%s,%s)",
                                (UserName, PassWord, UserPicture, PictureID))

            self.__InsertFile(PictureID, PictureVal)
            self.data_base.commit()
        except Exception as e:
            print(e)
    """
    the function is getting bytes as parameter and yield 255 bytes of the original bytes every time 
    """
    def __ArrangeFile(self, FileData):
        jump = 255
        while FileData != b"":
            if len(FileData) < jump:
                yield FileData
                FileData = b""
            else:
                yield FileData[0:jump:1]
                FileData = FileData[jump::1]

    """
    the function is getting FileID and bytes and insert it into the Files SQL Table as a file
    """
    def __InsertFile(self, FileID, FileData):
        index = 1
        for Data in self.__ArrangeFile(FileData):
            try:
                self.cursor.execute(f"INSERT INTO Files (FileID, SerialID, Data) VALUES (%s,%s,%s)",
                                    (FileID, index, Data))
            except Exception as e:
                print(e)
            index += 1
        self.data_base.commit()

    def InsertFriends(self, UserID1, UserID2):
        try:
            if not self.IsFriends(UserID1, UserID2) and self.GetUserExsist(UserID1) and self.GetUserExsist(UserID2):
                self.cursor.execute(f"INSERT INTO Friends (FirstUserID, SecondUserID) VALUES (%s,%s)",
                                    (UserID1, UserID2))
        except Exception as e:
            print(e)
        self.data_base.commit()

    def DeleteFriends(self, UserID1, UserID2):
        try:
            self.cursor.execute(
                f"DELETE FROM Friends WHERE (FirstUserID = {UserID1} AND SecondUserID = {UserID2}) OR (FirstUserID = {UserID2} AND SecondUserID = {UserID1})")
        except Exception as e:
            print(e)
        self.data_base.commit()

    def IsFriends(self, UserID1, UserID2):
        try:
            self.cursor.execute(
                f"SELECT * FROM Friends WHERE (FirstUserID = {UserID1} AND SecondUserID = {UserID2}) OR (FirstUserID = {UserID2} AND SecondUserID = {UserID1})")
        except Exception as e:
            print(e)
        flag = False
        for friends in self.cursor:
            flag = True
        return flag

    def GetUserExsist(self, UserID):
        self.cursor.execute(f"SELECT * FROM Users WHERE UserID = {UserID}")
        flag = False
        for user in self.cursor:
            flag = True
        return flag

    def DeleteFile(self, FileID):
        try:
            self.cursor.execute(f"DELETE FROM Files WHERE FileID = {FileID}")
            self.data_base.commit()
        except Exception as e:
            print(e)

    def GetFile(self, FileID):
        binaryFile = b""
        if type(FileID) is int:
            self.cursor.execute(f"SELECT Data FROM Files WHERE FileID = {FileID}")
            for Data in self.cursor:
                binaryFile += Data[0]
            return binaryFile
        else:
            return None

    def GetUsers(self):
        self.cursor.execute("SELECT UserID, UserName, PassWord, UserPicture, PictureID FROM Users")
        tempL = [user for user in self.cursor]
        return tempL

    def InsertGroup(self, GroupName, GroupPicture, PictureVal, UserID):
        PictureID = self.__GetNextFileID()
        try:
            self.cursor.execute(
                f"INSERT INTO GroupChat (GroupName, GroupPicture, PictureID, OwnerID) VALUES (%s,%s,%s,%s)",
                (GroupName, GroupPicture, PictureID, UserID))
            self.__InsertFile(PictureID, PictureVal)
            self.data_base.commit()
        except Exception as e:
            print(e)

        try:
            self.cursor.execute(f"SELECT GroupID FROM GroupChat WHERE GroupName = '{GroupName}' AND PictureID = {PictureID} ORDER BY GroupID")
        except Exception as e:
            print(e)
        temp = None
        for x in self.cursor:
            temp = x[0]
        return temp


    def InsertGroupMember(self, GroupID, UserID):
        try:
            if self.IsGroup(GroupID) and self.GetUserExsist(UserID) and not self.IsMember(GroupID, UserID):
                self.cursor.execute("INSERT INTO GroupMembers (GroupID, UserID) VALUES (%s,%s)", (GroupID, UserID))
            self.data_base.commit()
        except Exception as e:
            print(e)

    def DeleteGroupMember(self, GroupID, UserID):
        try:
            self.cursor.execute(f"DELETE FROM GroupMembers WHERE GroupID = {GroupID} AND UserID = {UserID}")
            self.data_base.commit()
        except Exception as e:
            print(e)

    def IsGroup(self, GroupID):
        try:
            self.cursor.execute(f"SELECT * FROM GroupChat WHERE GroupID = {GroupID}")
        except Exception as e:
            print(e)
        flag = False
        for Group in self.cursor:
            flag = True
        return flag

    def IsMember(self, GroupID, UserID):
        try:
            self.cursor.execute(f"SELECT * FROM GroupMembers WHERE GroupID = {GroupID} AND UserID = {UserID}")
        except Exception as e:
            print(e)
        flag = False
        for Group in self.cursor:
            flag = True
        return flag

    def __GetNextMassageID(self, GroupID):
        MaxMassageID = 1
        try:
            self.cursor.execute(f"SELECT MassageID FROM GroupMassages WHERE GroupID = {GroupID}")
        except Exception as e:
            print(e)
        for ID in self.cursor:
            if ID[0] > MaxMassageID:
                MaxMassageID = ID[0] + 1
        try:
            self.cursor.execute(f"SELECT MassageID FROM GroupFiles WHERE GroupID = {GroupID}")
        except Exception as e:
            print(e)
        for ID in self.cursor:
            if ID[0] > MaxMassageID:
                MaxMassageID = ID[0] + 1
        return MaxMassageID

    def InsertMassage(self, GroupID, UserID, Massage, date):
        MassageID = self.__GetNextMassageID(GroupID)
        FileID = self.__GetNextFileID()
        if self.IsMember(GroupID, UserID) or UserID == 0:
            try:
                self.cursor.execute(
                    "INSERT INTO GroupMassages (GroupID, MassageID, UserID, SentDate, FileID) VALUES (%s,%s,%s,%s,%s)",
                    (GroupID, MassageID, UserID, date, FileID))
                self.__InsertFile(FileID, Massage)
            except Exception as e:
                print(e)
        self.data_base.commit()

    def InsertMassageFile(self, GroupID, UserID, date, FileName, File):
        MassageID = self.__GetNextMassageID(GroupID)
        FileID = self.__GetNextFileID()
        if self.IsMember(GroupID, UserID) or UserID == 0:
            try:
                self.cursor.execute(
                    "INSERT INTO GroupFiles (GroupID, MassageID, UserID, SentDate, File, FileID) VALUES (%s,%s,%s,%s,%s,%s)",
                    (GroupID, MassageID, UserID, date, FileName, FileID))
                self.__InsertFile(FileID, File)
            except Exception as e:
                print(e)
        self.data_base.commit()

    def DeleteGroupChat(self, GroupID):
        try:
            self.cursor.execute(f"SELECT FileID FROM GroupMassages WHERE GroupID = {GroupID}")
            templ = []
            for ID in self.cursor:
                templ.append(ID[0])
            for ID in templ:
                self.DeleteFile(ID)
            self.cursor.execute(f"SELECT FileID FROM GroupFiles WHERE GroupID = {GroupID}")
            templ = []
            for ID in self.cursor:
                templ.append(ID[0])
            for ID in templ:
                self.DeleteFile(ID)
            self.cursor.execute(f"SELECT PictureID FROM GroupChat WHERE GroupID = {GroupID}")
            templ = []
            for ID in self.cursor:
                templ.append(ID[0])
            for ID in templ: self.DeleteFile(ID)
            self.cursor.execute(f"DELETE FROM GroupMembers WHERE GroupID = {GroupID}")
            self.cursor.execute(f"DELETE FROM GroupMassages WHERE GroupID = {GroupID}")
            self.cursor.execute(f"DELETE FROM GroupFiles WHERE GroupID = {GroupID}")
            self.cursor.execute(f"DELETE FROM GroupChat WHERE GroupID = {GroupID}")
            self.cursor.execute(f"DELETE FROM CommunityChats WHERE GroupID = {GroupID}")
            self.data_base.commit()
        except Exception as e:
            print(e)

    def InsertCommunity(self, CommunityName, UserID, PictureName, PictureVal):
        PictureID = self.__GetNextFileID()
        try:
            self.cursor.execute(
                "INSERT INTO Communities (CommunityName, OwnerID, ServerPicture, PictureID) VALUES (%s,%s,%s,%s)",
                (CommunityName, UserID, PictureName, PictureID))
            self.__InsertFile(PictureID, PictureVal)
        except Exception as e:
            print(e)
        self.data_base.commit()

    def IsCommunity(self, CommunityID):
        try:
            self.cursor.execute(f"SELECT * FROM Communities WHERE CommunityID = {CommunityID}")
        except Exception as e:
            print(e)
        flag = False
        for Community in self.cursor:
            flag = True
        return flag

    def IsCommunityMember(self, UserID, CommunityID):
        try:
            self.cursor.execute(
                f"SELECT * FROM CommunityMembers WHERE CommunityID = {CommunityID} AND UserID = {UserID}")
        except Exception as e:
            print(e)
        flag = False
        for Community in self.cursor:
            flag = True
        return flag

    def InsertCommunityMember(self, CommunityID, UserID):
        try:
            if self.GetUserExsist(UserID) and self.IsCommunity(CommunityID) and not self.IsCommunityMember(UserID,
                                                                                                           CommunityID):
                self.cursor.execute("INSERT INTO CommunityMembers (CommunityID, UserID) VALUES (%s,%s)",
                                    (CommunityID, UserID))
                self.InsertMemberChat(CommunityID, UserID)
        except Exception as e:
            print(e)
        self.data_base.commit()

    def InsertMemberChat(self, CommunityID, UserID):
        try:
            self.cursor.execute(f"SELECT GroupID FROM CommunityChats WHERE CommunityID = {CommunityID}")
        except Exception as e:
            print(e)
        templ = []
        for GroupID in self.cursor:
            templ.append(GroupID[0])
        for Group in templ:
            self.InsertGroupMember(Group, UserID)
        self.data_base.commit()

    def IsCommunityGroup(self, CommunityID, GroupID):
        try:
            self.cursor.execute(
                f"SELECT * FROM CommunityChats WHERE CommunityID = {CommunityID} AND GroupID = {GroupID}")
        except Exception as e:
            print(e)
        flag = False
        for Group in self.cursor:
            flag = True
        return flag

    def InsertCommunityChat(self, CommunityID, GroupID):
        if self.IsCommunity(CommunityID) and self.IsGroup(GroupID) and not self.IsCommunityGroup(CommunityID,
                                                                                                 GroupID):
            try:
                self.cursor.execute("INSERT INTO CommunityChats (CommunityID, GroupID) VALUES (%s,%s)",
                                    (CommunityID, GroupID))
            except Exception as e:
                print(e)
            self.data_base.commit()
            try:
                self.cursor.execute(f"SELECT UserID FROM CommunityMembers WHERE CommunityID = {CommunityID}")
            except Exception as e:
                print(e)
            l = []
            for UserID in self.cursor:
                l.append(UserID[0])
            for User in l:
                self.InsertGroupMember(GroupID, User)
        self.data_base.commit()

    def DeleteCommunityMember(self, CommunityID, MemberID):
        try:
            print(3)
            self.cursor.execute(f"SELECT GroupID FROM CommunityChats WHERE CommunityID = {CommunityID}")
            templ = []
            for GroupID in self.cursor:
                templ.append(GroupID[0])
            for Group in templ:
                self.DeleteGroupMember(Group, MemberID)
            print(1)
            self.cursor.execute(
                f"DELETE FROM CommunityMembers WHERE CommunityID = {CommunityID} AND UserID = {MemberID}")
            print(2)
        except Exception as e:
            print(e)
        self.data_base.commit()

    def DeleteCommunity(self, CommunityID):
        try:
            self.cursor.execute(f"SELECT GroupID FROM CommunityChats WHERE CommunityID = {CommunityID}")
            templ = []
            for GroupID in self.cursor:
                templ.append(GroupID[0])
            for Group in templ:
                self.DeleteGroupChat(Group)
            self.cursor.execute(f"DELETE FROM CommunityChats WHERE CommunityID = {CommunityID}")
            self.cursor.execute(f"DELETE FROM Communities WHERE CommunityID = {CommunityID}")
            self.data_base.commit()
        except Exception as e:
            print(e)

    def DeleteUser(self, UserID):
        try:
            self.cursor.execute(f"SELECT CommunityID FROM CommunityMembers WHERE UserID = {UserID}")
            templ = []
            for CommunityID in self.cursor:
                templ.append(CommunityID[0])
            for Community in templ:
                self.DeleteCommunityMember(Community, UserID)
            self.cursor.execute(f"SELECT GroupID FROM GroupMembers WHERE UserID = {UserID}")
            templ = []
            for GroupID in self.cursor:
                templ.append(GroupID[0])
            for Group in templ:
                self.DeleteGroupMember(Group, UserID)
            self.cursor.execute(f"DELETE FROM Users WHERE UserID = {UserID}")
            self.data_base.commit()
        except Exception as e:
            print(e)

    def GetPassWord(self, UserID):
        try:
            self.cursor.execute(f"SELECT PassWord FROM Users WHERE UserID = {UserID}")
        except Exception as e:
            print(e)
        PassWord = ""
        for x in self.cursor:
            PassWord = x[0]
        return PassWord

    def GetUserName(self, UserID):
        try:
            self.cursor.execute(f"SELECT UserName FROM Users WHERE UserID = {UserID}")
        except Exception as e:
            print(e)
        UserName = ""
        for x in self.cursor:
            UserName = x[0]
        return UserName

    def GetUserID(self, UserName):

        try:
            self.cursor.execute(f"SELECT UserID FROM Users WHERE UserName = '{UserName}'")
        except Exception as e:
            print(e)
        UserID = None
        for x in self.cursor:
            UserID = x[0]
        return UserID

    def GetTables(self):
        tempL = []
        newL = []
        massage = ""
        try:
            self.cursor.execute("SHOW TABLES")
            for Table in self.cursor:
                tempL.append(Table[0])
            for var in tempL:
                self.cursor.execute(f"DESCRIBE {var}")
                var = f"{var} ["
                for val in self.cursor:
                    var += "("
                    for item in val:
                        var += f"{item},"
                    var += ")"
                var += "]"
                newL.append(var)
            for item in newL:
                massage += f"{item}\n"
        except Exception as e:
            print(e)
        return massage

    def GetTableData(self, Table):
        massage = ""
        try:
            self.cursor.execute(f"SELECT * FROM {Table}")
            for var in self.cursor:
                for val in var:
                    massage += f"{val} "
                massage += "\n"
        except Exception as e:
            print(e)
        return massage

    def GetGroup(self, GroupID):
        massage = ""
        try:
            self.cursor.execute(f"SELECT GroupName, GroupPicture, OwnerID FROM GroupChat WHERE GroupID = {GroupID}")
            for Group in self.cursor:
                massage += "Group Info: (GroupName, GroupPicture, OwnerID) \n"
                for var in Group:
                    massage += f"{var}"
                massage += "\n"
            self.cursor.execute(f"SELECT UserID FROM GroupMembers WHERE GroupID = {GroupID}")
            massage += "Group Members: "
            for User in self.cursor:
                massage += f"{User}, "
        except Exception as e:
            print(e)
        return massage

    def GetUserPicture(self, UserID):
        try:
            self.cursor.execute(f"SELECT UserPicture FROM Users WHERE UserID = {UserID}")
        except Exception as e:
            print(e)
        userpic = ""
        for x in self.cursor:
            userpic = x[0]
        return userpic

    def GetUserPictureID(self, UserID):
        try:
            self.cursor.execute(f"SELECT PictureID FROM Users WHERE UserID = {UserID}")
        except Exception as e:
            print(e)
        userpic = ""
        for x in self.cursor:
            userpic = x[0]
        return userpic

    def GetUser(self, UserID):
        return UserID

    def GetCommunity(self, CommunityID):
        massage = ""
        try:
            self.cursor.execute(
                f"SELECT CommunityName, OwnerID, ServerPicture FROM Communities WHERE CommunityID = {CommunityID}")
            massage = "Group Info: (CommunityName, OwnerID, ServerPicture) "
            for Community in self.cursor:
                for item in Community:
                    massage += f"{item}, "
            massage += "\nMembers: "
            self.cursor.execute(f"SELECT UserID FROM CommunityMembers WHERE CommunityID = {CommunityID}")
            for Member in self.cursor:
                massage += f"{Member}, "
            massage += "\n"
            self.cursor.execute(f"SELECT GroupID FROM CommunityChats WHERE CommunityID = {CommunityID}")
            for Group in self.cursor:
                massage += f"{Group}, "
        except Exception as e:
            print(e)
        return massage

    def ChangeUserName(self, UserID, UserName):
        try:
            self.cursor.execute(f"UPDATE Users SET UserName = '{UserName}' WHERE UserID = {UserID}")
        except Exception as e:
            print(e)
        self.data_base.commit()

    def ChangePassWord(self, UserID, PassWord):
        try:
            self.cursor.execute(f"UPDATE Users SET PassWord = '{PassWord}' WHERE UserID = {UserID}")
        except Exception as e:
            print(e)
        self.data_base.commit()

    def ChangePicture(self, UserID, UserPicture, Val):
        try:
            self.cursor.execute(f"SELECT PictureID FROM Users WHERE UserID = {UserID}")
            for x in self.cursor:
                self.DeleteFile(x[0])
            PictureID = self.__GetNextFileID()
            self.cursor.execute(
                f"UPDATE Users SET UserPicture = '{UserPicture}' WHERE UserID = {UserID}")
            self.cursor.execute(
                f"UPDATE Users SET PictureID = {PictureID} WHERE UserID = {UserID}")
            self.__InsertFile(PictureID, Val)
        except Exception as e:
            print(e)
        self.data_base.commit()

    def ChangeGroup(self, GroupID, GroupName):
        try:
            self.cursor.execute(f"UPDATE GroupChat SET GroupName = '{GroupName}' WHERE GroupID = {GroupID}")
        except Exception as e:
            print(e)
        self.data_base.commit()

    def ChangeGroupOwner(self, GroupID, UserID):
        try:
            if UserID == 0 or (self.GetUserExsist(UserID) and self.IsMember(GroupID, UserID)):
                self.cursor.execute(f"UPDATE GroupChat SET OwnerID = {UserID} WHERE GroupID = {GroupID}")
        except Exception as e:
            print(e)
        self.data_base.commit()

    def ChangeGroupPicture(self, GroupID, GroupPicture, Val):
        try:
            self.cursor.execute(f"SELECT PictureID FROM GroupChat WHERE GroupID = {GroupID}")
            for x in self.cursor:
                self.DeleteFile(x[0])
            PictureID = self.__GetNextFileID()
            self.cursor.execute(
                f"UPDATE GroupChat SET GroupPicture = '{GroupPicture}' WHERE GroupID = {GroupID}")
            self.cursor.execute(
                f"UPDATE GroupChat SET PictureID = {PictureID} WHERE GroupID = {GroupID}")
            self.__InsertFile(PictureID, Val)
        except Exception as e:
            print(e)
        self.data_base.commit()

    def ChangeCommunityChat(self, CommunityID, CommunityName):
        try:
            self.cursor.execute(
                f"UPDATE Communities SET CommunityName = '{CommunityName}' WHERE CommunityID = {CommunityID}")
        except Exception as e:
            print(e)
        self.data_base.commit()




    def ChangeCommunityOwner(self, CommunityID, UserID):
        try:
            if self.IsCommunityMember(UserID, CommunityID):
                self.cursor.execute(f"SELECT GroupID FROM CommunityChats WHERE CommunityID = {CommunityID}")
                tempL = []
                for x in self.cursor:
                    tempL.append(x[0])
                for var in tempL:
                    self.ChangeGroupOwner(var, UserID)
                self.cursor.execute(f"UPDATE Communities SET OwnerID = {UserID} WHERE CommunityID = {CommunityID}")
        except Exception as e:
            print(e)
        self.data_base.commit()

    def ChangeCommunityPicture(self, CommunityID, CommunityPicture, Val):
        try:
            self.cursor.execute(f"SELECT PictureID FROM Communities WHERE CommunityID = {CommunityID}")
            for x in self.cursor:
                self.DeleteFile(x[0])
            PictureID = self.__GetNextFileID()
            self.cursor.execute(
                f"UPDATE Communities SET ServerPicture = '{CommunityPicture}' WHERE CommunityID = {CommunityID}")
            self.cursor.execute(
                f"UPDATE Communities SET PictureID = {PictureID} WHERE CommunityID = {CommunityID}")
            self.__InsertFile(PictureID, Val)
        except Exception as e:
            print(e)
        self.data_base.commit()

    def key(self, var):
        return var[1]

    def GetGroupMassages(self, GroupID):
        templ = []
        try:
            self.cursor.execute(f"SELECT UserID, SentDate, FileID FROM GroupMassages WHERE GroupID = {GroupID}")
            for x in self.cursor:
                templ.append([x[0], x[1], x[2]])
            self.cursor.execute(f"SELECT UserID, SentDate, FileID, File FROM GroupFiles WHERE GroupID = {GroupID}")
            for x in self.cursor:
                templ.append([x[0], x[1], x[2], x[3]])
            for x in templ:
                x[2] = self.GetFile(x[2])
            templ.sort(key=self.key)
        except Exception as e:
            print(e)
        return templ

    def GetGroupMembers(self, GroupID):
        templ = []
        try:
            self.cursor.execute(f"SELECT UserID FROM GroupMembers WHERE GroupID = {GroupID}")
            for x in self.cursor:
                templ.append(x[0])
        except Exception as e:
            print(e)
        return templ
    def GetCommunities(self):
        templ = []
        try:
            self.cursor.execute(f"SELECT CommunityID, CommunityName FROM Communities")
            for x in self.cursor:
                templ.append([x[0], x[1]])
        except Exception as e:
            print(e)
        return templ

    def GetCommunityName(self, CommunityID):
        var = ""
        try:
            self.cursor.execute(f"SELECT CommunityName FROM Communities WHERE CommunityID = {CommunityID}")
            for x in self.cursor:
                var = x[0]
        except Exception as e:
            print(e)
        return var

    def GetGroupOwner(self, GroupID):
        try:
            self.cursor.execute(f"SELECT OwnerID FROM GroupChat WHERE GroupID = {GroupID}")
            for x in self.cursor:
                var = x[0]
        except Exception as e:
            print(e)
        return var

    def GetGroupName(self, GroupID):
        var = ""
        try:
            self.cursor.execute(f"SELECT GroupName FROM GroupChat WHERE GroupID = {GroupID}")
            for x in self.cursor:
                var = x[0]
        except Exception as e:
            print(e)
        return var

    def GetGroupInfo(self, GroupID):
        var = []
        try:
            self.cursor.execute(
                f"SELECT GroupName, GroupPicture, PictureID, OwnerID FROM GroupChat WHERE GroupID = {GroupID}")
            for x in self.cursor:
                var = [x[0], x[1], x[2], x[3]]
            var[2] = self.GetFile(var[2])
        except Exception as e:
            print(e)
        return var

    def GetUserFriends(self, UserID):
        templ = []
        try:
            self.cursor.execute(
                f"SELECT FirstUserID, SecondUserID FROM Friends WHERE FirstUserID = {UserID} OR SecondUserID = {UserID}")
            for x in self.cursor:
                templ.append(x[0] if x[1] == UserID else x[1])
        except Exception as e:
            print(e)
        return templ

    def GetUserID(self, UserName):
        var = None
        try:
            self.cursor.execute(f"SELECT UserID FROM Users WHERE UserName = '{UserName}'")
            for x in self.cursor:
                var = x[0]
        except Exception as e:
            print(e)
        return var

    def GetUser(self, UserID):
        var = [[], [], [], []]
        try:
            self.cursor.execute(f"SELECT UserName, UserPicture, PictureID FROM Users WHERE UserID = {UserID}")
            for x in self.cursor:
                var[0] = [x[0], x[1], x[2]]
            var[0][2] = self.GetFile(var[0][2])
            var[1] = self.GetUserFriends(UserID)
            templ = []
            self.cursor.execute(f"SELECT GroupID FROM CommunityChats")
            for x in self.cursor:
                templ.append(x[0])
            self.cursor.execute(f"SELECT GroupID FROM GroupMembers WHERE UserID = {UserID}")
            for x in self.cursor:
                if x[0] not in templ: var[2].append(x[0])
            self.cursor.execute(f"SELECT CommunityID FROM CommunityMembers WHERE UserID = {UserID}")
            for x in self.cursor:
                var[3].append(x[0])
        except Exception as e:
            print(e)
        return var

    def GetCommunityInfo(self, CommunityID):
        var = [[], [], []]
        try:
            if self.IsCommunity(CommunityID):
                self.cursor.execute(
                    f"SELECT CommunityName, OwnerID, ServerPicture, PictureID FROM Communities WHERE CommunityID = {CommunityID}")
                for x in self.cursor:
                    var[0] = [x[0], x[1], x[2], x[3]]
                var[0][3] = self.GetFile(var[0][3])
                self.cursor.execute(f"SELECT GroupID FROM CommunityChats WHERE CommunityID = {CommunityID}")
                for x in self.cursor:
                    var[1].append(x[0])
                self.cursor.execute(f"SELECT UserID FROM CommunityMembers WHERE CommunityID = {CommunityID}")
                for x in self.cursor:
                    var[2].append(x[0])
        except Exception as e:
            print(e)
        return var


def main():
    pass


if __name__ == '__main__':
    main()
