from PIL import Image
import io
import pygame
import time
from text_box import *

"""
this object is supporting appending users on screen
"""
class User:
    def __init__(self, ID, UserName, UserPicture, Picture, path, screen_size, font, screen, Icon=None,
                 color=(41, 43, 47)):
        self.Color = (41, 43, 47)
        self.ID = ID
        self.UserName = UserName
        self.UserPicture = UserPicture
        self.Picture = Picture
        self.path = path
        self.screen_size = screen_size
        self.font = font
        self.screen = screen
        self.try1 = Icon
        self.Rect = None
        self.TouchEvent = [False, False]
        self.Load()

    def pilImageToSurface(self, pilImage):
        return pygame.image.fromstring(
            pilImage.tobytes(), pilImage.size, pilImage.mode).convert()

    def ByteToSurface(self, bytes):
        return self.pilImageToSurface(Image.open(io.BytesIO(bytes)))

    """
    load user values
    """
    def Load(self):
        if not self.try1 == None:
            self.Icon = self.try1
        else:
            self.Icon = self.ByteToSurface(self.Picture)
        self.IconR = self.Icon.get_rect()
        self.UserNameText = self.font.render(self.UserName, True, (255, 255, 255))
        self.UserNameTextR = self.UserNameText.get_rect()

    """
    render user on screen
    """
    def render(self, Left, Top, Width, Height, background=True):
        self.Icon = pygame.transform.scale(self.Icon, (Height - 5, Height - 5))
        self.IconR = self.Icon.get_rect()
        if background:
            pygame.draw.rect(self.screen, self.Color, pygame.Rect(Left, Top, Width, Height), 0, 4)
        self.IconR.midleft = (Left + 4, Top + Height / 2)
        self.screen.blit(self.Icon, self.IconR)
        tempUserName = self.UserName
        self.UserNameTextR.midleft = (self.IconR.right + 5, Top + Height / 2)
        while self.UserNameTextR.width > Left + Width - self.IconR.right + 20:
            tempUserName = tempUserName[0:len(tempUserName) - 1:]
            self.UserNameText = self.font.render(tempUserName, True, (255, 255, 255))
            self.UserNameTextR = self.UserNameText.get_rect()
            self.UserNameTextR.midleft = (self.IconR.right + 5, Top + Height / 2)
        self.screen.blit(self.UserNameText, self.UserNameTextR)

