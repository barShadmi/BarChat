import pygame
import threading


class Log_in(threading.Thread):
    def __init__(self, path, Incorrect, screen_size, BlackBox, Icon, Lato, Lato_Clean, BackGroundBlob1, screen):
        self.RUN = True
        self.path = path
        self.Incorrect = Incorrect
        self.screen_size = screen_size
        self.BlackBox = BlackBox
        self.Icon = Icon
        self.Lato = Lato
        self.Lato_Clean = Lato_Clean
        self.screen = screen
        self.BackGroundBlob1 = BackGroundBlob1
        threading.Thread.__init__(self)

    def run(self):
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
        UserName = self.Lato_Clean.render("USERNAME", True, (200, 200, 210))
        UserNameRect = UserName.get_rect()
        UserNameRect.topleft = (SignInMassRect.topleft[0], BlackBoxRect.topleft[1] + (
                BlackBoxRect.bottomleft[1] - BlackBoxRect.topleft[1]) * 1 / 4)

        IncorrectUserName = self.Lato_Clean.render("USERNAME - Incorrect password or username", True, (200, 0, 0))
        IncorrectUserNameRect = IncorrectUserName.get_rect()
        IncorrectUserNameRect.topleft = UserNameRect.topleft
        UserNameBar = pygame.Rect(SignInMassRect.topleft[0], UserNameRect.bottomleft[1] + 10, 500, 40)

        PassWord = self.Lato_Clean.render("PASSWORD", True, (200, 200, 210))
        PassWordRect = UserName.get_rect()
        PassWordRect.topleft = (UserNameBar.bottomleft[0], UserNameBar.bottomleft[1] + 20)
        PassWordBar = pygame.Rect(UserNameBar[0], PassWordRect.bottomleft[1] + 10, UserNameBar[2], UserNameBar[3])

        LogIn = pygame.Rect(UserNameBar[0], PassWordBar.bottomleft[1] + 50, UserNameBar[2], UserNameBar[3])
        LogInMass1 = self.Lato_Clean.render("*", True, (255, 255, 255))
        LogInMassR1 = LogInMass1.get_rect()
        LogInMass2 = self.Lato_Clean.render("**", True, (255, 255, 255))
        LogInMassR2 = LogInMass2.get_rect()
        LogInMass3 = self.Lato_Clean.render("***", True, (255, 255, 255))
        LogInMassR3 = LogInMass3.get_rect()
        LogInMassR3.center = LogIn.center
        LogInMassR2.center = LogIn.center
        LogInMassR1.center = LogIn.center
        index = 1
        clock = pygame.time.Clock()
        while self.RUN:
            events = pygame.event.get()
            try:
                self.Check_If_Close(events)
            except Exception as e:
                print(e)
            if index == 1:
                LogInMass = LogInMass1
                LogInMassR = LogInMassR1

            if index == 2:
                LogInMass = LogInMass2
                LogInMassR = LogInMassR2

            if index == 3:
                LogInMass = LogInMass3
                LogInMassR = LogInMassR3

            self.screen.blit(self.BackGroundBlob1, (0, 0))
            self.screen.blit(self.BlackBox, BlackBoxRect)
            self.screen.blit(Icon, Icon_rect)
            self.screen.blit(Welcome_Back, Welcome_BackRect)
            self.screen.blit(Welcome_Back2, Welcome_BackRect2)
            self.screen.blit(UserName, UserNameRect)
            self.screen.blit(PassWord, PassWordRect)

            pygame.draw.rect(self.screen, (56, 52, 60), UserNameBar, 0, 4)
            pygame.draw.rect(self.screen, (40, 37, 41), UserNameBar, 1, 4)

            if UserNameBar.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(self.screen, (6, 6, 7), UserNameBar, 1, 4)

            pygame.draw.rect(self.screen, (64, 68, 164), LogIn, 0, 4)

            pygame.draw.rect(self.screen, (56, 52, 60), PassWordBar, 0, 4)
            pygame.draw.rect(self.screen, (40, 37, 41), PassWordBar, 1, 4)

            if PassWordBar.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(self.screen, (6, 6, 7), PassWordBar, 1, 4)
            self.screen.blit(LogInMass, LogInMassR)
            print(index)
            if index == 3:
                index = 1
            else:
                index += 1
            clock.tick(4)
            pygame.display.update()

    def Check_If_Close(self, events):
        try:
            for event in events:
                if event.type == pygame.QUIT:
                    self.Close()
        except Exception as e:
            print(e)

    def Stop(self):
        self.RUN = False

    def Close(self):
        quit()


