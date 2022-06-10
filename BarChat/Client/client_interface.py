from bar_chat_client import *
import pygame
from PIL import Image
import io
from text_box import *
from log_in_or_sign_in import *
from datetime import datetime
import time
from tkinter import *
from tkinter import filedialog
from structures import *
import threading

GameName = "Bar Chat"
vocabulary = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPGRSTUVWXYZ1234567890.:,;'\"(!?)+-*/="
Friends_List = []
Groups_List = []
Communities_List = []
PublicCommunities_List = []
Friend_Request_List = []
Alert = []
Add_Group = []
condition = threading.Condition()
My_User = None

"""
this object takes care of making user interface and process it for client server communication
"""


class ClientInterface:
    def __init__(self, screen_size, default_image_path):
        pygame.init()
        self.default_image_path = default_image_path
        self.screen_size = (192 * screen_size, 108 * screen_size)
        self.screen = pygame.display.set_mode((192 * screen_size, 108 * screen_size))
        self.Load_Defualt_Images_Fonts(self.default_image_path)
        pygame.display.set_caption(GameName)
        pygame.display.set_icon(pygame.transform.scale(self.Icon, (32, 32)))
        massage = False
        nextC = "Log_in"
        flag = True
        Incorrect = False
        while not massage:
            log_in = ""
            listD = self.LogIn_or_SignIn([self.default_image_path, Incorrect], nextC)
            if listD[0] == "Log_in":
                log_in = Log_in(self.default_image_path, Incorrect, self.screen_size, self.BlackBox, self.Icon,
                                self.Lato,
                                self.Lato_Clean, self.BackGroundBlob1, self.screen)
            if listD[0] == "Sign_in":
                log_in = Sign_in(listD[3], Incorrect, self.screen_size, self.Lato, self.Lato2, self.Lato_Clean,
                                 self.screen, self.BackGroundBlob2, self.BlackBox)

            log_in.start()
            if flag:
                self.Client = BarChatClient()

            if listD[0] == "Log_in":
                Incorrect = True
                massage = self.Client.Log_in(listD[1], listD[2])
                log_in.Stop()
                nextC = "Log_in"
                flag = False

            if listD[0] == "Sign_in":
                Incorrect = True
                massage = self.Client.IsUserNameUsed(listD[1])
                if not massage:
                    massage = self.Client.Sign_in(listD[1], listD[2], listD[3])
                else:
                    massage = False
                    nextC = "Sign_in"
                    Incorrect = True
                log_in.Stop()
                flag = False
        self.UserID = int(massage)

    """
    create a pygame picture object from bytes
    """

    def pilImageToSurface(self, pilImage):
        return pygame.image.fromstring(
            pilImage.tobytes(), pilImage.size, pilImage.mode).convert()

    """
    create a pygame picture object from bytes
    """

    def ByteToSurface(self, bytes):
        return self.pilImageToSurface(Image.open(io.BytesIO(bytes)))

    """
    creating self values of interface images
    """

    def Load_Defualt_Images_Fonts(self, path):
        self.Icon = pygame.image.load(rf"{path}\Default\012-user-avatar-5.png")
        self.BackGroundBlob1 = pygame.transform.scale(pygame.image.load(rf"{path}\Default\blob-haikei (1).png"),
                                                      self.screen_size)
        self.BackGroundBlob2 = pygame.transform.scale(pygame.image.load(rf"{path}\Default\blob-haikei (2).png"),
                                                      self.screen_size)
        self.BackGroundBlob3 = pygame.transform.scale(pygame.image.load(rf"{path}\Default\stacked-waves-haikei.png"),
                                                      self.screen_size)
        self.BlackBox = pygame.transform.scale(pygame.image.load(rf"{path}\Default\black_box.png"),
                                               (self.screen_size[0] / 1.5, self.screen_size[1] / 1.5))
        self.GroupTheme = pygame.image.load(rf"{path}\Default\017-friends.png")

        self.Lato = pygame.font.Font(rf"{path}\Fonts\Lato\Lato-Black.ttf", 40)
        self.LatoBig = pygame.font.Font(rf"{path}\Fonts\Lato\Lato-Black.ttf", 70)

        self.Lato2 = pygame.font.Font(rf"{path}\Fonts\Lato\Lato-Black.ttf", 28)
        self.Lato3 = pygame.font.Font(rf"{path}\Fonts\Lato\Lato-Black.ttf", 21)
        self.Lato_Clean = pygame.font.Font(rf"{path}\Fonts\Lato\Lato-Regular.ttf", 20)
        self.Lato_Under_Line = pygame.font.Font(rf"{path}\Fonts\Lato\Lato-Regular.ttf", 20)
        self.Default_avatar = pygame.image.load(rf"{path}\Default\001-user-avatar.png").convert_alpha()
        self.Friends_button = pygame.transform.scale(pygame.image.load(rf"{path}\Default\021-avatars.png"), (
            self.screen_size[0] * 1 / 25, self.screen_size[0] * 1 / 25)).convert_alpha()
        self.File_Icon = pygame.image.load(rf"{path}\Default\check-list.png")
        self.Upload = pygame.image.load(rf"{path}\Default\cloud-upload.png")
        self.OwnerIcon = pygame.image.load(rf"{path}\Default\014-user-avatar-6.png")
        self.send_button = pygame.image.load(rf"{path}\Default\left-arrow.png")
        self.Small_Lato = pygame.font.Font(rf"{path}\Fonts\Lato\Lato-Regular.ttf", 20)
        self.Trash = pygame.image.load(rf"{path}\Default\trash-bin.png")
        pygame.font.Font.set_underline(self.Lato_Under_Line, True)

    """
    handle log in or sign in to a user
    """

    def LogIn_or_SignIn(self, path, next):
        while True:
            if next == "Log_in":
                next = self.Log_in(path[0], path[1])
            if next == "Sign_in":
                next = self.Sign_in(path[0], path[1])
            if next != "Log_in" and next != "Sign_in":
                return next

    """
    takes care of getting user info for log in
    """

    def Log_in(self, path, Incorrect):
        User = ""
        Pass = ""
        flag = False
        BlackBoxRect = self.BlackBox.get_rect()
        BlackBoxRect.center = (self.screen_size[0] / 2, self.screen_size[1] / 2)

        Icon = pygame.transform.scale(self.Icon, (300, 300))
        Icon_rect = Icon.get_rect()
        Icon_rect.center = (
            BlackBoxRect.bottomleft[0] + (int(BlackBoxRect.bottomright[0]) - int(BlackBoxRect.bottomleft[0])) * 5 / 6,
            BlackBoxRect.center[1])

        Welcome_Back = self.Lato.render("Welcome back!", True, (255, 255, 255))
        Welcome_BackRect = Welcome_Back.get_rect()
        Welcome_BackRect.center = (
            BlackBoxRect.bottomleft[0] + (int(BlackBoxRect.bottomright[0]) - int(BlackBoxRect.bottomleft[0])) * 1 / 3,
            BlackBoxRect.topleft[1] + (BlackBoxRect.bottomleft[1] - BlackBoxRect.topleft[1]) * 1 / 8)

        Welcome_Back2 = self.Lato_Clean.render("We're happy to see you again!", True, (110, 110, 120))
        Welcome_BackRect2 = Welcome_Back2.get_rect()
        Welcome_BackRect2.center = (
            BlackBoxRect.bottomleft[0] + (int(BlackBoxRect.bottomright[0]) - int(BlackBoxRect.bottomleft[0])) * 1 / 3,
            BlackBoxRect.topleft[1] + (BlackBoxRect.bottomleft[1] - BlackBoxRect.topleft[1]) * 3 / 16)

        SignInMass = self.Lato_Clean.render("First time here? ", True, (110, 110, 120))
        SignInMassRect = SignInMass.get_rect()
        SignInMassRect.topleft = (
            BlackBoxRect.bottomleft[0] + (BlackBoxRect.bottomright[0] - BlackBoxRect.bottomleft[0]) * 1 / 18,
            BlackBoxRect.topleft[1] + (BlackBoxRect.bottomleft[1] - BlackBoxRect.topleft[1]) * 7 / 8)

        SignInMassLink = self.Lato_Clean.render("Sign In", True, (57, 136, 255))
        SignInMassLinkRect = SignInMass.get_rect()
        SignInMassLinkRect.topleft = SignInMassRect.topright

        SignInMassLinkU = self.Lato_Under_Line.render("Sign In", True, (57, 136, 255))
        SignInMassLinkURect = SignInMass.get_rect()
        SignInMassLinkURect.topleft = SignInMassRect.topright
        Pressed_Sign_in = False

        UserName = self.Lato_Clean.render("USERNAME", True, (200, 200, 210))
        UserNameRect = UserName.get_rect()
        UserNameRect.topleft = (SignInMassRect.topleft[0], BlackBoxRect.topleft[1] + (
                BlackBoxRect.bottomleft[1] - BlackBoxRect.topleft[1]) * 1 / 4)
        RawUserName = self.Lato_Clean.render("USERNAME - Must Use 2-32 Chars From 0-9,aA-zZ.:,;'\"(!?)-*/=", True,
                                             (200, 0, 0))
        RawUserNameRect = RawUserName.get_rect()
        RawUserNameRect.topleft = UserNameRect.topleft
        IncorrectUserName = self.Lato_Clean.render("USERNAME - Incorrect password or username", True, (200, 0, 0))
        IncorrectUserNameRect = IncorrectUserName.get_rect()
        IncorrectUserNameRect.topleft = UserNameRect.topleft
        UserNameBar = pygame.Rect(SignInMassRect.topleft[0], UserNameRect.bottomleft[1] + 10, 500, 40)
        UserNameTextBox = TextInputBox(UserNameBar.topleft[0] + 3, UserNameBar.topleft[1] + 2,
                                       font_family=rf"{path}\Fonts\Lato\Lato-Black.ttf", font_size=30, max_width=500,
                                       max_height=40)
        UserNameTextBox.set_cursor_color((56, 52, 60))
        UserNameTextBoxR = pygame.Rect(UserNameBar.topleft[0] + 3, UserNameBar.topleft[1] + 2, 500, 40)
        PassWord = self.Lato_Clean.render("PASSWORD", True, (200, 200, 210))
        PassWordRect = UserName.get_rect()
        PassWordRect.topleft = (UserNameBar.bottomleft[0], UserNameBar.bottomleft[1] + 20)
        RawPassWord = self.Lato_Clean.render("PASSWORD - Must Use 2-32 Chars From 0-9,aA-zZ.:,;'\"(!?)-*/=", True,
                                             (200, 0, 0))
        RawPassWordRect = RawPassWord.get_rect()
        IncorrectPassWord = self.Lato_Clean.render("PASSWORD - Incorrect password or username", True, (200, 0, 0))
        IncorrectPassWordRect = IncorrectPassWord.get_rect()
        IncorrectPassWordRect.topleft = PassWordRect.topleft
        RawPassWordRect.topleft = PassWordRect.topleft
        PassWordBar = pygame.Rect(UserNameBar[0], PassWordRect.bottomleft[1] + 10, UserNameBar[2], UserNameBar[3])
        PassWordTextBox = TextInputBox(PassWordBar.topleft[0] + 3, PassWordBar.topleft[1] + 2,
                                       font_family=rf"{path}\Fonts\Lato\Lato-Black.ttf", font_size=30, max_width=500,
                                       max_height=40, password=True)
        PassWordTextBox.set_cursor_color((56, 52, 60))
        PassWordTextBoxR = pygame.Rect(PassWordBar.topleft[0] + 3, PassWordBar.topleft[1] + 2, 500, 40)

        LogIn = pygame.Rect(UserNameBar[0], PassWordBar.bottomleft[1] + 50, UserNameBar[2], UserNameBar[3])
        Pressed_Log_In = False
        LogInMass = self.Lato_Clean.render("Login", True, (255, 255, 255))
        LogInMassR = LogInMass.get_rect()
        LogInMassR.center = LogIn.center
        ENTER = False
        WriteUser = False
        WritePass = False
        while True:
            ENTER = False

            events = pygame.event.get()
            try:
                self.Check_If_Close(events)
            except Exception as e:
                print(e)
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        ENTER = True

            if not UserNameTextBoxR.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                WriteUser = False
                UserNameTextBox.set_cursor_color((56, 52, 60))

            if not PassWordTextBoxR.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                WritePass = False
                PassWordTextBox.set_cursor_color((56, 52, 60))
            self.screen.blit(self.BackGroundBlob1, (0, 0))
            self.screen.blit(self.BlackBox, BlackBoxRect)
            self.screen.blit(Icon, Icon_rect)
            self.screen.blit(Welcome_Back, Welcome_BackRect)
            self.screen.blit(Welcome_Back2, Welcome_BackRect2)
            self.screen.blit(SignInMass, SignInMassRect)
            self.screen.blit(UserName, UserNameRect)
            self.screen.blit(PassWord, PassWordRect)

            pygame.draw.rect(self.screen, (56, 52, 60), UserNameBar, 0, 4)
            pygame.draw.rect(self.screen, (40, 37, 41), UserNameBar, 1, 4)
            if WriteUser:
                pygame.draw.rect(self.screen, (57, 136, 255), UserNameBar, 1, 4)
            elif UserNameBar.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(self.screen, (6, 6, 7), UserNameBar, 1, 4)

            pygame.draw.rect(self.screen, (96, 100, 244), LogIn, 0, 4)
            if LogIn.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(self.screen, (72, 84, 196), LogIn, 0, 4)

            pygame.draw.rect(self.screen, (56, 52, 60), PassWordBar, 0, 4)
            pygame.draw.rect(self.screen, (40, 37, 41), PassWordBar, 1, 4)
            if WritePass:
                pygame.draw.rect(self.screen, (57, 136, 255), PassWordBar, 1, 4)
            elif PassWordBar.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(self.screen, (6, 6, 7), PassWordBar, 1, 4)

            if not SignInMassLinkRect.collidepoint(pygame.mouse.get_pos()):
                self.screen.blit(SignInMassLink, SignInMassLinkRect)
            else:
                self.screen.blit(SignInMassLinkU, SignInMassLinkURect)

            if LogIn.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                pygame.draw.rect(self.screen, (64, 68, 164), LogIn, 0, 4)
                Pressed_Log_In = True
            if Pressed_Log_In:
                pygame.draw.rect(self.screen, (64, 68, 164), LogIn, 0, 4)
            if LogIn.collidepoint(pygame.mouse.get_pos()) and not pygame.mouse.get_pressed()[0] and Pressed_Log_In:
                pygame.draw.rect(self.screen, (64, 68, 164), LogIn, 0, 4)
                test = self.CheckIfValid(UserNameTextBox.get_text(), PassWordTextBox.get_text())
                if test[0] and test[1]:
                    User = UserNameTextBox.get_text()
                    UserNameTextBox.clear_text()
                    Pass = PassWordTextBox.get_text()
                    PassWordTextBox.clear_text()
                    flag = True
                if not test[0]:
                    UserName = RawUserName
                    UserNameRect = RawUserNameRect
                if not test[1]:
                    PassWord = RawPassWord
                    PassWordRect = RawPassWordRect
                Pressed_Log_In = False
            elif not pygame.mouse.get_pressed()[0]:
                Pressed_Log_In = False
            self.screen.blit(LogInMass, LogInMassR)

            if (UserNameTextBoxR.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]) or WriteUser:
                WriteUser = True
                UserNameTextBox.set_cursor_color((255, 255, 255))
                if ENTER:
                    pygame.draw.rect(self.screen, (64, 68, 164), LogIn, 0, 4)
                    test = self.CheckIfValid(UserNameTextBox.get_text(), PassWordTextBox.get_text())
                    if test[0] and test[1]:
                        User = UserNameTextBox.get_text()
                        UserNameTextBox.clear_text()
                        Pass = PassWordTextBox.get_text()
                        PassWordTextBox.clear_text()
                        flag = True
                    if not test[0]:
                        UserName = RawUserName
                        UserNameRect = RawUserNameRect
                    if not test[1]:
                        PassWord = RawPassWord
                        PassWordRect = RawPassWordRect
                else:
                    UserNameTextBox.update(events)

            if (PassWordTextBoxR.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]) or WritePass:
                WritePass = True
                PassWordTextBox.set_cursor_color((255, 255, 255))
                if ENTER:
                    pygame.draw.rect(self.screen, (64, 68, 164), LogIn, 0, 4)
                    test = self.CheckIfValid(UserNameTextBox.get_text(), PassWordTextBox.get_text())
                    if test[0] and test[1]:
                        User = UserNameTextBox.get_text()
                        UserNameTextBox.clear_text()
                        Pass = PassWordTextBox.get_text()
                        PassWordTextBox.clear_text()
                        flag = True
                    if not test[0]:
                        UserName = RawUserName
                        UserNameRect = RawUserNameRect
                    if not test[1]:
                        PassWord = RawPassWord
                        PassWordRect = RawPassWordRect
                else:
                    PassWordTextBox.update(events)

            if UserName != RawUserName and Incorrect:
                self.screen.blit(IncorrectUserName, IncorrectUserNameRect)
                pygame.draw.rect(self.screen, (200, 0, 0), UserNameBar, 1, 4)
            elif UserName == RawUserName:
                pygame.draw.rect(self.screen, (200, 0, 0), UserNameBar, 1, 4)
            if PassWord != RawPassWord and Incorrect:
                self.screen.blit(IncorrectPassWord, IncorrectPassWordRect)
                pygame.draw.rect(self.screen, (200, 0, 0), PassWordBar, 1, 4)
            elif PassWord == RawPassWord:
                pygame.draw.rect(self.screen, (200, 0, 0), PassWordBar, 1, 4)

            if SignInMassLinkRect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[
                0]: Pressed_Sign_in = True
            if Pressed_Sign_in and SignInMassLinkRect.collidepoint(pygame.mouse.get_pos()) and not \
                    pygame.mouse.get_pressed()[0]:
                return "Sign_in"
            elif not pygame.mouse.get_pressed()[0]:
                Pressed_Sign_in = False
            PassWordTextBox.render(self.screen)
            UserNameTextBox.render(self.screen)
            pygame.display.update()
            if flag:
                return ("Log_in", User, Pass)

    """
    takes care of getting new user info for sign in
    """

    def Sign_in(self, path, Incorrect):
        User = ""
        Pass = ""
        flag = False
        self.new_File = ""
        self.Picture_Path = fr"{path}\Default\001-user-avatar.png"
        BlackBoxRect = self.BlackBox.get_rect()
        BlackBoxRect.center = (self.screen_size[0] / 2, self.screen_size[1] / 2)

        Icon = pygame.transform.scale(self.Default_avatar, (300, 300))
        Icon_rect = Icon.get_rect()
        Icon_rect.center = (
            BlackBoxRect.bottomleft[0] + (int(BlackBoxRect.bottomright[0]) - int(BlackBoxRect.bottomleft[0])) * 5 / 6,
            BlackBoxRect.center[1])

        Welcome_Back = self.Lato.render("Create an account", True, (255, 255, 255))
        Welcome_BackRect = Welcome_Back.get_rect()
        Welcome_BackRect.center = (
            BlackBoxRect.bottomleft[0] + (int(BlackBoxRect.bottomright[0]) - int(BlackBoxRect.bottomleft[0])) * 1 / 3,
            BlackBoxRect.topleft[1] + (BlackBoxRect.bottomleft[1] - BlackBoxRect.topleft[1]) * 1 / 8)

        Welcome_Back2 = self.Lato_Clean.render("Have fun in Bar Chat!", True, (110, 110, 120))
        Welcome_BackRect2 = Welcome_Back2.get_rect()
        Welcome_BackRect2.center = (
            BlackBoxRect.bottomleft[0] + (int(BlackBoxRect.bottomright[0]) - int(BlackBoxRect.bottomleft[0])) * 1 / 3,
            BlackBoxRect.topleft[1] + (BlackBoxRect.bottomleft[1] - BlackBoxRect.topleft[1]) * 3 / 16)

        SignInMass = self.Lato_Clean.render("Already have an account? ", True, (110, 110, 120))
        SignInMassRect = SignInMass.get_rect()
        SignInMassRect.topleft = (
            BlackBoxRect.bottomleft[0] + (BlackBoxRect.bottomright[0] - BlackBoxRect.bottomleft[0]) * 1 / 18,
            BlackBoxRect.topleft[1] + (BlackBoxRect.bottomleft[1] - BlackBoxRect.topleft[1]) * 7 / 8)

        SignInMassLink = self.Lato_Clean.render("Log In", True, (57, 136, 255))
        SignInMassLinkRect = SignInMass.get_rect()
        SignInMassLinkRect.topleft = SignInMassRect.topright

        SignInMassLinkU = self.Lato_Under_Line.render("Log In", True, (57, 136, 255))
        SignInMassLinkURect = SignInMass.get_rect()
        SignInMassLinkURect.topleft = SignInMassRect.topright
        Pressed_Sign_in = False

        UserName = self.Lato_Clean.render("USERNAME", True, (200, 200, 210))
        UserNameRect = UserName.get_rect()
        UserNameRect.topleft = (SignInMassRect.topleft[0], BlackBoxRect.topleft[1] + (
                BlackBoxRect.bottomleft[1] - BlackBoxRect.topleft[1]) * 1 / 4)
        RawUserName = self.Lato_Clean.render("USERNAME - Must Use 2-32 Chars From 0-9,aA-zZ.:,;'\"(!?)-*/=", True,
                                             (200, 0, 0))
        RawUserNameRect = RawUserName.get_rect()
        RawUserNameRect.topleft = UserNameRect.topleft
        IncorrectUserName = self.Lato_Clean.render("USERNAME -  UserName is taken", True, (200, 0, 0))
        IncorrectUserNameRect = IncorrectUserName.get_rect()
        IncorrectUserNameRect.topleft = UserNameRect.topleft
        UserNameBar = pygame.Rect(SignInMassRect.topleft[0], UserNameRect.bottomleft[1] + 10, 500, 40)
        UserNameTextBox = TextInputBox(UserNameBar.topleft[0] + 3, UserNameBar.topleft[1] + 2,
                                       font_family=rf"{path}\Fonts\Lato\Lato-Black.ttf", font_size=30, max_width=500,
                                       max_height=40)
        UserNameTextBox.set_cursor_color((56, 52, 60))
        UserNameTextBoxR = pygame.Rect(UserNameBar.topleft[0] + 3, UserNameBar.topleft[1] + 2, 500, 40)
        PassWord = self.Lato_Clean.render("PASSWORD", True, (200, 200, 210))
        PassWordRect = UserName.get_rect()
        PassWordRect.topleft = (UserNameBar.bottomleft[0], UserNameBar.bottomleft[1] + 20)
        RawPassWord = self.Lato_Clean.render("PASSWORD - Must Use 2-32 Chars From 0-9,aA-zZ.:,;'\"(!?)-*/=", True,
                                             (200, 0, 0))
        RawPassWordRect = RawPassWord.get_rect()

        RawPassWordRect.topleft = PassWordRect.topleft
        PassWordBar = pygame.Rect(UserNameBar[0], PassWordRect.bottomleft[1] + 10, UserNameBar[2], UserNameBar[3])
        PassWordTextBox = TextInputBox(PassWordBar.topleft[0] + 3, PassWordBar.topleft[1] + 2,
                                       font_family=rf"{path}\Fonts\Lato\Lato-Black.ttf", font_size=30, max_width=500,
                                       max_height=40, password=True)
        PassWordTextBox.set_cursor_color((56, 52, 60))
        PassWordTextBoxR = pygame.Rect(PassWordBar.topleft[0] + 3, PassWordBar.topleft[1] + 2, 500, 40)

        PassWordBar2 = pygame.Rect(UserNameBar[0], PassWordRect.bottomleft[1] + 70, UserNameBar[2], UserNameBar[3])
        PassWordTextBox2 = TextInputBox(PassWordBar2.topleft[0] + 3, PassWordBar2.topleft[1] + 2,
                                        font_family=rf"{path}\Fonts\Lato\Lato-Black.ttf", font_size=30, max_width=500,
                                        max_height=40, password=True)
        PassWordTextBoxR2 = pygame.Rect(PassWordBar2.topleft[0] + 3, PassWordBar2.topleft[1] + 2, 500, 40)
        PassWordTextBox2.set_cursor_color((56, 52, 60))

        Change_Button = pygame.Rect(Icon_rect.bottomleft[0], SignInMassLinkRect.topleft[1], 130, 50)
        Change_Button.bottomleft = (Icon_rect.bottomleft[0], SignInMassLinkRect.bottomleft[1])
        Change_Button_Mass = self.Lato2.render("Change", True, (255, 255, 255))
        Change_Button_MassR = Change_Button_Mass.get_rect()
        Change_Button_MassR.center = Change_Button.center

        Clear_Button = pygame.Rect(Icon_rect.bottomleft[0], SignInMassLinkRect.topleft[1], 130, 50)
        Clear_Button.bottomright = (Icon_rect.bottomright[0], SignInMassLinkRect.bottomleft[1])
        Clear_Button_Mass = self.Lato2.render("Clear", True, (255, 255, 255))
        Clear_Button_MassR = Clear_Button_Mass.get_rect()
        Clear_Button_MassR.center = Clear_Button.center

        LogIn = pygame.Rect(UserNameBar[0], PassWordBar.bottomleft[1] + 90, UserNameBar[2], UserNameBar[3])
        Pressed_Log_In = False
        Pressed_Change = False
        Pressed_Clear = False
        LogInMass = self.Lato_Clean.render("Register", True, (255, 255, 255))
        LogInMassR = LogInMass.get_rect()
        LogInMassR.center = LogIn.center
        ENTER = False
        WriteUser = False
        WritePass = False
        WritePass2 = False
        while True:
            ENTER = False

            events = pygame.event.get()
            try:
                self.Check_If_Close(events)
            except Exception as e:
                print(e)
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        ENTER = True

            if not UserNameTextBoxR.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                WriteUser = False
                UserNameTextBox.set_cursor_color((56, 52, 60))

            if not PassWordTextBoxR.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                WritePass = False
                PassWordTextBox.set_cursor_color((56, 52, 60))
            if not PassWordTextBoxR2.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                WritePass2 = False
                PassWordTextBox2.set_cursor_color((56, 52, 60))
            self.screen.blit(self.BackGroundBlob2, (0, 0))
            self.screen.blit(self.BlackBox, BlackBoxRect)
            self.screen.blit(Icon, Icon_rect)
            self.screen.blit(Welcome_Back, Welcome_BackRect)
            self.screen.blit(Welcome_Back2, Welcome_BackRect2)
            self.screen.blit(SignInMass, SignInMassRect)
            self.screen.blit(UserName, UserNameRect)
            self.screen.blit(PassWord, PassWordRect)

            pygame.draw.rect(self.screen, (56, 52, 60), UserNameBar, 0, 4)
            pygame.draw.rect(self.screen, (40, 37, 41), UserNameBar, 1, 4)
            if WriteUser:
                pygame.draw.rect(self.screen, (57, 136, 255), UserNameBar, 1, 4)
            elif UserNameBar.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(self.screen, (6, 6, 7), UserNameBar, 1, 4)

            pygame.draw.rect(self.screen, (96, 100, 244), LogIn, 0, 4)
            if LogIn.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(self.screen, (72, 84, 196), LogIn, 0, 4)

            pygame.draw.rect(self.screen, (56, 52, 60), PassWordBar, 0, 4)
            pygame.draw.rect(self.screen, (40, 37, 41), PassWordBar, 1, 4)
            if WritePass:
                pygame.draw.rect(self.screen, (57, 136, 255), PassWordBar, 1, 4)
            elif PassWordBar.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(self.screen, (6, 6, 7), PassWordBar, 1, 4)

            pygame.draw.rect(self.screen, (56, 52, 60), PassWordBar2, 0, 4)
            pygame.draw.rect(self.screen, (40, 37, 41), PassWordBar2, 1, 4)
            if WritePass2:
                pygame.draw.rect(self.screen, (57, 136, 255), PassWordBar2, 1, 4)
            elif PassWordBar2.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(self.screen, (6, 6, 7), PassWordBar2, 1, 4)

            if not SignInMassLinkRect.collidepoint(pygame.mouse.get_pos()):
                self.screen.blit(SignInMassLink, SignInMassLinkRect)
            else:
                self.screen.blit(SignInMassLinkU, SignInMassLinkURect)

            pygame.draw.rect(self.screen, (240, 68, 68), Clear_Button, 0, 4)
            if Clear_Button.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(self.screen, (200, 52, 52), Clear_Button, 0, 4)

            if Clear_Button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[
                0] and not Pressed_Change and not Pressed_Log_In:
                pygame.draw.rect(self.screen, (168, 44, 44), Clear_Button, 0, 4)
                Pressed_Clear = True
            if Pressed_Clear and not Pressed_Change and not Pressed_Log_In:
                pygame.draw.rect(self.screen, (168, 44, 44), Clear_Button, 0, 4)

            if Clear_Button.collidepoint(pygame.mouse.get_pos()) and not pygame.mouse.get_pressed()[
                0] and Pressed_Clear and not Pressed_Change and not Pressed_Log_In:
                pygame.draw.rect(self.screen, (168, 44, 44), Change_Button, 0, 4)
                Icon = pygame.transform.scale(self.Default_avatar, (300, 300))
                Icon_rect = Icon.get_rect()
                Icon_rect.center = (
                    BlackBoxRect.bottomleft[0] + (
                            int(BlackBoxRect.bottomright[0]) - int(BlackBoxRect.bottomleft[0])) * 5 / 6,
                    BlackBoxRect.center[1])
                self.Picture_Path = rf"{path}\Default\001-user-avatar.png"
                self.new_File = ""
                Pressed_Clear = False
            elif not pygame.mouse.get_pressed()[0]:
                Pressed_Clear = False
            self.screen.blit(Clear_Button_Mass, Clear_Button_MassR)

            pygame.draw.rect(self.screen, (96, 100, 244), Change_Button, 0, 4)
            if Change_Button.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(self.screen, (72, 84, 196), Change_Button, 0, 4)

            if Change_Button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[
                0] and not Pressed_Clear and not Pressed_Log_In:
                pygame.draw.rect(self.screen, (64, 68, 164), Change_Button, 0, 4)
                Pressed_Change = True
            if Pressed_Change and not Pressed_Clear and not Pressed_Log_In:
                pygame.draw.rect(self.screen, (64, 68, 164), Change_Button, 0, 4)

            if Change_Button.collidepoint(pygame.mouse.get_pos()) and not pygame.mouse.get_pressed()[
                0] and Pressed_Change and not Pressed_Clear and not Pressed_Log_In:
                pygame.draw.rect(self.screen, (64, 68, 164), Change_Button, 0, 4)
                self.window = Tk()
                button = Button(text="Open File", command=self.openFile)
                button.pack()
                self.window.mainloop()
                Pressed_Change = False
            elif not pygame.mouse.get_pressed()[0]:
                Pressed_Change = False
            self.screen.blit(Change_Button_Mass, Change_Button_MassR)

            if LogIn.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[
                0] and not Pressed_Change and not Pressed_Clear:
                pygame.draw.rect(self.screen, (64, 68, 164), LogIn, 0, 4)
                Pressed_Log_In = True
            if Pressed_Log_In and not Pressed_Change and not Pressed_Clear:
                pygame.draw.rect(self.screen, (64, 68, 164), LogIn, 0, 4)

            if LogIn.collidepoint(pygame.mouse.get_pos()) and not pygame.mouse.get_pressed()[
                0] and Pressed_Log_In and not Pressed_Change and not Pressed_Clear:
                pygame.draw.rect(self.screen, (64, 68, 164), LogIn, 0, 4)
                test = self.CheckIfValidSign(UserNameTextBox.get_text(), PassWordTextBox.get_text(),
                                             PassWordTextBox2.get_text())
                if test[0] and test[1]:
                    User = UserNameTextBox.get_text()
                    UserNameTextBox.clear_text()
                    Pass = PassWordTextBox.get_text()
                    PassWordTextBox.clear_text()
                    PassWordTextBox2.clear_text()
                    flag = True
                if not test[0]:
                    UserName = RawUserName
                    UserNameRect = RawUserNameRect
                if not test[1]:
                    PassWord = RawPassWord
                    PassWordRect = RawPassWordRect
                Pressed_Log_In = False
            elif not pygame.mouse.get_pressed()[0]:
                Pressed_Log_In = False
            self.screen.blit(LogInMass, LogInMassR)
            if (UserNameTextBoxR.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]) or WriteUser:
                WriteUser = True
                UserNameTextBox.set_cursor_color((255, 255, 255))
                if ENTER:
                    pygame.draw.rect(self.screen, (64, 68, 164), LogIn, 0, 4)
                    test = self.CheckIfValidSign(UserNameTextBox.get_text(), PassWordTextBox.get_text(),
                                                 PassWordTextBox2.get_text())
                    if test[0] and test[1]:
                        User = UserNameTextBox.get_text()
                        UserNameTextBox.clear_text()
                        Pass = PassWordTextBox.get_text()
                        PassWordTextBox.clear_text()
                        PassWordTextBox2.clear_text()
                        flag = True
                    if not test[0]:
                        UserName = RawUserName
                        UserNameRect = RawUserNameRect
                    if not test[1]:
                        PassWord = RawPassWord
                        PassWordRect = RawPassWordRect
                else:
                    UserNameTextBox.update(events)

            if (PassWordTextBoxR.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]) or WritePass:
                WritePass = True
                PassWordTextBox.set_cursor_color((255, 255, 255))
                if ENTER:
                    pygame.draw.rect(self.screen, (64, 68, 164), LogIn, 0, 4)
                    test = self.CheckIfValidSign(UserNameTextBox.get_text(), PassWordTextBox.get_text(),
                                                 PassWordTextBox2.get_text())
                    if test[0] and test[1]:
                        User = UserNameTextBox.get_text()
                        UserNameTextBox.clear_text()
                        Pass = PassWordTextBox.get_text()
                        PassWordTextBox.clear_text()
                        PassWordTextBox2.clear_text()
                        flag = True
                    if not test[0]:
                        UserName = RawUserName
                        UserNameRect = RawUserNameRect
                    if not test[1]:
                        PassWord = RawPassWord
                        PassWordRect = RawPassWordRect
                else:
                    PassWordTextBox.update(events)

            if (PassWordTextBoxR2.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]) or WritePass2:
                WritePass2 = True
                PassWordTextBox2.set_cursor_color((255, 255, 255))
                if ENTER:
                    pygame.draw.rect(self.screen, (64, 68, 164), LogIn, 0, 4)
                    test = self.CheckIfValidSign(UserNameTextBox.get_text(), PassWordTextBox.get_text(),
                                                 PassWordTextBox2.get_text())
                    if test[0] and test[1]:
                        User = UserNameTextBox.get_text()
                        UserNameTextBox.clear_text()
                        Pass = PassWordTextBox.get_text()
                        PassWordTextBox.clear_text()
                        PassWordTextBox2.clear_text()
                        flag = True
                    if not test[0]:
                        UserName = RawUserName
                        UserNameRect = RawUserNameRect
                    if not test[1]:
                        PassWord = RawPassWord
                        PassWordRect = RawPassWordRect
                else:
                    PassWordTextBox2.update(events)

            if UserName != RawUserName and Incorrect:
                self.screen.blit(IncorrectUserName, IncorrectUserNameRect)
                pygame.draw.rect(self.screen, (200, 0, 0), UserNameBar, 1, 4)
            elif UserName == RawUserName:
                pygame.draw.rect(self.screen, (200, 0, 0), UserNameBar, 1, 4)
            if PassWord == RawPassWord:
                pygame.draw.rect(self.screen, (200, 0, 0), PassWordBar, 1, 4)
                pygame.draw.rect(self.screen, (200, 0, 0), PassWordBar2, 1, 4)

            if SignInMassLinkRect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[
                0]: Pressed_Sign_in = True
            if Pressed_Sign_in and SignInMassLinkRect.collidepoint(pygame.mouse.get_pos()) and not \
                    pygame.mouse.get_pressed()[0]:
                return "Log_in"
            elif not pygame.mouse.get_pressed()[0]:
                Pressed_Sign_in = False
            PassWordTextBox.render(self.screen)
            UserNameTextBox.render(self.screen)
            PassWordTextBox2.render(self.screen)
            pygame.display.update()
            if self.new_File != "":
                self.Picture_Path = self.new_File
                Icon = pygame.transform.smoothscale(pygame.image.load(self.Picture_Path), (300, 300))
            if flag:
                return ("Sign_in", User, Pass, self.Picture_Path)

    def Close(self):
        quit()

    def IsString(self, String):
        for Char in String:
            if Char not in vocabulary:
                return False
        return True

    def CheckIfValid(self, UserName, PassWord):
        l = [False, False]
        if len(UserName) >= 2 and len(UserName) <= 32 and self.IsString(UserName):
            l[0] = True
        if len(PassWord) >= 2 and len(PassWord) <= 32 and self.IsString(PassWord):
            l[1] = True
        return l

    def CheckIfValidSign(self, UserName, PassWord, PassWord2):
        l = [False, False]
        if len(UserName) >= 2 and len(UserName) <= 32 and self.IsString(UserName):
            l[0] = True
        if len(PassWord) >= 2 and len(PassWord) <= 32 and self.IsString(PassWord) and PassWord2 == PassWord:
            l[1] = True
        return l

    def Check_If_Close(self, events):
        try:
            for event in events:
                if event.type == pygame.QUIT:
                    self.Close()
        except Exception as e:
            print()

    """
    the function is creating a filedialog button which is selecting a file and sets new_File value to its path
    """

    def openFile(self):

        self.new_File = filedialog.askopenfilename(initialdir="C:\\Users\\Bar\\",
                                                   title="Open file okay?",
                                                   filetypes=(("png", "*.png"),
                                                              ("jpg", "*.jpg")))
        self.window.destroy()

    """
    makeing graphic interface for user and communicate with server
    """

    def run(self):
        self.new_File = ""
        global Friends_List, Groups_List, Communities_List, Alert
        t = Loading(self.Icon, self.BackGroundBlob3, self.Lato, self.screen_size, self.screen)
        t.start()
        self.Client.Finish_Log_In()
        print(self.UserID)
        Data = self.Client.Load_Data(self.UserID)
        self.Client.UserID = self.UserID
        My_User = User(self.UserID, Data[0][0], Data[0][1], Data[0][2], self.default_image_path, self.screen_size,
                       self.Lato,
                       self.screen)
        for friend in Data[1]:
            self.Add_Friend(friend[0], friend[1], friend[2], friend[3])
        for group in Data[2]:
            self.Add_Group(group[0][0], group[0][1], group[0][2], group[0][3], group[0][4], group[1], group[2])
        for community in Data[3]:
            self.Add_Community(community[0][0], community[0][1], community[0][2], community[0][3], community[0][4],
                               community[1], community[2])
        for Community in Data[4]:
            self.Add_PublicCommunity(Community[0], Community[1])
        t.RUN = False
        self.FriendsLoad(self.screen_size[0] * 3 / 12 + 3, 20,
                         self.screen_size[0] * 5.5 / 12, self.screen_size[1] * 2 / 16)

        self.GroupsLoad(2 + self.screen_size[0] * 1 / 25, 80)
        self.LoadAddGroupButton()
        self.Client.OpenListener()
        self.Listener = Listener(self.Client.Client, self.Client.Key, self.default_image_path, self.screen_size,
                                 self.Lato2, self.screen, self.Lato3, self.File_Icon, self.Small_Lato, self.Lato,
                                 self.Default_avatar, self.OwnerIcon, self.send_button, self.Upload, self.UserID)
        self.Listener.start()
        while True:
            events = pygame.event.get()
            events2 = events.copy()
            events3 = events.copy()
            events4 = events.copy()
            self.Close_event(events)
            self.screen.fill((32, 34, 37))
            if Alert == []:
                self.AddGroupButtonEvents()
                if Alert == []:
                    self.FriendsEvent(events)
                    if Alert == []:
                        Alert = self.GroupsEvents(events2)
                        self.FriendRequestsUpdate(events3, My_User)

            self.GroupsRender(2 + self.screen_size[0] * 1 / 25, 0)
            self.FriendsRender(self.screen_size[0] * 3 / 12, 0)
            self.FriendRequestsRender()
            self.Alert_screen(events4)
            self.RenderAddGroupButton(50 + self.screen_size[0] * 1 / 25, 10)
            My_User.render(0, self.screen_size[1] * 15 / 16, self.screen_size[0] * 3 / 12,
                           self.screen_size[1] * 1 / 16)
            pygame.display.update()

    def LoadAddGroupButton(self):
        global Add_Group
        Add_Group = [self.Lato.render("New Group", True, (59, 165, 93)),
                     self.Lato.render("New Group", True, (255, 255, 255)).get_rect(),
                     self.Lato.render("New Group", True, (54, 57, 63)), [False, False], (54, 57, 63)]

    def AddGroupButtonEvents(self):
        global Add_Group, Alert
        temp = None
        if Add_Group[1].collidepoint(pygame.mouse.get_pos()):
            Add_Group[0] = self.Lato.render("New Group", True, (54, 57, 63))
            Add_Group[-1] = (59, 165, 93)
        elif not Add_Group[3][0]:
            Add_Group[0] = self.Lato.render("New Group", True, (59, 165, 93))
            Add_Group[-1] = (54, 57, 63)
        if Add_Group[1].collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            Add_Group[3][0] = True
            Add_Group[0] = self.Lato.render("New Group", True, (54, 57, 63))
            Add_Group[-1] = (59, 165, 93)
        if Add_Group[1].collidepoint(pygame.mouse.get_pos()) and not pygame.mouse.get_pressed()[
            0] and Add_Group[3][0]:
            Add_Group[3][0] = False
            Add_Group[3][1] = True

            Height = self.screen_size[1] * 2 / 16
            Top = 100
            tempL = []
            for x in Friends_List:
                tempL.append(
                    [x[0], pygame.Rect(self.screen_size[0] * 3 / 12 + 400, Top + 10, self.screen_size[0] * 5.5 / 12,
                                       self.screen_size[1] * 2 / 16), [False, False]])
                Top += Height + 3
            Alert = ["Add Group", tempL, None, None, [False, False], None, None, [False, False], None, None, None, True,
                     None, None, None, None, None, None, None, None]
        if pygame.mouse.get_pressed()[0] and Add_Group[3][0]:
            Add_Group[0] = self.Lato.render("New Group", True, (54, 57, 63))
            Add_Group[-1] = (59, 165, 93)
        elif pygame.mouse.get_pressed()[0]:
            Add_Group[0] = self.Lato.render("New Group", True, (59, 165, 93))
            Add_Group[-1] = (54, 57, 63)
            Add_Group[3][0] = False
        if pygame.mouse.get_pressed()[0] and not Add_Group[1].collidepoint(pygame.mouse.get_pos()) and not Add_Group[3][
            0]:
            Add_Group[-1] = (54, 57, 63)
            Add_Group[0] = self.Lato.render("New Group", True, (59, 165, 93))
            Add_Group[3][1] = False

    def RenderAddGroupButton(self, left, top):
        global Add_Group
        Add_Group[1].topleft = (left, top)
        pygame.draw.rect(self.screen, Add_Group[-1], Add_Group[1], 0, 4)
        self.screen.blit(Add_Group[0], Add_Group[1])

    """
    this function handle pressing buttons for sending data to server
    """

    def Alert_screen(self, events):
        global Alert, Groups_List
        if Alert != []:
            # Alert = ["Friend", friend[0], None, None, [False, False],None, None,[False, False], True, Rect] לתקןןןןןןןןןןןןןןןןןןן
            if Alert[0] == "Friend" and Alert[8]:
                Alert[2] = self.LatoBig.render("Delete", True, (255, 255, 255))
                Alert[3] = Alert[2].get_rect()
                Alert[3].midleft = (Alert[9].midleft[0] + 2, Alert[9].midleft[1])
                Alert[5] = pygame.transform.scale(self.Trash, (self.screen_size[1] * 2 / 16 - 20,
                                                               self.screen_size[1] * 2 / 16 - 20))
                Alert[6] = Alert[5].get_rect()
                Alert[6].midright = (Alert[9].midright[0] - 5, Alert[9].midright[1])
                Alert[8] = False

            elif Alert != [] and Alert[0] == "Friend" and not Alert[8]:
                pygame.draw.rect(self.screen, (66, 70, 77), Alert[9], 0, 4)
                self.screen.blit(Alert[5], Alert[6])
                if Alert != []:
                    pygame.draw.rect(self.screen, (216, 60, 62), Alert[3], 0, 4)
                if Alert != [] and Alert[3].collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    Alert[4][0] = True
                    pygame.draw.rect(self.screen, (149, 42, 43), Alert[3], 0, 4)
                if Alert != [] and Alert[3].collidepoint(pygame.mouse.get_pos()) and not pygame.mouse.get_pressed()[
                    0] and Alert[4][0]:
                    Alert[4][0] = False
                    Alert[4][1] = True
                    pygame.draw.rect(self.screen, (149, 42, 43), Alert[3], 0, 4)
                    self.RemoveFriend(Alert[1])
                    Alert = []
                if Alert != [] and pygame.mouse.get_pressed()[0] and Alert[4][0]:
                    pygame.draw.rect(self.screen, (149, 42, 43), Alert[3], 0, 4)
                elif Alert != [] and pygame.mouse.get_pressed()[0]:
                    Alert[4][0] = False
                if Alert != [] and pygame.mouse.get_pressed()[0] and not Alert[3].collidepoint(
                        pygame.mouse.get_pos()) and not \
                        Alert[4][0]:
                    Alert[4][1] = False

                if Alert != [] and Alert[6].collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    Alert[7][0] = True
                if Alert != [] and Alert[6].collidepoint(pygame.mouse.get_pos()) and not pygame.mouse.get_pressed()[
                    0] and Alert[7][0]:
                    Alert[7][0] = False
                    Alert[7][1] = True
                    Alert = []
                if Alert != [] and pygame.mouse.get_pressed()[0] and Alert[6][0]:
                    pass
                elif Alert != [] and pygame.mouse.get_pressed()[0]:
                    Alert[7][0] = False
                if Alert != [] and pygame.mouse.get_pressed()[0] and not Alert[6].collidepoint(
                        pygame.mouse.get_pos()) and not \
                        Alert[7][0]:
                    Alert[7][1] = False
                if Alert != []:
                    self.screen.blit(Alert[2], Alert[3])




            elif Alert[0] == "Send File" and Alert[10]:
                Alert[10] = False
                self.window = Tk()
                button = Button(text="Open File", command=self.OpenAnyFile)
                button.pack()
                self.window.mainloop()
                if self.new_File == "":
                    Alert = []
                else:
                    if self.new_File[-4::] in [".jpg", ".png"]:
                        Picture = pygame.image.load(self.new_File)
                        z = Picture.get_rect().height / Picture.get_rect().width
                        Picture = pygame.transform.scale(Picture,
                                                         (self.screen_size[0] * 1 / 4,
                                                          z * (self.screen_size[0] * 1 / 4)))
                    else:
                        Picture = self.Lato.render(self.new_File.split("\\")[-1][-1:-32:-1][::-1], True,
                                                   (255, 255, 255))
                    rect = pygame.Rect(self.screen_size[0] * 5 / 16 + 10, 0, self.screen_size[0] * 5 / 8 - 40,
                                       Picture.get_rect().height + 10)
                    rect.bottomleft = (self.screen_size[0] * 3 / 12 + 20, self.screen_size[1] - 20)
                    send_button = pygame.transform.scale(self.send_button,
                                                         (self.screen_size[1] * 1 / 16 - 20,
                                                          self.screen_size[1] * 1 / 16 - 20))
                    send_buttonR = send_button.get_rect()
                    send_buttonR.bottomleft = (rect.bottomleft[0] + 5, rect.bottomleft[1] - 5)
                    trash_button = pygame.transform.scale(self.Trash, (self.screen_size[1] * 1 / 16 - 20,
                                                                       self.screen_size[1] * 1 / 16 - 20))
                    trash_buttonR = trash_button.get_rect()
                    trash_buttonR.bottomright = (rect.bottomright[0] - 5, rect.bottomright[1] - 5)
                    PictureR = Picture.get_rect()
                    PictureR.center = rect.center
                    Alert[11] = rect
                    Alert[8] = Picture
                    Alert[9] = PictureR
                    Alert[2] = send_button
                    Alert[3] = send_buttonR
                    Alert[5] = trash_button
                    Alert[6] = trash_buttonR
                    Alert[12] = self.new_File

            elif Alert != [] and Alert[0] == "Send File" and not Alert[10]:
                pygame.draw.rect(self.screen, (64, 68, 75), Alert[11], 0, 4)
                self.screen.blit(Alert[8], Alert[9])
                self.screen.blit(Alert[2], Alert[3])
                self.screen.blit(Alert[5], Alert[6])

                if Alert != [] and Alert[3].collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    Alert[4][0] = True
                if Alert != [] and Alert[3].collidepoint(pygame.mouse.get_pos()) and not pygame.mouse.get_pressed()[
                    0] and Alert[4][0]:
                    Alert[4][0] = False
                    Alert[4][1] = True
                    self.Client.send_massage_file(Alert[1], Alert[12])
                    Alert = []
                if Alert != [] and pygame.mouse.get_pressed()[0] and Alert[4][0]:
                    pass
                elif Alert != [] and not pygame.mouse.get_pressed()[0]:
                    Alert[4][0] = False
                if Alert != [] and pygame.mouse.get_pressed()[0] and not Alert[3].collidepoint(pygame.mouse.get_pos()):
                    Alert[4][1] = False

                if Alert != [] and Alert[6].collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    Alert[7][0] = True
                if Alert != [] and Alert[6].collidepoint(pygame.mouse.get_pos()) and not pygame.mouse.get_pressed()[
                    0] and Alert[7][0]:
                    Alert[7][0] = False
                    Alert[7][1] = True
                    Alert = []
                if Alert != [] and pygame.mouse.get_pressed()[0] and Alert[7][0]:
                    pass
                elif Alert != [] and not pygame.mouse.get_pressed()[0]:
                    Alert[7][0] = False
                if Alert != [] and pygame.mouse.get_pressed()[0] and not Alert[6].collidepoint(pygame.mouse.get_pos()):
                    Alert[7][1] = False

            # ["Add Group", tempL, None, None, [False, False], None, None, [False, False], None, None, None, False, None
            #   , None, None, None, None, None, None, None, [False, False]]
            elif Alert[0] != [] and Alert[0] == "Add Group" and Alert[11]:
                Alert[10] = pygame.Rect(self.screen_size[0] * 3 / 12, 0, self.screen_size[0],
                                        self.screen_size[1])
                self.new_File = ""
                Alert[12] = []
                Alert[13] = "Group Chat"
                Alert[2] = self.Lato.render("Create", True, (255, 255, 255))
                Alert[3] = Alert[2].get_rect()
                Alert[3].topleft = (Alert[10].topleft[0] + 20, Alert[10].topleft[1] + 20)
                Alert[5] = self.Lato.render("Cancel", True, (255, 255, 255))
                Alert[6] = Alert[5].get_rect()
                Alert[6].topleft = (Alert[3].bottomleft[0], Alert[3].bottomleft[1] + 20)
                Alert[9] = pygame.Rect(0, 0, 650, 50)
                Alert[9].topright = (Alert[10].topright[0] - 500, Alert[10].topright[1] + 20)
                Alert[8] = TextInputBox(Alert[9].left + 10, Alert[9].top + 5,
                                        font_family=rf"{self.default_image_path}\Fonts\Lato\Lato-Black.ttf",
                                        font_size=30,
                                        max_width=Alert[9].width - 10,
                                        max_height=Alert[9].height,
                                        max_string_length=32)
                Alert[14] = pygame.transform.scale(self.GroupTheme, (300, 300))
                Alert[15] = Alert[14].get_rect()
                Alert[15].topleft = (Alert[6].bottomleft[0], Alert[6].bottomleft[1] + 10)
                Alert[16] = self.Lato.render("Change", True, (255, 255, 255))
                Alert[17] = Alert[16].get_rect()
                Alert[17].topleft = (Alert[15].bottomleft[0], Alert[15].bottomleft[1] + 5)
                Alert[18] = self.Lato.render("Clear", True, (255, 255, 255))
                Alert[19] = Alert[18].get_rect()
                Alert[19].topright = (Alert[15].bottomright[0], Alert[15].bottomright[1] + 5)
                Alert[11] = False
            elif Alert[0] != [] and Alert[0] == "Add Group" and not Alert[11]:
                events2 = events.copy()
                pygame.draw.rect(self.screen, (54, 57, 63), Alert[10])
                pygame.draw.rect(self.screen, (88, 101, 242), Alert[17], 0, 4)
                pygame.draw.rect(self.screen, (216, 60, 62), Alert[19], 0, 4)
                self.screen.blit(Alert[2], Alert[3])
                self.screen.blit(Alert[5], Alert[6])
                self.screen.blit(Alert[14], Alert[15])
                self.screen.blit(Alert[16], Alert[17])
                self.screen.blit(Alert[18], Alert[19])

                for User in Alert[1]:
                    User[0].render(User[1].left, User[1].top, User[1].width, User[1].height)
                flag = True
                if Alert != [] and len(Alert[1]) > 6 and pygame.Rect(self.screen_size[0] * 3 / 12 + 200, 100,
                                                                     self.screen_size[0] * 5.5 / 12,
                                                                     self.screen_size[1]).collidepoint(
                    pygame.mouse.get_pos()):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 4:
                                if Alert[1][0][1].top <= 100:
                                    for User in Alert[1]:
                                        User[1].topleft = (User[1].topleft[0], User[1].topleft[1] + 10)
                            if event.button == 5:
                                if Alert[1][-1][1].bottom >= self.screen_size[1]:
                                    for User in Alert[1]:
                                        User[1].topleft = (User[1].topleft[0], User[1].topleft[1] - 10)
                for event in events2:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            flag = False
                if Alert != [] and Alert[9].collidepoint(pygame.mouse.get_pos()) and flag:
                    Alert[8].update(events2)

                if Alert != [] and pygame.Rect(self.screen_size[0] * 3 / 12 + 200, 100,
                                               self.screen_size[0] * 5.5 / 12,
                                               self.screen_size[1]).collidepoint(pygame.mouse.get_pos()):
                    for friend in Alert[1]:
                        if friend[1].collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                            friend[2][0] = True
                        if friend[1].collidepoint(pygame.mouse.get_pos()) and not pygame.mouse.get_pressed()[
                            0] and friend[2][0]:
                            friend[2][0] = False
                            friend[2][1] = True
                            if not self.IsInList(friend[0], Alert[12]):
                                friend[0].Color = (111, 118, 130)
                                Alert[12].append(friend[0])
                            else:
                                friend[0].Color = (41, 43, 47)
                                Alert[12] = self.RemoveFromList(friend[0], Alert[12])
                        if pygame.mouse.get_pressed()[0] and friend[2][0]:
                            pass
                        elif pygame.mouse.get_pressed()[0]:
                            friend[2][0] = False
                        if pygame.mouse.get_pressed()[0] and not friend[1].collidepoint(pygame.mouse.get_pos()) and not \
                                friend[2][0]:
                            Add_Group[3][1] = False
                if Alert != [] and Alert[17].collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    self.window = Tk()
                    button = Button(text="Open File", command=self.openFile)
                    button.pack()
                    self.window.mainloop()
                    if self.new_File != "":
                        Alert[14] = pygame.transform.scale(pygame.image.load(self.new_File), (300, 300))
                if Alert != [] and Alert[19].collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    Alert[14] = pygame.transform.scale(self.GroupTheme, (300, 300))
                    self.new_File = ""
                pygame.draw.rect(self.screen, (88, 101, 242), Alert[3], 0, 4)
                if Alert != [] and Alert[3].collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    Alert[4][0] = True
                    pygame.draw.rect(self.screen, (60, 69, 165), Alert[3], 0, 4)
                if Alert != [] and len(Alert[12]) > 0 and Alert[3].collidepoint(pygame.mouse.get_pos()) and not \
                        pygame.mouse.get_pressed()[
                            0] and Alert[4][0]:
                    Alert[4][0] = False
                    Alert[4][1] = True
                    pygame.draw.rect(self.screen, (60, 69, 165), Alert[3], 0, 4)
                    if Alert[8].get_text() != "":
                        Alert[13] = Alert[8].get_text()
                    self.AddGroup(Alert[13], Alert[12])
                    for x in Friends_List:
                        x[0].Color = (41, 43, 47)
                    Alert = []
                if Alert != [] and pygame.mouse.get_pressed()[0] and Alert[4][0]:
                    pygame.draw.rect(self.screen, (60, 69, 165), Alert[3], 0, 4)
                elif Alert != [] and pygame.mouse.get_pressed()[0]:
                    Alert[4][0] = False
                if Alert != [] and pygame.mouse.get_pressed()[0] and not Alert[3].collidepoint(
                        pygame.mouse.get_pos()) and not \
                        Alert[4][0]:
                    Alert[4][1] = False
                if Alert != [] and not pygame.mouse.get_pressed()[0]:
                    Alert[4][0] = False
                    Alert[4][1] = False
                if Alert != []:
                    pygame.draw.rect(self.screen, (216, 60, 62), Alert[6], 0, 4)
                if Alert != [] and Alert[6].collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    Alert[7][0] = True
                    pygame.draw.rect(self.screen, (138, 38, 40), Alert[6], 0, 4)
                if Alert != [] and Alert[6].collidepoint(pygame.mouse.get_pos()) and not pygame.mouse.get_pressed()[
                    0] and Alert[7][0]:
                    Alert[7][0] = False
                    Alert[7][1] = True
                    pygame.draw.rect(self.screen, (138, 38, 40), Alert[6], 0, 4)
                    for x in Friends_List:
                        x[0].Color = (41, 43, 47)
                    Alert = []
                if Alert != [] and pygame.mouse.get_pressed()[0] and Alert[7][0]:
                    pygame.draw.rect(self.screen, (138, 38, 40), Alert[6], 0, 4)
                elif Alert != [] and pygame.mouse.get_pressed()[0]:
                    Alert[7][0] = False
                if Alert != [] and pygame.mouse.get_pressed()[0] and not Alert[6].collidepoint(
                        pygame.mouse.get_pos()) and not \
                        Alert[7][0]:
                    Alert[7][1] = False
                if Alert != []:
                    pygame.draw.rect(self.screen, (32, 34, 37), Alert[9], 0, 4)
                    if Alert != [] and Alert[9].collidepoint(pygame.mouse.get_pos()):
                        pygame.draw.rect(self.screen, (6, 6, 7), Alert[9], 1, 4)
                    self.screen.blit(Alert[2], Alert[3])
                    self.screen.blit(Alert[5], Alert[6])
                    self.screen.blit(Alert[14], Alert[15])
                    self.screen.blit(Alert[16], Alert[17])
                    self.screen.blit(Alert[18], Alert[19])
                    Alert[8].render(self.screen)
                # ["Delete Group", self.ID, self.Rect, None, None, [False, False], None, None, [False, False], True]
            elif Alert[0] != [] and Alert[0] == "Delete Group" and Alert[9]:
                if Alert[10] != self.UserID:
                    Alert = []
                else:
                    Alert[3] = self.Lato.render("Delete", True, (255, 255, 255))
                    Alert[4] = Alert[3].get_rect()
                    Alert[4].topleft = (Alert[2].topleft[0] + 2, Alert[2].topleft[1] + 2)
                    Alert[6] = pygame.transform.scale(self.Trash, (self.screen_size[1] * 1 / 16 - 20,
                                                                   self.screen_size[1] * 1 / 16 - 20))
                    Alert[7] = Alert[6].get_rect()
                    Alert[7].topright = (Alert[2].topright[0] - 5, Alert[2].topright[1] + 10)
                    Alert[9] = False
            elif Alert[0] != [] and Alert[0] == "Delete Group" and not Alert[9]:
                pygame.draw.rect(self.screen, (66, 70, 77), Alert[2], 0, 4)
                self.screen.blit(Alert[6], Alert[7])
                if Alert != []:
                    pygame.draw.rect(self.screen, (216, 60, 62), Alert[4], 0, 4)
                if Alert != [] and Alert[4].collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    Alert[5][0] = True
                    pygame.draw.rect(self.screen, (149, 42, 43), Alert[4], 0, 4)
                if Alert != [] and Alert[4].collidepoint(pygame.mouse.get_pos()) and not pygame.mouse.get_pressed()[
                    0] and Alert[5][0]:
                    Alert[5][0] = False
                    Alert[5][1] = True
                    pygame.draw.rect(self.screen, (149, 42, 43), Alert[4], 0, 4)
                    self.DeleteGroup(Alert[1])
                    Alert = []
                if Alert != [] and pygame.mouse.get_pressed()[0] and Alert[5][0]:
                    pygame.draw.rect(self.screen, (149, 42, 43), Alert[4], 0, 4)
                elif Alert != [] and pygame.mouse.get_pressed()[0]:
                    Alert[5][0] = False
                if Alert != [] and pygame.mouse.get_pressed()[0] and not Alert[4].collidepoint(
                        pygame.mouse.get_pos()) and not \
                        Alert[5][0]:
                    Alert[5][1] = False

                if Alert != [] and Alert[7].collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    Alert[8][0] = True
                if Alert != [] and Alert[7].collidepoint(pygame.mouse.get_pos()) and not pygame.mouse.get_pressed()[
                    0] and Alert[8][0]:
                    Alert[8][0] = False
                    Alert[8][1] = True
                    Alert = []
                if Alert != [] and pygame.mouse.get_pressed()[0] and Alert[8][0]:
                    pass
                elif Alert != [] and pygame.mouse.get_pressed()[0]:
                    Alert[8][0] = False
                if Alert != [] and pygame.mouse.get_pressed()[0] and not Alert[7].collidepoint(
                        pygame.mouse.get_pos()) and not \
                        Alert[8][0]:
                    Alert[8][1] = False
                if Alert != []:
                    self.screen.blit(Alert[3], Alert[4])
            # Alert = ["Add Group Member", [], None, None, None, [False, False], None, None, [False, False], True]

            elif Alert[0] != [] and Alert[0] == "Add Group Member" and Alert[9]:
                Alert[2] = pygame.Rect(self.screen_size[0] * 3 / 12, 50, self.screen_size[0] * 5 / 8,
                                       self.screen_size[1])
                Height = self.screen_size[1] * 2 / 16
                Top = 100
                tempL = []
                for x in Friends_List:
                    if not self.IsInMemberList(Alert[11], x[0]):
                        tempL.append(
                            [x[0], pygame.Rect(self.screen_size[0] * 3 / 12, Top + 10, self.screen_size[0] * 5.5 / 12,
                                               self.screen_size[1] * 2 / 16), [False, False]])
                    Top += Height + 3
                Alert[1] = tempL
                Alert[3] = self.Lato.render("Add", True, (255, 255, 255))
                Alert[4] = Alert[3].get_rect()
                Alert[4].topleft = (Alert[2].topleft[0] + 5, Alert[2].topleft[1] + 5)
                Alert[6] = self.Lato.render("Cancel", True, (255, 255, 255))
                Alert[7] = Alert[6].get_rect()
                Alert[7].topleft = (Alert[4].topright[0] + 20, Alert[4].topright[1])
                Alert[9] = False





            elif Alert[0] != [] and Alert[0] == "Add Group Member" and not Alert[9]:
                if Alert != []:
                    pygame.draw.rect(self.screen, (54, 57, 63), Alert[2])
                    pygame.draw.rect(self.screen, (88, 101, 242), Alert[4], 0, 4)
                    pygame.draw.rect(self.screen, (216, 60, 62), Alert[7], 0, 4)

                if Alert != [] and len(Alert[1]) > 1 and pygame.Rect(self.screen_size[0] * 3 / 12, 100,
                                                                     self.screen_size[0] * 5.5 / 12,
                                                                     self.screen_size[1]).collidepoint(
                    pygame.mouse.get_pos()):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 4:
                                if Alert[1][0][1].top <= 100:
                                    for User in Alert[1]:
                                        User[1].topleft = (User[1].topleft[0], User[1].topleft[1] + 10)
                            if event.button == 5:
                                if Alert[1][-1][1].bottom >= self.screen_size[1]:
                                    for User in Alert[1]:
                                        User[1].topleft = (User[1].topleft[0], User[1].topleft[1] - 10)
                if Alert != []:
                    for friend in Alert[1]:
                        if friend[1].collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                            friend[2][0] = True
                        if friend[1].collidepoint(pygame.mouse.get_pos()) and not pygame.mouse.get_pressed()[
                            0] and friend[2][0]:
                            friend[2][0] = False
                            friend[2][1] = True
                            if not self.IsInList(friend[0], Alert[10]):
                                friend[0].Color = (111, 118, 130)
                                Alert[10].append(friend[0])
                            else:
                                friend[0].Color = (41, 43, 47)
                                Alert[10] = self.RemoveFromList(friend[0], Alert[10])
                        if pygame.mouse.get_pressed()[0] and friend[2][0]:
                            pass
                        elif pygame.mouse.get_pressed()[0]:
                            friend[2][0] = False
                        if pygame.mouse.get_pressed()[0] and not friend[1].collidepoint(pygame.mouse.get_pos()) and not \
                                friend[2][0]:
                            friend[2][1] = False

                if Alert != [] and Alert[4].collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    Alert[5][0] = True
                    pygame.draw.rect(self.screen, (60, 69, 165), Alert[4], 0, 4)

                if Alert != [] and len(Alert[10]) > 0 and Alert[4].collidepoint(pygame.mouse.get_pos()) and not \
                        pygame.mouse.get_pressed()[
                            0] and Alert[5][0]:
                    Alert[5][0] = False
                    Alert[5][1] = True
                    pygame.draw.rect(self.screen, (60, 69, 165), Alert[4], 0, 4)
                    for x in Friends_List:
                        x[0].Color = (41, 43, 47)
                    self.Client.send_add_group_member(Alert[-1], Alert[10])
                    Alert = []

                if Alert != [] and pygame.mouse.get_pressed()[0] and Alert[5][0]:
                    pygame.draw.rect(self.screen, (60, 69, 165), Alert[4], 0, 4)
                elif Alert != [] and pygame.mouse.get_pressed()[0]:
                    Alert[5][0] = False
                if Alert != [] and pygame.mouse.get_pressed()[0] and not Alert[4].collidepoint(
                        pygame.mouse.get_pos()) and not \
                        Alert[5][0]:
                    Alert[5][1] = False

                if Alert != [] and Alert[7].collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    Alert[8][0] = True
                    pygame.draw.rect(self.screen, (151, 42, 44), Alert[7], 0, 4)

                if Alert != [] and Alert[7].collidepoint(pygame.mouse.get_pos()) and not pygame.mouse.get_pressed()[
                    0] and Alert[8][0]:
                    Alert[8][0] = False
                    Alert[8][1] = True
                    pygame.draw.rect(self.screen, (151, 42, 44), Alert[7], 0, 4)
                    for x in Friends_List:
                        x[0].Color = (41, 43, 47)
                    Alert = []
                if Alert != [] and pygame.mouse.get_pressed()[0] and Alert[8][0]:
                    pygame.draw.rect(self.screen, (151, 42, 44), Alert[7], 0, 4)
                elif Alert != [] and pygame.mouse.get_pressed()[0]:
                    Alert[8][0] = False
                if Alert != [] and pygame.mouse.get_pressed()[0] and not Alert[7].collidepoint(
                        pygame.mouse.get_pos()) and not \
                        Alert[8][0]:
                    Alert[8][1] = False

                if Alert != []:
                    for User in Alert[1]:
                        User[0].render(User[1].left, User[1].top, User[1].width, User[1].height)
                if Alert != []:
                    self.screen.blit(Alert[3], Alert[4])
                    self.screen.blit(Alert[6], Alert[7])

            # Alert = ["Remove Group Member", self.ID, self.UserID, Member, None, None, [False, False], None, None, [False, False], True]
            elif Alert != [] and Alert[0] == "Remove Group Member" and Alert[10]:
                Alert[4] = self.Lato2.render("Delete", True, (255, 255, 255))
                Alert[5] = Alert[4].get_rect()
                Alert[5].midleft = (Alert[3].Rect.midleft[0] + 2, Alert[3].Rect.midleft[1])
                Alert[7] = pygame.transform.scale(self.Trash, (self.screen_size[1] * 1 / 16 - 20,
                                                               self.screen_size[1] * 1 / 16 - 20))
                Alert[8] = Alert[7].get_rect()
                Alert[8].midright = (Alert[3].Rect.midright[0] - 5, Alert[3].Rect.midright[1])
                Alert[10] = False

            elif Alert != [] and Alert[0] == "Remove Group Member" and not Alert[10]:
                pygame.draw.rect(self.screen, (66, 70, 77), Alert[3].Rect, 0, 4)
                self.screen.blit(Alert[7], Alert[8])
                if Alert != []:
                    pygame.draw.rect(self.screen, (216, 60, 62), Alert[5], 0, 4)
                if Alert != [] and Alert[5].collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    Alert[6][0] = True
                    pygame.draw.rect(self.screen, (149, 42, 43), Alert[5], 0, 4)
                if Alert != [] and Alert[5].collidepoint(pygame.mouse.get_pos()) and not pygame.mouse.get_pressed()[
                    0] and Alert[6][0]:
                    Alert[6][0] = False
                    Alert[6][1] = True
                    pygame.draw.rect(self.screen, (149, 42, 43), Alert[5], 0, 4)
                    self.Client.send_delete_group_member(Alert[1], Alert[3].ID)
                    Alert = []
                if Alert != [] and pygame.mouse.get_pressed()[0] and Alert[6][0]:
                    pygame.draw.rect(self.screen, (149, 42, 43), Alert[5], 0, 4)
                elif Alert != [] and pygame.mouse.get_pressed()[0]:
                    Alert[6][0] = False
                if Alert != [] and pygame.mouse.get_pressed()[0] and not Alert[5].collidepoint(
                        pygame.mouse.get_pos()) and not \
                        Alert[6][0]:
                    Alert[6][1] = False

                if Alert != [] and Alert[8].collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    Alert[9][0] = True
                if Alert != [] and Alert[8].collidepoint(pygame.mouse.get_pos()) and not pygame.mouse.get_pressed()[
                    0] and Alert[9][0]:
                    Alert[9][0] = False
                    Alert[9][1] = True
                    Alert = []
                if Alert != [] and pygame.mouse.get_pressed()[0] and Alert[9][0]:
                    pass
                elif Alert != [] and pygame.mouse.get_pressed()[0]:
                    Alert[9][0] = False
                if Alert != [] and pygame.mouse.get_pressed()[0] and not Alert[8].collidepoint(
                        pygame.mouse.get_pos()) and not \
                        Alert[9][0]:
                    Alert[9][1] = False
                if Alert != []:
                    self.screen.blit(Alert[4], Alert[5])

            elif Alert != [] and Alert[0] == "Leave Group":
                self.Client.send_leave_group(Alert[1])

                tempL = []
                Left = 2 + self.screen_size[0] * 1 / 25
                Top = 80
                for group in Groups_List:
                    if group.ID != Alert[1]:
                        temp = group
                        temp.Rect = pygame.Rect(Left, Top, self.screen_size[0] * 31 / 150,
                                                self.screen_size[1] * 1 / 16)
                        Top += self.screen_size[1] * 1 / 16 + 2
                        tempL.append(temp)
                Groups_List = tempL
                Alert = []

    def IsInMemberList(self, MemberList, User):
        for x in MemberList:
            if User.ID == x.ID:
                return True
        return False

    """
    send server delete group by groupID
    """

    def DeleteGroup(self, groupID):
        self.Client.send_delete_group(groupID)

    """
    send server massage of making new group
    """

    def AddGroup(self, GroupName, MembersList, owner=None):
        if self.new_File == "":
            if owner != None:
                self.Client.send_insert_group(GroupName, rf"{self.default_image_path}\Default\017-friends.png",
                                              open(rf"{self.default_image_path}\Default\017-friends.png", "rb").read(),
                                              owner, MembersList)
            else:
                self.Client.send_insert_group(GroupName, rf"{self.default_image_path}\Default\017-friends.png",
                                              open(rf"{self.default_image_path}\Default\017-friends.png", "rb").read(),
                                              self.UserID, MembersList)
        else:
            if owner != None:
                self.Client.send_insert_group(GroupName, self.new_File,
                                              open(self.new_File, "rb").read(),
                                              owner, MembersList)
            else:
                self.Client.send_insert_group(GroupName, self.new_File,
                                              open(self.new_File, "rb").read(),
                                              self.UserID, MembersList)
        self.new_File = ""

    def IsInList(self, User, List):
        for x in List:
            if User.ID == x.ID:
                return True
        return False

    def RemoveFromList(self, User, List):
        templ = []
        for x in List:
            if User.ID != x.ID:
                templ.append(x)
        return templ

    def OpenAnyFile(self):
        self.new_File = filedialog.askopenfilename(initialdir="C:\\Users\\Bar\\",
                                                   title="Open file okay?",
                                                   filetypes=(("all files", "*.*"),))
        self.window.destroy()

    """
    load and prieper the groups for rendering
    """

    def GroupsLoad(self, Left, Top):
        for group in Groups_List:
            group.Rect = pygame.Rect(Left, Top, self.screen_size[0] * 31 / 150, self.screen_size[1] * 1 / 16)
            Top += self.screen_size[1] * 1 / 16 + 2

    """
    feeding groups with event feed
    """

    def GroupsEvents(self, events):
        global Groups_List
        Alert2 = []
        temp = []
        for group in Groups_List:
            temp = group.update(events, self.Client)
            if temp != []:
                Alert2 = temp
            if group.GroupEvnets[1]:
                for group2 in Groups_List:
                    if group != group2:
                        group2.GroupEvnets[1] = False
                self.Friends_event[1] = False

        if len(Groups_List) > 3 and pygame.Rect(2 + self.screen_size[0] * 1 / 25, 80,
                                                self.screen_size[0] * 21 / 100,
                                                (self.screen_size[1] * 15 / 16) - 80).collidepoint(
            pygame.mouse.get_pos()):
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        if Groups_List[0].Rect.top <= 80:
                            for Group in Groups_List:
                                Group.Rect.topleft = (Group.Rect.topleft[0], Group.Rect.topleft[1] + 10)
                    if event.button == 5:
                        if Groups_List[-1].Rect.bottom >= self.screen_size[1] * 15 / 16 + 4:
                            for Group in Groups_List:
                                Group.Rect.topleft = (Group.Rect.topleft[0], Group.Rect.topleft[1] - 10)
        return Alert2

    """
    render the groups on screen
    """

    def GroupsRender(self, Left, Top, visible=True):
        global Groups_List
        if visible:
            pygame.draw.rect(self.screen, (47, 49, 54),
                             pygame.Rect(Left, Top, self.screen_size[0] * 21 / 100, self.screen_size[1] * 15 / 16))
            for group in Groups_List:
                group.render(group.Rect.left, group.Rect.top, group.Rect.width, group.Rect.height)

    def Add_Friend(self, ID, UserName, UserPicture, Picture):
        global Friends_List
        Friends_List.append(
            User(ID, UserName, UserPicture, Picture, self.default_image_path, self.screen_size, self.Lato, self.screen))

    def Add_Group(self, ID, GroupName, GroupPicture, Picture, OwnerID, MemberList, MassageList):
        global Groups_List
        TMemberList = []
        for Member in MemberList:
            TMemberList.append(
                User(Member[0], Member[1], None, None, self.default_image_path, self.screen_size, self.Lato3,
                     self.screen, Icon=self.Default_avatar if Member[0] != OwnerID else self.OwnerIcon))
        TMassageList = []
        for massage in MassageList:
            TMassageList.append(
                Massage(self.GetUserName(massage[0], TMemberList), massage[1], massage[2], massage[3],
                        self.default_image_path, self.screen_size,
                        self.Lato2, self.screen, self.Lato3, self.File_Icon))
        Groups_List.append(
            Group(ID, GroupName, GroupPicture, Picture, OwnerID, TMemberList, TMassageList, self.default_image_path,
                  self.screen_size, self.Lato3, self.screen, self.send_button, self.Upload, self.UserID))

    def GetUserName(self, ID, list):
        for Name in list:
            if Name.ID == ID:
                return Name.UserName

    def Add_Community(self, ID, CommunityName, CommunityPicture, Picture, OwnerID, MemberList, CommunityGroups):
        global Communities_List
        TMemberList = []
        for Member in MemberList:
            TMemberList.append(
                User(Member[0], Member[1], None, None, self.default_image_path, self.screen_size, self.Lato,
                     self.screen))
        TCommunityGroups = []
        for group in CommunityGroups:
            TMassageList = []
            for Massage in group[1]:
                TMassageList.append(
                    Massage(Massage[0], Massage[1], Massage[2], Massage[3], self.default_image_path, self.screen_size,
                            self.Lato, self.screen, self.Lato2, self.File_Icon))
            TCommunityGroups.append(
                Group(group[0][0], group[0][1], None, None, None, TMemberList, TMassageList, self.default_image_path,
                      self.screen_size, self.Lato, self.screen, self.send_button, self.Upload, self.UserID))
        Communities_List.append(
            Community(ID, CommunityName, CommunityPicture, Picture, OwnerID, TMemberList, TCommunityGroups,
                      self.default_image_path, self.screen_size, self.Lato, self.screen))

    def Add_PublicCommunity(self, ID, CommunityName):
        global PublicCommunities_List
        PublicCommunities_List.append(
            PublicCommunity(ID, CommunityName, self.default_image_path, self.screen_size, self.Lato, self.screen))

    """
    Load the friends and priepering them for rendering
    """

    def FriendsLoad(self, Left, Top, Width, Height):
        global Friends_List
        self.Friends_buttonR = self.Friends_button.get_rect()
        self.Friends_buttonR.center = (self.screen_size[1] * 1 / 25, self.screen_size[1] * 1 / 25)
        self.Friends_event = [False, True, False]
        self.Friend_Request_Bar_R = pygame.Rect(Left + 10, Top, 800, 50)
        self.Friend_Request_Bar_R_events = [False, False, False]
        self.Request_Bar = TextInputBox(self.Friend_Request_Bar_R.left + 10, self.Friend_Request_Bar_R.top + 5,
                                        font_family=rf"{self.default_image_path}\Fonts\Lato\Lato-Black.ttf",
                                        font_size=30,
                                        max_width=self.Friend_Request_Bar_R.width - 100,
                                        max_height=self.Friend_Request_Bar_R.height,
                                        max_string_length=32)
        self.Request_Button = pygame.Rect(0, 0, 200, 40)
        self.Request_Button.topright = (
            self.Friend_Request_Bar_R.topright[0] - 10, self.Friend_Request_Bar_R.topright[1] + 5)
        self.RequestMass = self.Lato_Clean.render("Send Friend Request", True, (255, 255, 255))
        self.Request_Button_R = self.RequestMass.get_rect()
        self.Request_Button_R.center = self.Request_Button.center
        tempL = []
        Top += 80
        for x in Friends_List:
            tempL.append([x, pygame.Rect(Left + 30, Top + 10, Width, Height)])
            Top += Height + 3
        Friends_List = tempL

    """
    feeding the friends with event feed
    """

    def FriendsEvent(self, events):
        e = events.copy()
        global Friends_List, Alert
        ENTER = False
        if self.Friends_buttonR.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and not \
                self.Friends_event[2]:
            pygame.draw.rect(self.screen, (96, 100, 244), self.Friends_buttonR, 0, 10)
            self.Friends_event[0] = True
        if self.Friends_event[0]:
            pygame.draw.rect(self.screen, (96, 100, 244), self.Friends_buttonR, 0, 10)
        if self.Friends_buttonR.collidepoint(pygame.mouse.get_pos()) and not pygame.mouse.get_pressed()[0] and \
                self.Friends_event[0]:
            pygame.draw.rect(self.screen, (96, 100, 244), self.Friends_buttonR, 0, 10)
            self.Friends_event[0] = False
            self.Friends_event[1] = True
            for group in Groups_List:
                group.GroupEvnets[1] = False
        elif not pygame.mouse.get_pressed()[0]:
            self.Friends_event[0] = False
        if pygame.mouse.get_pressed()[0]:
            self.Friends_event[2] = True
        else:
            self.Friends_event[2] = False
        if self.Friends_event[1]:
            if len(Friends_List) > 6 and pygame.Rect(self.screen_size[0] * 3 / 12 + 10, 0,
                                                     self.screen_size[0] * 5.5 / 12,
                                                     self.screen_size[1]).collidepoint(pygame.mouse.get_pos()):
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:

                        if event.button == 4:
                            if Friends_List[0][1].top <= 0:
                                for User in Friends_List:
                                    User[1].topleft = (User[1].topleft[0], User[1].topleft[1] + 10)
                        if event.button == 5:
                            if Friends_List[-1][1].bottom >= self.screen_size[1]:
                                for User in Friends_List:
                                    User[1].topleft = (User[1].topleft[0], User[1].topleft[1] - 10)
            e2 = e.copy()
            for event in e2:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        ENTER = True
            if self.Friend_Request_Bar_R.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and not \
                    self.Friend_Request_Bar_R_events[2]:
                self.Friend_Request_Bar_R_events[0] = True
            if self.Friend_Request_Bar_R.collidepoint(pygame.mouse.get_pos()) and not pygame.mouse.get_pressed()[0] and \
                    self.Friend_Request_Bar_R_events[0]:
                self.Friend_Request_Bar_R_events[0] = False
                self.Friend_Request_Bar_R_events[1] = True
            elif not pygame.mouse.get_pressed()[0]:
                self.Friend_Request_Bar_R_events[0] = False
            if pygame.mouse.get_pressed()[0]:
                self.Friend_Request_Bar_R_events[2] = True
            else:
                self.Friend_Request_Bar_R_events[2] = False
            if pygame.mouse.get_pressed()[0] and not self.Friend_Request_Bar_R.collidepoint(pygame.mouse.get_pos()):
                self.Friend_Request_Bar_R_events[1] = False

            if self.Friend_Request_Bar_R_events[1] and not ENTER:
                self.Request_Bar.update(e)
            if (ENTER and self.Request_Bar.get_text() != "") or (
                    self.Request_Button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] \
                    and self.Request_Bar.get_text() != ""):
                self.Client.send_friend_request(self.Request_Bar.get_text())
                self.Request_Bar.clear_text()
            if pygame.Rect(self.screen_size[0] * 3 / 12 + 10, 0, self.screen_size[0] * 5.5 / 12,
                           self.screen_size[1]).collidepoint(pygame.mouse.get_pos()):
                for friend in Friends_List:
                    if not pygame.mouse.get_pressed()[0] and not friend[1].collidepoint(pygame.mouse.get_pos()):
                        friend[0].TouchEvent[0] = False
                    if friend[1].collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                        friend[0].TouchEvent[0] = True
                    if friend[1].collidepoint(pygame.mouse.get_pos()) and not pygame.mouse.get_pressed()[
                        0] and friend[0].TouchEvent[0]:
                        friend[0].TouchEvent[0] = False
                        friend[0].TouchEvent[1] = True
                        # ["Friend", friend[0], None, None, [False, False], None, None, [False, False], True, Rect]
                        # Alert = ["Friend", friend[0], None, None, [False, False], True]
                        Alert = ["Friend", friend[0], None, None, [False, False], None, None, [False, False], True,
                                 friend[1]]
                    if pygame.mouse.get_pressed()[0] and friend[0].TouchEvent[0]:
                        pass
                    elif Alert != [] and pygame.mouse.get_pressed()[0]:
                        friend[0].TouchEvent[0] = False
                    if pygame.mouse.get_pressed()[0] and not friend[1].collidepoint(
                            pygame.mouse.get_pos()) and not \
                            friend[0].TouchEvent[0]:
                        friend[0].TouchEvent[1] = False

    """
    rendering the friends in screen
    """

    def FriendsRender(self, Left, Top):
        global Friends_List
        if not self.Friends_event[1]:
            self.screen.blit(self.Friends_button, self.Friends_buttonR)
        else:
            pygame.draw.rect(self.screen, (54, 57, 63),
                             pygame.Rect(Left, Top, self.screen_size[0], self.screen_size[1]))
            pygame.draw.rect(self.screen, (96, 100, 244), self.Friends_buttonR, 0, 10)
            self.screen.blit(self.Friends_button, self.Friends_buttonR)
            for User in Friends_List:
                if Alert == []:
                    User[0].Color = (41, 43, 47)
                User[0].render(User[1].left, User[1].top, User[1].width, User[1].height)
            pygame.draw.rect(self.screen, (32, 34, 37), self.Friend_Request_Bar_R, 0, 4)
            pygame.draw.rect(self.screen, (88, 101, 242), self.Request_Button, 0, 4)
            self.screen.blit(self.RequestMass, self.Request_Button_R)
            if self.Friend_Request_Bar_R_events[1]:
                pygame.draw.rect(self.screen, (57, 136, 255), self.Friend_Request_Bar_R, 1, 4)
            else:
                pygame.draw.rect(self.screen, (6, 6, 7), self.Friend_Request_Bar_R, 1, 4)
            self.Request_Bar.render(self.screen)


    """
    remove friend from interface and send to server
    """
    def RemoveFriend(self, User):
        global Friends_List
        tempL = []
        Top = 100
        for x in Friends_List:
            if x[0].ID != User.ID:
                tempL.append(
                    [x[0], pygame.Rect(self.screen_size[0] * 3 / 12 + 33, Top + 10, self.screen_size[0] * 5.5 / 12,
                                       self.screen_size[1] * 2 / 16)])
                Top += self.screen_size[1] * 2 / 16 + 3
        Friends_List = tempL
        self.Client.send_remove_friend(User.ID)

    def FriendRequestsUpdate(self, events, user):
        global Friend_Request_List, condition
        if self.Friends_event[1]:
            if len(Friend_Request_List) > 1 and pygame.Rect(self.screen_size[0] * 17 / 24 + 120, 0,
                                                            self.screen_size[0] - (self.screen_size[0] * 17 / 24),
                                                            self.screen_size[1]).collidepoint(pygame.mouse.get_pos()):
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:

                        if event.button == 4:
                            if Friend_Request_List[0][0].top <= 0:
                                for request in Friend_Request_List:
                                    request[0].topleft = (request[0].topleft[0], request[0].topleft[1] + 10)
                                    request[3].topleft = (request[3].topleft[0], request[3].topleft[1] + 10)
                                    request[5].topleft = (request[5].topleft[0], request[5].topleft[1] + 10)
                                    request[7].topleft = (request[7].topleft[0], request[7].topleft[1] + 10)

                        if event.button == 5:
                            if Friend_Request_List[-1][0].bottom >= self.screen_size[1]:
                                for request in Friend_Request_List:
                                    request[0].topleft = (request[0].topleft[0], request[0].topleft[1] - 10)
                                    request[3].topleft = (request[3].topleft[0], request[3].topleft[1] - 10)
                                    request[5].topleft = (request[5].topleft[0], request[5].topleft[1] - 10)
                                    request[7].topleft = (request[7].topleft[0], request[7].topleft[1] - 10)
            for Request in Friend_Request_List:
                if Request[7].collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    Request[9][0] = True
                if Request[7].collidepoint(pygame.mouse.get_pos()) and not pygame.mouse.get_pressed()[
                    0] and \
                        Request[9][0]:
                    Request[9][0] = False
                    Request[9][1] = True
                    condition.acquire()
                    self.RemoveRequest(Request, False)
                    condition.notify()
                    condition.release()
                    break
                elif not pygame.mouse.get_pressed()[0]:
                    Request[9][0] = False
                if pygame.mouse.get_pressed()[0] and not Request[7].collidepoint(pygame.mouse.get_pos()):
                    Request[9][1] = False

                if Request[5].collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    Request[10][0] = True
                if Request[5].collidepoint(pygame.mouse.get_pos()) and not pygame.mouse.get_pressed()[
                    0] and \
                        Request[10][0]:
                    Request[10][0] = False
                    Request[10][1] = True
                    condition.acquire()
                    self.RemoveRequest(Request, True, user=user)
                    condition.notify()
                    condition.release()
                    break
                elif not pygame.mouse.get_pressed()[0]:
                    Request[10][0] = False
                if pygame.mouse.get_pressed()[0] and not Request[5].collidepoint(pygame.mouse.get_pos()):
                    Request[10][1] = False

    def RemoveRequest(self, Request, accept, user=None):
        global Friend_Request_List, Friends_List
        tList = []
        for x in Friend_Request_List:
            if x[1] != Request[1]:
                tList.append(x)
        Friend_Request_List = tList
        h = 70
        for x in Friend_Request_List:
            x[0].topleft = (x[0].topleft[0], h)
            x[3].topleft = (x[0].topleft[0] + 5, x[0].topleft[1] + 5)
            x[5].bottomleft = (x[0].bottomleft[0] + 5, x[0].bottomleft[1] - 5)
            x[7].bottomright = (x[0].bottomright[0] - 5, x[0].bottomright[1] - 5)
            h = x[0].bottomleft[1] + 10
        if accept:
            User = Request[8]
            if Friends_List == []:
                Rect = pygame.Rect(self.screen_size[0] * 3 / 12 + 3, 20,
                                   self.screen_size[0] * 5.5 / 12, self.screen_size[1] * 2 / 16)
            else:
                Rect = pygame.Rect(Friends_List[-1][1].left, Friends_List[-1][1].bottom + 3, Friends_List[-1][1].width,
                                   Friends_List[-1][1].height)
            Friends_List.append([User, Rect])
            self.new_File = ""
            self.AddGroup(f"{User.UserName}, {user.UserName}", [User, user], owner=0)
            time.sleep(1)
            self.Client.send_accept_friend_request(Request[1])

    def FriendRequestsRender(self):
        global Friend_Request_List
        if self.Friends_event[1]:
            for Friend in Friend_Request_List:
                pygame.draw.rect(self.screen, (47, 49, 54), Friend[0], 0, 4)
                self.screen.blit(Friend[2], Friend[3])
                pygame.draw.rect(self.screen, (59, 165, 93), Friend[5], 0, 4)
                self.screen.blit(Friend[4], Friend[5])
                pygame.draw.rect(self.screen, (216, 60, 62), Friend[7], 0, 4)
                self.screen.blit(Friend[6], Friend[7])

    def Close_event(self, events):
        try:
            for event in events:
                if event.type == pygame.QUIT:
                    self.Close_Connection()
                    self.Close()
                    quit()
        except Exception as e:
            print()

    def Close_Connection(self):
        self.Client.Clost_Connection()