"""
this object is supporting appending massages on screen
"""
class Massage:
    def __init__(self, UserName, Date, Type, Massage, path, screen_size, font, screen, Mfont, FileIcon):
        self.UserName = UserName
        self.Date = Date
        self.Type = Type
        self.Massage = Massage
        self.path = path
        self.screen_size = screen_size
        self.font = font
        self.screen = screen
        self.Mfont = Mfont
        self.Rect = None
        self.FileIcon = FileIcon
        self.massageEvents = [False, False, False]
        self.Load()

    def pilImageToSurface(self, pilImage):
        return pygame.image.fromstring(
            pilImage.tobytes(), pilImage.size, pilImage.mode).convert()

    def ByteToSurface(self, bytes):
        return self.pilImageToSurface(Image.open(io.BytesIO(bytes)))

    """
    the function is loading and prepering the Massage Object for rendering
    """
    def Load(self):
        self.MassageTop = self.font.render(fr"{self.UserName}", True, (255, 255, 255))
        self.MassageTopDate = self.font.render(rf" {self.Date.day}/{self.Date.month}/{self.Date.year}", True,
                                               (121, 124, 124))
        if self.Type == "Text":
            self.MassageFile = None
        elif self.Type[-4::] in [".jpg", ".png"]:
            icon = self.ByteToSurface(self.Massage)
            z = icon.get_rect().height / icon.get_rect().width
            self.MassageFile = pygame.transform.scale(icon,
                                                      (self.screen_size[0] * 1 / 4, z * (self.screen_size[0] * 1 / 4)))
        else:
            self.MassageFile = self.Mfont.render(self.Type, True, (0, 164, 195))
            # self.MassageFile = self.Mfont.render(self.Type, True, (0, 164, 195))
            self.FileIcon = pygame.transform.scale(self.FileIcon,
                                                   (self.screen_size[0] * 1 / 25, self.screen_size[0] * 1 / 25))

    def wrap_word(self, word, width):
        wrapped_word = []

        while len(word):
            ## Store as many characters as possible to fit in allowed width
            line_of_char = []
            while len(word):
                line_of_char.append(word[:1])
                word = word[1:]
                fw, fh = self.Mfont.size(''.join(line_of_char + [word[:1]]))

                ## If width exceeds then store remaining characters in new line
                if fw > width:
                    break

            ## Join all characters that fit in width into one line
            final_line = ''.join(line_of_char)
            wrapped_word.append(final_line)

        return wrapped_word

    """
    the function is updates the massage if touched and downloads it
    """
    def update(self):
        if not self.massageEvents[1]:
            if self.Rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and not \
                    self.massageEvents[2]:
                self.massageEvents[0] = True
            if self.massageEvents[0]:
                pass
            if self.Rect.collidepoint(pygame.mouse.get_pos()) and not pygame.mouse.get_pressed()[0] and \
                    self.massageEvents[0]:
                self.massageEvents[0] = False
                self.massageEvents[1] = True
                if self.Type != "Text":
                    t = self.Type.split("/")[-1]
                    t = t.split("\\")[-1]
                    file = open(rf"C:\\Users\\user\\Downloads\\1{t}", "wb")
                    file.write(self.Massage)
                    file.close()


            elif not pygame.mouse.get_pressed()[0]:
                self.massageEvents[0] = False
            if pygame.mouse.get_pressed()[0]:
                self.massageEvents[2] = True
            else:
                self.massageEvents[2] = False
        else:
            self.massageEvents[1] = False

    """
    the function is bliting the massage in the Rect Given into the screen
    """
    def render(self, Left, Top, Width, visible=True):
        Height = 0
        MassageTopR = self.MassageTop.get_rect()
        MassageTopR.topleft = (Left, Top)
        Height += MassageTopR.height
        flag = True
        Massages = []
        if self.Type == "Text":
            if type(self.Massage) != list:
                self.Massage = self.wrap_word(self.Massage.decode(), Width)
            for massage in self.Massage:
                massage = b''.join(massage.encode().split(b'\x00')).decode()
                MassT = self.Mfont.render(massage, True, (255, 255, 255))
                Height += MassT.get_rect().height
                MassRT = MassT.get_rect()
                MassRT.topleft = MassageTopR.bottomleft if flag else Massages[-1][1].bottomleft
                if flag:
                    flag = False
                Massages.append([MassT, MassRT])
        elif self.Type[-4::] in [".jpg", ".png"]:
            massageR = self.MassageFile.get_rect()
            massageR.midtop = (Left + (Width / 2), MassageTopR.bottomleft[1] + 2)
            Height += massageR.height + 4
            Massages.append([self.MassageFile, massageR])
        else:
            IconR = self.FileIcon.get_rect()
            IconR.topleft = MassageTopR.bottomleft
            MassR = self.MassageFile.get_rect()
            MassR.midleft = (IconR.midright[0] + 5, IconR.midright[1])
            Massages.append([self.FileIcon, IconR])
            Massages.append([self.MassageFile, MassR])
            Height += IconR.height
        if visible:
            pygame.draw.rect(self.screen, (48, 44, 44), pygame.Rect(Left, Top, Width, Height), 0, 4)
            self.screen.blit(self.MassageTop, MassageTopR)
            DateR = self.MassageTopDate.get_rect()
            DateR.topleft = MassageTopR.topright
            self.screen.blit(self.MassageTopDate, DateR)
            for x in Massages:
                self.screen.blit(x[0], x[1])

        return Height