class Sign_in(threading.Thread):
    def __init__(self, path, Incorrect, screen_size, Lato, Lato2, Lato_Clean, screen, BackGroundBlob2, BlackBox):
        self.path = path
        self.Incorrect = Incorrect
        self.screen_size = screen_size
        self.Lato = Lato
        self.Lato_Clean = Lato_Clean
        self.screen = screen
        self.BackGroundBlob2 = BackGroundBlob2
        self.BlackBox = BlackBox
        self.Lato2 = Lato2
        self.RUN = True
        threading.Thread.__init__(self)

    def run(self):
        flag = False
        BlackBoxRect = self.BlackBox.get_rect()
        BlackBoxRect.center = (self.screen_size[0] / 2, self.screen_size[1] / 2)
        clock = pygame.time.Clock()
        Icon = pygame.transform.scale(pygame.image.load(self.path), (300, 300))
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

        SignInMassLink = self.Lato.render("Log In", True, (57, 136, 255))
        SignInMassLinkRect = SignInMass.get_rect()
        SignInMassLinkRect.topleft = SignInMassRect.topright

        SignInMassLinkU = self.Lato.render("Log In", True, (57, 136, 255))
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
        UserNameTextBoxR = pygame.Rect(UserNameBar.topleft[0] + 3, UserNameBar.topleft[1] + 2, 500, 40)
        PassWord = self.Lato_Clean.render("PASSWORD", True, (200, 200, 210))
        PassWordRect = UserName.get_rect()
        PassWordRect.topleft = (UserNameBar.bottomleft[0], UserNameBar.bottomleft[1] + 20)
        RawPassWord = self.Lato_Clean.render("PASSWORD - Must Use 2-32 Chars From 0-9,aA-zZ.:,;'\"(!?)-*/=", True,
                                             (200, 0, 0))
        RawPassWordRect = RawPassWord.get_rect()

        RawPassWordRect.topleft = PassWordRect.topleft
        PassWordBar = pygame.Rect(UserNameBar[0], PassWordRect.bottomleft[1] + 10, UserNameBar[2], UserNameBar[3])
        PassWordTextBoxR = pygame.Rect(PassWordBar.topleft[0] + 3, PassWordBar.topleft[1] + 2, 500, 40)

        PassWordBar2 = pygame.Rect(UserNameBar[0], PassWordRect.bottomleft[1] + 70, UserNameBar[2], UserNameBar[3])

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
        LogInMass1 = self.Lato_Clean.render("*", True, (255, 255, 255))
        LogInMassR1 = LogInMass1.get_rect()
        LogInMass2 = self.Lato_Clean.render("**", True, (255, 255, 255))
        LogInMassR2 = LogInMass2.get_rect()
        LogInMass3 = self.Lato_Clean.render("***", True, (255, 255, 255))
        LogInMassR3 = LogInMass3.get_rect()
        LogInMassR3.center = LogIn.center
        LogInMassR2.center = LogIn.center
        LogInMassR1.center = LogIn.center
        index = 1
        ENTER = False
        WriteUser = False
        WritePass = False
        WritePass2 = False
        while self.RUN:
            ENTER = False

            events = pygame.event.get()
            try:
                self.Check_If_Close(events)
            except Exception as e:
                print(e)
            if index == 1:
                LogInMass = LogInMass1
                LogInMassR = LogInMassR1

            if index == 2:
                LogInMass = LogInMass2
                LogInMassR = LogInMassR2

            if index == 3:
                LogInMass = LogInMass3
                LogInMassR = LogInMassR3
            self.screen.blit(self.BackGroundBlob2, (0, 0))
            self.screen.blit(self.BlackBox, BlackBoxRect)
            self.screen.blit(Icon, Icon_rect)
            self.screen.blit(Welcome_Back, Welcome_BackRect)
            self.screen.blit(Welcome_Back2, Welcome_BackRect2)
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

            pygame.draw.rect(self.screen, (240, 68, 68), Clear_Button, 0, 4)
            self.screen.blit(Clear_Button_Mass, Clear_Button_MassR)

            pygame.draw.rect(self.screen, (96, 100, 244), Change_Button, 0, 4)
            self.screen.blit(Change_Button_Mass, Change_Button_MassR)

            self.screen.blit(LogInMass, LogInMassR)
            if index == 3:
                index = 1
            else:
                index += 1
            pygame.display.update()
            clock.tick(4)

    def Check_If_Close(self, events):
        try:
            for event in events:
                if event.type == pygame.QUIT:
                    self.Close()
        except Exception as e:
            print(e)

    def Stop(self):
        self.RUN = False

    def Close(self):
        quit()