"""
this objecgt handle listening to the server massages and user updates and render it into the interface
"""
class Listener(threading.Thread):
    def __init__(self, Client, Key, path, screen_size,
                 Lato2, screen, Lato3, File_Icon, small_Lato, Lato, Default_avatar, OwnerIcon, send_button, Upload,
                 UserID):
        self.UserID = UserID
        self.Upload = Upload
        self.send_button = send_button
        self.OwnerIcon = OwnerIcon
        self.Default_avatar = Default_avatar
        self.path = path
        self.screen_size = screen_size
        self.Lato = Lato
        self.Small_Lato = small_Lato
        self.Lato2 = Lato2
        self.screen = screen
        self.Lato3 = Lato3
        self.File_Icon = File_Icon
        self.Key = Key
        self.Client = Client
        self.RUN = True
        threading.Thread.__init__(self)

    """
    the function is recving massage from the server and handling the information given for changing the ClientInterface
    vars
    """

    def run(self):
        global Friends_List, Groups_List, Communities_List, Friend_Request_List, condition
        try:
            while self.RUN:
                m = self.Client.recv(self.Key)
                if m == "Massage":
                    # UserName, Date, Type, Massage, path, screen_size, font, screen, Mfont, FileIcon)
                    groupID = int(self.Client.recv(self.Key))  # GroupID
                    massage2 = self.Client.recvFile(self.Key)  # Massage
                    ID = int(self.Client.recv(self.Key))  # ID
                    date = self.Client.recvPickle()  # date
                    temp = None
                    for x in Groups_List:
                        if x.ID == groupID:
                            temp = x

                    temp2 = Massage(self.GetUserName(ID, temp.MemberList), date, "Text", massage2, self.path,
                                    self.screen_size,
                                    self.Lato2, self.screen, self.Lato3, self.File_Icon)
                    r = self.screen_size[1] * 15 / 16 - 15
                    h = temp2.render(self.screen_size[0] * 3 / 12 + 20, r, self.screen_size[0] * 5 / 8 - 40,
                                     visible=False)
                    r = r - h - 5
                    temp2.Rect = pygame.Rect(self.screen_size[0] * 3 / 12 + 20, r, self.screen_size[0] * 5 / 8 - 40, h)
                    for x in Groups_List:
                        if x.ID == groupID:
                            for massage in x.MassageList[::-1]:
                                h = massage.render(self.screen_size[0] * 3 / 12 + 20, r,
                                                   self.screen_size[0] * 5 / 8 - 40,
                                                   visible=False)
                                r = r - h - 5
                                massage.Rect = pygame.Rect(self.screen_size[0] * 3 / 12 + 20, r,
                                                           self.screen_size[0] * 5 / 8 - 40, h)
                            x.MassageList.append(temp2)
                if m == "Friend_Request":
                    UserID = int(self.Client.recv(self.Key))
                    UserName = self.Client.recv(self.Key)
                    UserPic = self.Client.recv(self.Key)
                    Pic = self.Client.recvFile(self.Key)
                    User2 = User(UserID, UserName, UserPic, Pic, self.path, self.screen_size, self.Lato, self.screen)
                    if Friend_Request_List == []:
                        Rect = pygame.Rect(self.screen_size[0] * 17 / 24 + 120, 70,
                                           self.screen_size[0] - (self.screen_size[0] * 17 / 24) - 130, 100)
                        UserName = self.Small_Lato.render(UserName, True, (255, 255, 255))
                        UserNameR = UserName.get_rect()
                        UserNameR.topleft = (Rect.topleft[0] + 5, Rect.topleft[1] + 5)
                        Accept = self.Lato.render("Accept", True, (255, 255, 255))
                        AcceptR = Accept.get_rect()
                        AcceptR.bottomleft = (Rect.bottomleft[0] + 5, Rect.bottomleft[1] - 5)
                        Decline = self.Lato.render("Decline", True, (255, 255, 255))
                        DeclineR = Decline.get_rect()
                        DeclineR.bottomright = (Rect.bottomright[0] - 5, Rect.bottomright[1] - 5)
                        condition.acquire()
                        Friend_Request_List.append(
                            [Rect, UserID, UserName, UserNameR, Accept, AcceptR, Decline, DeclineR, User2,
                             [False, False],
                             [False, False]])
                        condition.notify()
                        condition.release()
                    else:
                        Rect = pygame.Rect(0, 0, self.screen_size[0] - (self.screen_size[0] * 17 / 24) - 130, 100)
                        Rect.topleft = (
                            Friend_Request_List[-1][0].bottomleft[0], Friend_Request_List[-1][0].bottomleft[1] + 10)
                        UserName = self.Small_Lato.render(UserName, True, (255, 255, 255))
                        UserNameR = UserName.get_rect()
                        UserNameR.topleft = (Rect.topleft[0] + 5, Rect.topleft[1] + 5)
                        Accept = self.Lato.render("Accept", True, (255, 255, 255))
                        AcceptR = Accept.get_rect()
                        AcceptR.bottomleft = (Rect.bottomleft[0] + 5, Rect.bottomleft[1] - 5)
                        Decline = self.Lato.render("Decline", True, (255, 255, 255))
                        DeclineR = Decline.get_rect()
                        DeclineR.bottomright = (Rect.bottomright[0] - 5, Rect.bottomright[1] - 5)
                        condition.acquire()
                        Friend_Request_List.append(
                            [Rect, UserID, UserName, UserNameR, Accept, AcceptR, Decline, DeclineR, User2,
                             [False, False],
                             [False, False]])
                        condition.notify()
                        condition.release()
                print(m)
                if m == "Accept_Friend_Request":
                    UserID = int(self.Client.recv(self.Key))
                    UserName = self.Client.recv(self.Key)
                    UserPic = self.Client.recv(self.Key)
                    Pic = self.Client.recvFile(self.Key)
                    User2 = User(UserID, UserName, UserPic, Pic, self.path, self.screen_size, self.Lato, self.screen)
                    if Friends_List == []:
                        Friends_List.append([User2, pygame.Rect(self.screen_size[0] * 3 / 12 + 3, 20,
                                                                self.screen_size[0] * 5.5 / 12,
                                                                self.screen_size[1] * 2 / 16)])
                    else:
                        Friends_List.append(
                            [User2, pygame.Rect(Friends_List[-1][1].left, Friends_List[-1][1].bottom + 3,
                                                Friends_List[-1][1].width,
                                                Friends_List[-1][1].height)])
                if m == "Remove_Friend":
                    UserID = int(self.Client.recv(self.Key))
                    tempL = []
                    Top = 100
                    for x in Friends_List:
                        if x[0].ID != UserID:
                            tempL.append(
                                [x[0],
                                 pygame.Rect(self.screen_size[0] * 3 / 12 + 33, Top + 10,
                                             self.screen_size[0] * 5.5 / 12,
                                             self.screen_size[1] * 2 / 16)])
                            Top += self.screen_size[1] * 2 / 16 + 3
                    Friends_List = tempL

                if m == "Massage_File":
                    GroupID = int(self.Client.recv(self.Key))
                    UserID = int(self.Client.recv(self.Key))
                    date = self.Client.recvPickle()
                    FileName = self.Client.recv(self.Key)
                    File = self.Client.recvFile(self.Key)
                    # UserName, Date, Type, Massage, path, screen_size, font, screen, Mfont, FileIcon)
                    temp = None
                    for x in Groups_List:
                        if x.ID == GroupID:
                            temp = x

                    temp2 = Massage(self.GetUserName(UserID, temp.MemberList), date, FileName, File, self.path,
                                    self.screen_size,
                                    self.Lato2, self.screen, self.Lato3, self.File_Icon)

                    r = self.screen_size[1] * 15 / 16 - 15
                    h = temp2.render(self.screen_size[0] * 3 / 12 + 20, r, self.screen_size[0] * 5 / 8 - 40,
                                     visible=False)
                    r = r - h - 5
                    temp2.Rect = pygame.Rect(self.screen_size[0] * 3 / 12 + 20, r, self.screen_size[0] * 5 / 8 - 40, h)
                    for x in Groups_List:
                        if x.ID == GroupID:
                            for massage in x.MassageList[::-1]:
                                h = massage.render(self.screen_size[0] * 3 / 12 + 20, r,
                                                   self.screen_size[0] * 5 / 8 - 40,
                                                   visible=False)
                                r = r - h - 5
                                massage.Rect = pygame.Rect(self.screen_size[0] * 3 / 12 + 20, r,
                                                           self.screen_size[0] * 5 / 8 - 40, h)
                            x.MassageList.append(temp2)

                if m == "Insert_Group":
                    GroupID = int(self.Client.recv(self.Key))
                    GroupName = self.Client.recv(self.Key)
                    GroupPictureName = self.Client.recv(self.Key)
                    GroupPicture = self.Client.recvFile(self.Key)
                    OwnerID = int(self.Client.recv(self.Key))
                    Members = []
                    mess = self.Client.recv(self.Key)
                    while mess != "Stop":
                        MemberID = int(mess)
                        MemberName = self.Client.recv(self.Key)
                        Members.append([MemberID, MemberName])
                        mess = self.Client.recv(self.Key)
                    TMemberList = []
                    for Member in Members:
                        TMemberList.append(
                            User(Member[0], Member[1], None, None, self.path, self.screen_size, self.Lato3,
                                 self.screen, Icon=self.Default_avatar if Member[0] != OwnerID else self.OwnerIcon))

                    TempGroup = Group(GroupID, GroupName, GroupPictureName, GroupPicture, OwnerID, TMemberList, [],
                                      self.path,
                                      self.screen_size, self.Lato3, self.screen, self.send_button, self.Upload,
                                      self.UserID)

                    if Groups_List == []:
                        TempGroup.Rect = pygame.Rect(2 + self.screen_size[0] * 1 / 25, 80,
                                                     self.screen_size[0] * 31 / 150,
                                                     self.screen_size[1] * 1 / 16)
                    else:
                        TempGroup.Rect = pygame.Rect(2 + self.screen_size[0] * 1 / 25,
                                                     Groups_List[-1].Rect.top + self.screen_size[1] * 1 / 16 + 2,
                                                     self.screen_size[0] * 31 / 150, self.screen_size[1] * 1 / 16)
                    Groups_List.append(TempGroup)
                if m == "Delete_Group":
                    GroupID = int(self.Client.recv(self.Key))
                    tempL = []
                    Left = 2 + self.screen_size[0] * 1 / 25
                    Top = 80
                    for group in Groups_List:
                        if group.ID != GroupID:
                            temp = group
                            temp.Rect = pygame.Rect(Left, Top, self.screen_size[0] * 31 / 150,
                                                    self.screen_size[1] * 1 / 16)
                            Top += self.screen_size[1] * 1 / 16 + 2
                            tempL.append(temp)
                    Groups_List = tempL

                if m == "Add_Group_Member":
                    GroupID = int(self.Client.recv(self.Key))
                    Members = []
                    mess = self.Client.recv(self.Key)
                    while mess != "Stop":
                        MemberID = int(mess)
                        MemberName = self.Client.recv(self.Key)
                        Members.append([MemberID, MemberName])
                        mess = self.Client.recv(self.Key)

                    temp = None
                    for x in Groups_List:
                        if x.ID == GroupID:
                            temp = x
                    t = temp.MemberList[-1].Rect.bottom
                    for User2 in Members:
                        user = User(User2[0], User2[1], None, None, self.path, self.screen_size, self.Lato3,
                                    self.screen,
                                    Icon=self.Default_avatar)
                        user.Rect = pygame.Rect(self.screen_size[0] * 10.5 / 12, t, self.screen_size[0] * 1.5 / 12,
                                                self.screen_size[1] * 1 / 20)
                        t += self.screen_size[1] * 1 / 20
                        temp.MemberList.append(user)
                if m == "Add_New_Group_Member":
                    GroupID = int(self.Client.recv(self.Key))
                    OwnerID = int(self.Client.recv(self.Key))
                    GroupName = self.Client.recv(self.Key)
                    GroupPictureName = self.Client.recv(self.Key)
                    GroupPicture = self.Client.recvFile(self.Key)
                    Members = []
                    mess = self.Client.recv(self.Key)
                    while mess != "Stop":
                        MemberID = int(mess)
                        MemberName = self.Client.recv(self.Key)
                        Members.append([MemberID, MemberName])
                        mess = self.Client.recv(self.Key)
                    SenderID = None
                    Date = None
                    MassageName = None
                    MassageFile = None
                    massage = self.Client.recv(self.Key)
                    MassageList = []
                    while massage != "Stop":
                        SenderID = int(massage)
                        Date = self.Client.recvPickle()
                        MassageName = self.Client.recv(self.Key)
                        MassageFile = self.Client.recvFile(self.Key)
                        massage = self.Client.recv(self.Key)
                        MassageList.append([SenderID, Date, MassageName, MassageFile])
                    flag = False
                    for x in Groups_List:
                        if x.ID == GroupID:
                            flag = True
                    if not flag:
                        TMemberList = []
                        for Member in Members:
                            TMemberList.append(
                                User(Member[0], Member[1], None, None, self.path, self.screen_size, self.Lato3,
                                     self.screen, Icon=self.Default_avatar if Member[0] != OwnerID else self.OwnerIcon))

                        TMassageList = []
                        for Mass in MassageList:
                            TMassageList.append(Massage(self.GetUserName(Mass[0], TMemberList), Mass[1], Mass[2],
                                                        Mass[3], self.path, self.screen_size,
                                                        self.Lato2, self.screen, self.Lato3, self.File_Icon))

                        TempGroup = Group(GroupID, GroupName, GroupPictureName, GroupPicture, OwnerID, TMemberList,
                                          TMassageList,
                                          self.path,
                                          self.screen_size, self.Lato3, self.screen, self.send_button, self.Upload,
                                          self.UserID)

                        if Groups_List == []:
                            TempGroup.Rect = pygame.Rect(2 + self.screen_size[0] * 1 / 25, 80,
                                                         self.screen_size[0] * 31 / 150,
                                                         self.screen_size[1] * 1 / 16)
                        else:
                            TempGroup.Rect = pygame.Rect(2 + self.screen_size[0] * 1 / 25,
                                                         Groups_List[-1].Rect.top + self.screen_size[1] * 1 / 16 + 2,
                                                         self.screen_size[0] * 31 / 150, self.screen_size[1] * 1 / 16)
                        Groups_List.append(TempGroup)

                if m == "Send_Delete_Group_Member":
                    GroupID = int(self.Client.recv(self.Key))
                    UserID = int(self.Client.recv(self.Key))
                    if self.UserID == UserID:
                        tempL = []
                        Left = 2 + self.screen_size[0] * 1 / 25
                        Top = 80
                        for group in Groups_List:
                            if group.ID != GroupID:
                                temp = group
                                temp.Rect = pygame.Rect(Left, Top, self.screen_size[0] * 31 / 150,
                                                        self.screen_size[1] * 1 / 16)
                                Top += self.screen_size[1] * 1 / 16 + 2
                                tempL.append(temp)
                        Groups_List = tempL
                    else:
                        for x in Groups_List:
                            if x.ID == GroupID:
                                tempL = []
                                t = self.screen_size[1] * 1 / 12
                                for user in x.MemberList:
                                    if user.ID != UserID:
                                        user.Rect = pygame.Rect(self.screen_size[0] * 10.5 / 12, t,
                                                                self.screen_size[0] * 1.5 / 12,
                                                                self.screen_size[1] * 1 / 20)
                                        t += self.screen_size[1] * 1 / 20
                                        tempL.append(user)
                                x.MemberList = tempL

                if m == "Leave_Group":
                    GroupID = int(self.Client.recv(self.Key))
                    UserID = int(self.Client.recv(self.Key))
                    if self.UserID == UserID:
                        tempL = []
                        Left = 2 + self.screen_size[0] * 1 / 25
                        Top = 80
                        for group in Groups_List:
                            if group.ID != GroupID:
                                temp = group
                                temp.Rect = pygame.Rect(Left, Top, self.screen_size[0] * 31 / 150,
                                                        self.screen_size[1] * 1 / 16)
                                Top += self.screen_size[1] * 1 / 16 + 2
                                tempL.append(temp)
                        Groups_List = tempL
                    else:
                        for x in Groups_List:
                            if x.ID == GroupID:
                                tempL = []
                                t = self.screen_size[1] * 1 / 12
                                for user in x.MemberList:
                                    if user.ID != UserID:
                                        user.Rect = pygame.Rect(self.screen_size[0] * 10.5 / 12, t,
                                                                self.screen_size[0] * 1.5 / 12,
                                                                self.screen_size[1] * 1 / 20)
                                        t += self.screen_size[1] * 1 / 20
                                        tempL.append(user)
                                x.MemberList = tempL


        except Exception as e:
            print("Closed")

    def GetUserName(self, ID, list):
        for Name in list:
            if Name.ID == ID:
                return Name.UserName