"""
this object is supporting appending groups on screen
"""
class Group:
    def __init__(self, ID, GroupName, GroupPicture, Picture, OwnerID, MemberList, MassageList, path, screen_size, font,
                 screen, send_icon, upload, userID):
        self.UserID = userID
        self.ID = ID
        self.Upload = upload
        self.GroupName = GroupName
        self.GroupPicture = GroupPicture
        self.Picture = Picture
        self.OwnerID = OwnerID
        self.MemberList = MemberList
        self.MassageList = MassageList
        self.path = path
        self.screen_size = screen_size
        self.font = font
        self.screen = screen
        self.UploadEvents = [False, False, False]
        self.GroupEvnets = [False, False, False]
        self.GroupEvnets2 = [False, False]
        self.TextBox = [False, False, False]
        self.Rect = None
        self.send_icon = send_icon
        self.UpperBar = None
        self.UpperBarAddButton = None
        self.UpperBarAddButtonR = None
        self.UpperBarAddButtonEvents = [False, False]
        self.GroupNamet = None
        self.GroupNameR = None
        self.LeaveGroup = None
        self.LeaveGroupR = None
        self.LeaveGroupEvent = [False, False]
        self.Load()

    """
    loads the group values
    """
    def Load(self):
        TextBarRect = pygame.Rect(self.screen_size[0] * 3 / 12 + 70, self.screen_size[1] * 15 / 16 - 10,
                                  self.screen_size[0] * 5 / 8 - 140, self.screen_size[1] * 1 / 16 - 10)

        self.UpperBar = pygame.Rect(self.screen_size[0] * 3 / 12, 0, self.screen_size[0] * 5 / 8, 50)
        self.GroupNamet = self.font.render(self.GroupName, True, (220, 221, 222))
        self.GroupNameR = self.GroupNamet.get_rect()
        self.GroupNameR.midleft = (self.UpperBar.midleft[0] + 5, self.UpperBar.midleft[1])
        self.UpperBarAddButton = self.font.render("Add Member", True, (220, 221, 222))
        self.UpperBarAddButtonR = self.UpperBarAddButton.get_rect()
        self.UpperBarAddButtonR.midright = (self.UpperBar.midright[0] - 5, self.UpperBar.midright[1])
        self.LeaveGroup = self.font.render("Leave Group", True, (220, 221, 222))
        self.LeaveGroupR = self.LeaveGroup.get_rect()
        self.LeaveGroupR.midright = (self.UpperBarAddButtonR.midleft[0] - 10, self.UpperBarAddButtonR.midleft[1])
        self.send_icon = pygame.transform.scale(self.send_icon,
                                                (self.screen_size[1] * 1 / 16 - 20, self.screen_size[1] * 1 / 16 - 20))

        self.send_iconR = self.send_icon.get_rect()
        self.send_iconR.topleft = (self.screen_size[0] * 3 / 12 + 22, self.screen_size[1] * 15 / 16 - 5)
        self.Upload = pygame.transform.scale(self.Upload,
                                             (self.screen_size[1] * 1 / 16 - 20, self.screen_size[1] * 1 / 16 - 20))
        self.UploadR = self.Upload.get_rect()
        self.UploadR.topleft = (self.screen_size[0] * 9 / 11 + 22, self.screen_size[1] * 15 / 16 - 5)
        self.TextBar = TextInputBox(TextBarRect.left, TextBarRect.top, font_family='Arial', font_size=25,
                                    max_width=TextBarRect.width, max_height=TextBarRect.height + 10,
                                    max_string_length=-1)
        if not self.Picture == None:
            self.Picture = self.ByteToSurface(self.Picture)
        r = self.screen_size[1] * 15 / 16 - 15
        flag = True
        for massage in self.MassageList[::-1]:
            h = massage.render(self.screen_size[0] * 3 / 12 + 20, r, self.screen_size[0] * 5 / 8 - 40, visible=False)
            r = r - h - 5
            massage.Rect = pygame.Rect(self.screen_size[0] * 3 / 12 + 20, r, self.screen_size[0] * 5 / 8 - 40, h)
        t = self.screen_size[1] * 1 / 12
        for user in self.MemberList:
            user.Rect = pygame.Rect(self.screen_size[0] * 10.5 / 12, t, self.screen_size[0] * 1.5 / 12,
                                    self.screen_size[1] * 1 / 20)
            t += self.screen_size[1] * 1 / 20


    """
    update the self vars of the group by event feed
    """
    def update(self, events, Client):
        Alert = []
        events2 = events.copy()
        if not self.Picture == None:

            if self.Rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and not \
                    self.GroupEvnets[2]:
                pygame.draw.rect(self.screen, (96, 100, 244), self.Rect, 0, 10)
                self.GroupEvnets[0] = True
            if self.GroupEvnets[0]:
                pygame.draw.rect(self.screen, (96, 100, 244), self.Rect, 0, 10)
            if self.Rect.collidepoint(pygame.mouse.get_pos()) and not pygame.mouse.get_pressed()[0] and \
                    self.GroupEvnets[0]:
                pygame.draw.rect(self.screen, (96, 100, 244), self.Rect, 0, 10)
                self.GroupEvnets[0] = False
                self.GroupEvnets[1] = True

            elif not pygame.mouse.get_pressed()[0]:
                self.GroupEvnets[0] = False
            if pygame.mouse.get_pressed()[0]:
                self.GroupEvnets[2] = True
            else:
                self.GroupEvnets[2] = False

            if self.Rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[2]:
                pygame.draw.rect(self.screen, (96, 100, 244), self.Rect, 0, 10)
                self.GroupEvnets2[0] = True
            if self.GroupEvnets2[0]:
                pygame.draw.rect(self.screen, (96, 100, 244), self.Rect, 0, 10)
            if self.Rect.collidepoint(pygame.mouse.get_pos()) and not pygame.mouse.get_pressed()[2] and \
                    self.GroupEvnets2[0]:
                pygame.draw.rect(self.screen, (96, 100, 244), self.Rect, 0, 10)
                self.GroupEvnets2[0] = False
                self.GroupEvnets2[1] = True
                Alert = ["Delete Group", self.ID, self.Rect, None, None, [False, False], None, None, [False, False],
                         True, self.OwnerID]
            elif not pygame.mouse.get_pressed()[2]:
                self.GroupEvnets2[0] = False
        if self.GroupEvnets[1]:
            if self.UserID == self.OwnerID:
                if self.UpperBarAddButtonR.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    self.UpperBarAddButtonEvents[0] = True
                    pygame.draw.rect(self.screen, (60, 69, 165), self.UpperBarAddButtonR, 0, 4)
                if self.UpperBarAddButtonR.collidepoint(pygame.mouse.get_pos()) and not pygame.mouse.get_pressed()[
                    0] and self.UpperBarAddButtonEvents[0]:
                    self.UpperBarAddButtonEvents[0] = False
                    self.UpperBarAddButtonEvents[1] = True
                    pygame.draw.rect(self.screen, (60, 69, 165), self.UpperBarAddButtonR, 0, 4)
                    Alert = ["Add Group Member", [], None, None, None, [False, False], None, None, [False, False], True,
                             [], self.MemberList, self.ID]

                if pygame.mouse.get_pressed()[0] and self.UpperBarAddButtonEvents[0]:
                    pygame.draw.rect(self.screen, (60, 69, 165), self.UpperBarAddButtonR, 0, 4)
                elif Alert != [] and pygame.mouse.get_pressed()[0]:
                    self.UpperBarAddButtonEvents[0] = False
                if pygame.mouse.get_pressed()[0] and not self.UpperBarAddButtonR.collidepoint(
                        pygame.mouse.get_pos()) and not \
                        self.UpperBarAddButtonEvents[0]:
                    self.UpperBarAddButtonEvents[1] = False
                for Member in self.MemberList:
                    if Member.Rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                        Member.TouchEvent[0] = True
                    if Member.Rect.collidepoint(pygame.mouse.get_pos()) and not pygame.mouse.get_pressed()[
                        0] and Member.TouchEvent[0]:
                        Member.TouchEvent[0] = False
                        Member.TouchEvent[1] = True
                        if Member.ID != self.OwnerID:
                            Alert = ["Remove Group Member", self.ID, self.UserID, Member, None, None, [False, False], None,
                                     None, [False, False], True]
                    if pygame.mouse.get_pressed()[0] and Member.TouchEvent[0]:
                        pass
                    elif Alert != [] and pygame.mouse.get_pressed()[0]:
                        Member.TouchEvent[0] = False
                    if pygame.mouse.get_pressed()[0] and not Member.Rect.collidepoint(
                            pygame.mouse.get_pos()) and not \
                            Member.TouchEvent[0]:
                        Member.TouchEvent[1] = False
                    if Member.TouchEvent[1]:
                        break
            elif self.OwnerID != 0:
                if self.LeaveGroupR.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    self.LeaveGroupEvent[0] = True
                    pygame.draw.rect(self.screen, (60, 69, 165), self.LeaveGroupR, 0, 4)
                if self.LeaveGroupR.collidepoint(pygame.mouse.get_pos()) and not pygame.mouse.get_pressed()[
                    0] and self.LeaveGroupEvent[0]:
                    self.LeaveGroupEvent[0] = False
                    self.LeaveGroupEvent[1] = True
                    pygame.draw.rect(self.screen, (60, 69, 165), self.LeaveGroupR, 0, 4)
                    Alert = ["Leave Group", self.ID]
                if pygame.mouse.get_pressed()[0] and self.LeaveGroupEvent[0]:
                    pygame.draw.rect(self.screen, (60, 69, 165), self.LeaveGroupR, 0, 4)
                elif Alert != [] and pygame.mouse.get_pressed()[0]:
                    self.LeaveGroupEvent[0] = False
                if pygame.mouse.get_pressed()[0] and not self.LeaveGroupR.collidepoint(
                        pygame.mouse.get_pos()) and not \
                        self.LeaveGroupEvent[0]:
                    self.LeaveGroupEvent[1] = False

            if self.UploadR.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and not \
                    self.UploadEvents[2]:
                pygame.draw.rect(self.screen, (96, 100, 244), self.Rect, 0, 10)
                self.UploadEvents[0] = True
            if self.UploadEvents[0]:
                pygame.draw.rect(self.screen, (96, 100, 244), self.Rect, 0, 10)
            if self.UploadR.collidepoint(pygame.mouse.get_pos()) and not pygame.mouse.get_pressed()[0] and \
                    self.UploadEvents[0]:
                pygame.draw.rect(self.screen, (96, 100, 244), self.Rect, 0, 10)
                self.UploadEvents[0] = False
                self.UploadEvents[1] = True
                Alert = ["Send File", self.ID, None, None, [False, False], None, None, [False, False], None, None, True,
                         None, None]
            elif not pygame.mouse.get_pressed()[0]:
                self.UploadEvents[0] = False
            if pygame.mouse.get_pressed()[0]:
                self.UploadEvents[2] = True
            else:
                self.UploadEvents[2] = False
            if pygame.Rect(self.screen_size[0] * 3 / 12, 50, self.screen_size[0] * 5 / 8,
                           self.screen_size[1] * 15 / 16 - 60).collidepoint(pygame.mouse.get_pos()) and len(
                self.MassageList) > 4:
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 4:
                            if self.MassageList[0].Rect.top <= 50:
                                for massage in self.MassageList:
                                    massage.Rect.topleft = (massage.Rect.topleft[0], massage.Rect.topleft[1] + 15)
                        if event.button == 5:
                            if self.MassageList[-1].Rect.bottom >= self.screen_size[1] * 15 / 16 - 60:
                                for massage in self.MassageList:
                                    massage.Rect.topleft = (massage.Rect.topleft[0], massage.Rect.topleft[1] - 15)
            if pygame.Rect(self.screen_size[0] * 10.5 / 12, self.screen_size[1] * 1 / 12,
                           self.screen_size[0] * 1.5 / 12,
                           self.screen_size[1]).collidepoint(pygame.mouse.get_pos()) and len(self.MemberList) > 10:
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 4:
                            if self.MemberList[0].Rect.top < self.screen_size[1] * 1 / 12:
                                for massage in self.MemberList:
                                    massage.Rect.topleft = (massage.Rect.topleft[0], massage.Rect.topleft[1] + 10)
                        if event.button == 5:
                            if self.MemberList[-1].Rect.bottom >= self.screen_size[1]:
                                for massage in self.MemberList:
                                    massage.Rect.topleft = (massage.Rect.topleft[0], massage.Rect.topleft[1] - 10)
            if self.TextBar.get_text() != "":
                if not self.TextBox[1]:
                    if self.send_iconR.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and not \
                            self.TextBox[2]:
                        self.TextBox[0] = True
                    if self.TextBox[0]:
                        pass
                    if self.send_iconR.collidepoint(pygame.mouse.get_pos()) and not pygame.mouse.get_pressed()[0] and \
                            self.TextBox[0]:
                        self.TextBox[0] = False
                        self.TextBox[1] = True
                        Client.send_massage(self.TextBar.get_text(), self.ID)
                        self.TextBar.clear_text()

                    elif not pygame.mouse.get_pressed()[0]:
                        self.TextBox[0] = False
                    if pygame.mouse.get_pressed()[0]:
                        self.TextBox[2] = True
                    else:
                        self.TextBox[2] = False
                else:
                    self.TextBox[1] = False
            if pygame.Rect(self.screen_size[0] * 3 / 12 + 70, self.screen_size[1] * 15 / 16 - 10,
                           self.screen_size[0] * 5 / 8 - 140, self.screen_size[1] * 1 / 16 - 10).collidepoint(
                pygame.mouse.get_pos()):
                self.TextBar.update(events2)
            for mass in self.MassageList:
                mass.update()
        return Alert

    """
    renders the group on screen
    """
    def render(self, Left, Top, Width, Height):
        if not self.GroupEvnets[1]:
            if not self.Picture == None:
                if self.Rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(self.screen, (60, 63, 69), self.Rect, 0, 5)
                if self.GroupEvnets[0]:
                    pygame.draw.rect(self.screen, (66, 70, 77), self.Rect, 0, 5)
                self.Picture = pygame.transform.scale(self.Picture, (Height - 2, Height - 2))
                PicR = self.Picture.get_rect()
                PicR.topleft = (Left + 1, Top + 1)
                GroupName = self.wrap_word(self.GroupName, Width - Height)
                Mass = self.font.render(GroupName[0], True, (255, 255, 255))
                MassR = Mass.get_rect()
                Mass2 = self.font.render(f"{str(len(self.MemberList))} Members", True, (255, 255, 255))
                MassR.topleft = (PicR.topright[0] + 3, PicR.topright[1])
                Mass2R = Mass2.get_rect()
                Mass2R.topleft = MassR.bottomleft
                self.screen.blit(self.Picture, PicR)
                self.screen.blit(Mass, MassR)
                self.screen.blit(Mass2, Mass2R)
            else:
                if self.Rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(self.screen, (60, 63, 69), self.Rect, 0, 5)
                if self.GroupEvnets[0]:
                    pygame.draw.rect(self.screen, (66, 70, 77), self.Rect, 0, 5)
                GroupName = self.wrap_word(self.GroupName, Width)
                Mass = self.font.render(GroupName[0], True, (255, 255, 255))
                MassR = Mass.get_rect()
                MassR.topleft = (Left + 1, Top + 1)
                self.screen.blit(Mass, MassR)
        else:
            if not self.Picture == None:
                pygame.draw.rect(self.screen, (66, 70, 77), self.Rect, 0, 5)
                self.Picture = pygame.transform.scale(self.Picture, (Height - 2, Height - 2))
                PicR = self.Picture.get_rect()
                PicR.topleft = (Left + 1, Top + 1)
                GroupName = self.wrap_word(self.GroupName, Width - Height)
                Mass = self.font.render(GroupName[0], True, (255, 255, 255))
                MassR = Mass.get_rect()
                Mass2 = self.font.render(f"{str(len(self.MemberList))} Members", True, (255, 255, 255))
                MassR.topleft = (PicR.topright[0] + 3, PicR.topright[1])
                Mass2R = Mass2.get_rect()
                Mass2R.topleft = MassR.bottomleft
                self.screen.blit(self.Picture, PicR)
                self.screen.blit(Mass, MassR)
                self.screen.blit(Mass2, Mass2R)
            else:
                pygame.draw.rect(self.screen, (66, 70, 77), self.Rect, 0, 5)
                GroupName = self.wrap_word(self.GroupName, Width)
                Mass = self.font.render(GroupName[0], True, (255, 255, 255))
                MassR = Mass.get_rect()
                MassR.topleft = (Left + 1, Top + 1)
                self.screen.blit(Mass, MassR)

            r = pygame.Rect(self.screen_size[0] * 3 / 12, 0, self.screen_size[0] * 5 / 8, self.screen_size[1])
            pygame.draw.rect(self.screen, (54, 57, 63), r)
            r = pygame.Rect(self.screen_size[0] * 10.5 / 12, 0, self.screen_size[0] * 1.5 / 12, self.screen_size[1])
            pygame.draw.rect(self.screen, (47, 49, 54), r)
            for member in self.MemberList:
                member.render(member.Rect.left, member.Rect.top, member.Rect.width, member.Rect.height,
                              background=False)
            for massage in self.MassageList:
                massage.render(massage.Rect.left, massage.Rect.top, massage.Rect.width)
            r = pygame.Rect(self.screen_size[0] * 3 / 12, self.screen_size[1] * 15 / 16 - 10,
                            self.screen_size[0] * 5 / 8, self.screen_size[1] * 1 / 16 + 10)
            pygame.draw.rect(self.screen, (54, 57, 63), r)
            TextBarRect = pygame.Rect(self.screen_size[0] * 3 / 12 + 20, self.screen_size[1] * 15 / 16 - 10,
                                      self.screen_size[0] * 5 / 8 - 40, self.screen_size[1] * 1 / 16 - 10)
            TextMassRect = pygame.Rect(self.screen_size[0] * 3 / 12 + 70, self.screen_size[1] * 15 / 16 - 10,
                                       self.screen_size[0] * 5 / 8 - 140, self.screen_size[1] * 1 / 16 - 10)
            pygame.draw.rect(self.screen, (64, 68, 75), TextBarRect, 0, 5)
            pygame.draw.rect(self.screen, (185, 187, 190), self.UploadR, 0, 5)
            self.screen.blit(self.send_icon, self.send_iconR)
            self.screen.blit(self.Upload, self.UploadR)
            self.TextBar.render(self.screen)
            pygame.draw.rect(self.screen, (47, 49, 54), self.UpperBar)
            self.screen.blit(self.GroupNamet, self.GroupNameR)
            if self.UserID == self.OwnerID:
                pygame.draw.rect(self.screen, (88, 101, 242), self.UpperBarAddButtonR, 0, 4)
                if self.UpperBarAddButtonR.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    pygame.draw.rect(self.screen, (60, 69, 165), self.UpperBarAddButtonR, 0, 4)
                if self.UpperBarAddButtonEvents[0]:
                    pygame.draw.rect(self.screen, (60, 69, 165), self.UpperBarAddButtonR, 0, 4)
                self.screen.blit(self.UpperBarAddButton, self.UpperBarAddButtonR)
            if self.OwnerID != 0 and not self.UserID == self.OwnerID:
                pygame.draw.rect(self.screen, (88, 101, 242), self.LeaveGroupR, 0, 4)
                if self.LeaveGroupR.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    pygame.draw.rect(self.screen, (60, 69, 165), self.LeaveGroupR, 0, 4)
                if self.LeaveGroupEvent[0]:
                    pygame.draw.rect(self.screen, (60, 69, 165), self.LeaveGroupR, 0, 4)
                self.screen.blit(self.LeaveGroup, self.LeaveGroupR)

    def wrap_word(self, word, width):
        wrapped_word = []

        while len(word):
            ## Store as many characters as possible to fit in allowed width
            line_of_char = []
            while len(word):
                line_of_char.append(word[:1])
                word = word[1:]
                fw, fh = self.font.size(''.join(line_of_char + [word[:1]]))

                ## If width exceeds then store remaining characters in new line
                if fw > width:
                    break

            ## Join all characters that fit in width into one line
            final_line = ''.join(line_of_char)
            wrapped_word.append(final_line)

        return wrapped_word

    def pilImageToSurface(self, pilImage):
        return pygame.image.fromstring(
            pilImage.tobytes(), pilImage.size, pilImage.mode).convert()

    def ByteToSurface(self, bytes):
        return self.pilImageToSurface(Image.open(io.BytesIO(bytes)))