class Loading(threading.Thread):
    def __init__(self, icon, photo, Lato, screen_size, screen):
        self.screen_size = screen_size
        self.screen = screen
        self.photo = photo
        self.Lato = Lato
        self.Icon = icon
        self.RUN = True
        threading.Thread.__init__(self)

    def run(self):
        size = (500,500)
        Icon = self.Icon
        self.Icon = pygame.transform.scale(Icon, size)
        IconR = self.Icon.get_rect()
        IconR.center = (self.screen_size[0] / 2, self.screen_size[1] / 2)
        self.photo = pygame.transform.scale(self.photo, self.screen_size)
        events = pygame.event.get()
        self.Check_If_Close(events)
        self.text1 = self.Lato.render("Loading", True,(255, 255, 255))
        self.text2 = self.Lato.render("Loading.", True,(255, 255, 255))
        self.text3 = self.Lato.render("Loading..", True,(255, 255, 255))
        self.text4 = self.Lato.render("Loading...", True,(255, 255, 255))
        self.text1R = self.text1.get_rect()
        self.text1R.topleft = (self.screen_size[0]* 1 / 3, self.screen_size[1]*3/4)
        self.text2R = self.text1.get_rect()
        self.text2R.topleft = (self.screen_size[0] * 1 / 3, self.screen_size[1]*3 / 4)
        self.text3R = self.text1.get_rect()
        self.text3R.topleft = (self.screen_size[0] * 1 / 3, self.screen_size[1]*3 / 4)
        self.text4R = self.text1.get_rect()
        self.text4R.topleft = (self.screen_size[0] * 1 / 3, self.screen_size[1]*3 / 4)
        index = 1
        temp = self.text1
        tempR = self.text1R
        clock = pygame.time.Clock()
        flag =[True, False]
        while self.RUN:
            self.screen.blit(self.photo, (0,0))
            if index == 1:
                temp = self.text1
                tempR = self.text1R
            if index == 26:
                temp = self.text2
                tempR = self.text2R
            if index == 50:
                temp = self.text3
                tempR = self.text3R
            if index == 75:
                temp = self.text4
                tempR = self.text4R
            self.screen.blit(temp, tempR)
            if flag[1]:
                size = (size[0] -1, size[1] - 1)
            if flag[0]:
                size = (size[0] +1, size[1] + 1)
            self.Icon = pygame.transform.scale(Icon, size)
            IconR = self.Icon.get_rect()
            IconR.center = (self.screen_size[0]/2, self.screen_size[1]/2)
            self.screen.blit(self.Icon, IconR)

            if index == 100:
                index = 1
            else:
                index += 1
            if IconR[2] >= 600:
                flag = [False, True]
            if IconR[2] <= 400:
                flag = [True, False]
            clock.tick(100)
            pygame.display.update()

    def Check_If_Close(self, events):
        try:
            for event in events:
                if event.type == pygame.QUIT:
                    self.Close()
        except Exception as e:
            print(e)
    def Close(self):
        quit()