class Community:
    def __init__(self, ID, CommunityName, CommunityPicture, Picture, OwnerID, MemberList, CommunityGroups, path,
                 screen_size, font, screen):
        self.ID = ID
        self.CommunityName = CommunityName
        self.CommunityPicture = CommunityPicture
        self.Picture = Picture
        self.OwnerID = OwnerID
        self.MemberList = MemberList
        self.CommunityGroups = CommunityGroups
        self.path = path
        self.screen_size = screen_size
        self.font = font
        self.screen = screen
        self.Load()

    def pilImageToSurface(self, pilImage):
        return pygame.image.fromstring(
            pilImage.tobytes(), pilImage.size, pilImage.mode).convert()

    def ByteToSurface(self, bytes):
        return self.pilImageToSurface(Image.open(io.BytesIO(bytes)))

    def Load(self):
        self.Picture = pygame.transform.scale(self.ByteToSurface(self.Picture), self.screen_size[0] * 1/ 16, self.screen_size[0] * 1/ 16)

    def update(self, events):
        pass

    def render(self, Left, Top, Width, Height):
        self.screen.blit(self.Picture, pygame.Rect(Left, Top, Width, Height))


class PublicCommunity:
    def __init__(self, ID, CommunityName, path, screen_size, font, screen):
        self.ID = ID
        self.CommunityName = CommunityName
        self.path = path
        self.screen_size = screen_size
        self.font = font
        self.screen = screen
        self.Load()

    def Load(self):
        pass
