import keyboard
import os
import math
import psutil
import pygame.display
import time
import win32api
from Modules import startcsgo
from Modules.startcsgo import RestartSteam
import win32con
import win32gui
import subprocess
from pynput.mouse import Controller
from hashlib import sha256
from Modules.LicenseChecker import GetActiveAccount, CheckValid, GetWebHelpersList
from Modules.Generator import Generator
from ServerDB.Client import CheckIfUserExists, CheckIfPasswordIsCorrect, CheckIfUserLicenseIsValid

default_font_size = 15
default_font = "Microsoft Sans Serif"
ChangeAlpha = False

SmoothedR = 255
SmoothedG = 255
SmoothedB = 255
def color_surface(surface, color, fps):
    global SmoothedR, SmoothedG, SmoothedB
    arr = pygame.surfarray.pixels3d(surface)
    if fps == 0:
        SmoothedR -= (SmoothedR - color[0]) / 20
        SmoothedG -= (SmoothedG - color[1]) / 20
        SmoothedB -= (SmoothedB - color[2]) / 20
    else:
        SmoothedR -= (SmoothedR - color[0]) / (1 / fps) * 8
        SmoothedG -= (SmoothedG - color[1]) / (1 / fps) * 8
        SmoothedB -= (SmoothedB - color[2]) / (1 / fps) * 8
    for x in range(0, len(arr)):
        for y in range(0, len(arr[x])):
            if arr[x][y][0] != 0 and arr[x][y][1] != 0 and arr[x][y][2] != 0:
                arr[x][y][0] = clamp(arr[x][y][0] - 255 + SmoothedR, 0, 255)
                arr[x][y][1] = clamp(arr[x][y][1] - 255 + SmoothedG, 0, 255)
                arr[x][y][2] = clamp(arr[x][y][2] - 255 + SmoothedB, 0, 255)

class Colors():
    Background = (20, 20, 20, 150)      # background
    AlphaAnim = False
    HighlightBackground = (20, 40, 60)  # background slider / selector etc
    TextColor = (200, 200, 200)         # textcolor
    DisableColor = (20, 20, 20)
    ColorStyle = (40, 60, 80)           # slider red on start
    Transparency = 100

    pygame.font.init()
    FontBig = pygame.font.SysFont("Microsoft Sans Serif", 20, False, False)
    FontMed = pygame.font.SysFont("Microsoft Sans Serif", 15, False, False)
    FontSmall = pygame.font.SysFont("Microsoft Sans Serif", 14, False, False)

def clamp(num, min_value, max_value):
    num = max(min(num, max_value), min_value)
    return num

def Initscreen(resolution):
    screen = pygame.display.set_mode(resolution, pygame.NOFRAME)
    return screen

class Window():
    def __init__(self, resolution, position, screen):
        # window
        pygame.display.set_caption("Future")
        self.resolution = resolution
        self.ActiveModuleRes = resolution
        self.position = position
        self.CustomMouse = Controller()
        self.Foreground = True
        self.logo = pygame.image.load("Data\Images\Icon.png")
        self.starttime = time.time()

        self.screen = screen
        self.clicked = (0, 0)
        pygame.display.set_icon(self.logo)

        Window = win32gui.FindWindow(None, "Future")
        win32gui.SetWindowLong(Window, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(Window, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
        win32gui.SetLayeredWindowAttributes(Window, win32api.RGB(0, 0, 0), 210, win32con.LWA_ALPHA)

        self.Alpha = 210

        self.origSurface = self.logo
        self.origSurface.convert_alpha()
        self.LogoUpdate = False
        self.coloredSurface = self.logo
        self.clock = pygame.time.Clock()

        self.active_modules_dimensions = [120, 20]
        self.active_modules_margin = (10, 500)


    def Update(self, ActiveModules, Framedelta, is_login_screen):
        Window = win32gui.FindWindow(None, "Future")
        WindowRect = win32gui.GetWindowRect(Window)

        Mousepos = pygame.mouse.get_pos()

        self.screen.fill(Colors.Background)
        # main window
        if self.Foreground == True:

            # logo color change
            if self.LogoUpdate == True:
                self.coloredSurface = self.origSurface.copy()
                color_surface(self.coloredSurface, Colors.ColorStyle, self.clock.get_fps())

            self.screen.blit(self.coloredSurface, (10, 10))

            if abs(pygame.Surface.get_at(self.screen, (20, 20))[:-1][0] - Colors.ColorStyle[0]) > 2 or \
                    abs(pygame.Surface.get_at(self.screen, (20, 20))[:-1][1] - Colors.ColorStyle[1]) > 2 or \
                    abs(pygame.Surface.get_at(self.screen, (20, 20))[:-1][2] - Colors.ColorStyle[2]) > 2:

                self.LogoUpdate = True
            else:
                self.LogoUpdate = False


            # exit button
            close_button_rect = Colors.FontBig.render("x", True, (150, 50, 50))
            self.screen.blit(close_button_rect, (self.resolution[0] - close_button_rect.get_width() - 2, -4))


            for event in pygame.event.get():
                if Mousepos[0] > self.resolution[0] - close_button_rect.get_width() and Mousepos[0] < self.resolution[0] and Mousepos[1] > 0 and Mousepos[1] < close_button_rect.get_height():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pygame.quit()
                        exit(0)

                if Mousepos[0] > 0 and Mousepos[0] < self.resolution[0] - close_button_rect.get_width() and Mousepos[1] > 0 and Mousepos[1] < 35:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.clicked = (Mousepos[0], Mousepos[1])
                    if event.type == pygame.MOUSEBUTTONUP:
                        self.clicked = (0, 0)

                if event.type == pygame.MOUSEBUTTONUP:
                    self.clicked = (0, 0)


            if self.clicked != (0, 0):
                win32gui.SetWindowPos(Window, None, self.CustomMouse.position[0] - self.clicked[0], self.CustomMouse.position[1] - self.clicked[1], 0, 0, 1)

        else:
            Window = win32gui.FindWindow(None, "Future")
            WindowRect = win32gui.GetWindowRect(Window)
            # active module window
            if self.screen.get_rect()[2] != self.ActiveModuleRes[0] or self.screen.get_rect()[3] != self.ActiveModuleRes[1]:
                self.screen = pygame.display.set_mode(self.ActiveModuleRes, pygame.NOFRAME)
                self.screen.fill(Colors.Background)

            Toprect = Colors.FontSmall.render(str("Active Modules"), True, (200, 200, 200))
            self.screen.blit(Toprect, ((WindowRect[2] - WindowRect[0])/2 - Toprect.get_width()/2, 1))
            pygame.draw.rect(self.screen, (255, 255, 255), (10, Toprect.get_height(), Toprect.get_width(), 1))
            if len(ActiveModules) > 0:
                for I in range(0, len(ActiveModules)):
                    rect = Colors.FontSmall.render(str(ActiveModules[I]), True, (200, 200, 200))
                    self.screen.blit(rect, (self.ActiveModuleRes[0]/2 - rect.get_width()/2, Toprect.get_height() + rect.get_height() * I))

                self.active_modules_dimensions[1] = rect.get_height() * (len(ActiveModules) + 1)
            else:
                self.active_modules_dimensions[1] = Toprect.get_height()

            # print(Height, self.screen.get_rect()[3])
            if self.active_modules_dimensions[1] != self.screen.get_rect()[3]:
                self.ActiveModuleRes = (self.ActiveModuleRes[0], self.active_modules_dimensions[1])

            if WindowRect != (self.active_modules_margin[0], self.active_modules_margin[1], self.active_modules_margin[0] + self.ActiveModuleRes[0], self.active_modules_margin[1] + self.ActiveModuleRes[1]):
                win32gui.SetWindowPos(Window, win32con.HWND_TOPMOST, self.active_modules_margin[0], self.active_modules_margin[1], 0, 0, win32con.SWP_NOSIZE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

        if not is_login_screen:
            if keyboard.is_pressed("right_shift") and self.Foreground == True and self.starttime + 0.15 < time.time():
                self.starttime = time.time()
                Window = win32gui.FindWindow(None, "Future")
                WindowRect = win32gui.GetWindowRect(Window)
                win32gui.SetWindowLong(Window, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(Window, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
                win32gui.SetLayeredWindowAttributes(Window, win32api.RGB(0, 0, 0), 160, win32con.LWA_ALPHA)
                rect = win32gui.GetWindowRect(Window)
                win32gui.SetWindowPos(Window, win32con.HWND_TOPMOST, rect[0], rect[1], 0, 0, win32con.SWP_NOSIZE)
                self.ActiveModuleRes = (self.active_modules_dimensions[0], self.active_modules_dimensions[1])
                self.position = (rect[1], rect[0])
                self.Foreground = False

            elif keyboard.is_pressed("right_shift") and self.Foreground == False and self.starttime + 0.15 < time.time():
                self.starttime = time.time()
                Window = win32gui.FindWindow(None, "Future")
                WindowRect = win32gui.GetWindowRect(Window)
                win32gui.SetWindowLong(Window, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(Window, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
                win32gui.SetLayeredWindowAttributes(Window, win32api.RGB(0, 0, 0), 210, win32con.LWA_ALPHA)
                win32gui.SetWindowPos(Window, win32con.HWND_TOPMOST, self.position[1], self.position[0], 0, 0, win32con.SWP_NOSIZE)
                pygame.display.set_mode(self.resolution, pygame.NOFRAME)
                self.Foreground = True

        global ChangeAlpha
        if ChangeAlpha == True:
            # changing alpha
            if self.CustomMouse.position[0] > WindowRect[0] and self.CustomMouse.position[0] < WindowRect[2] and self.CustomMouse.position[1] > WindowRect[1] and self.CustomMouse.position[1] < WindowRect[3]:
                self.Alpha -= (self.Alpha - 255) * (1 / Framedelta) * 16
            else:
                self.Alpha -= (self.Alpha - Colors.Transparency) * (1 / Framedelta) * 16

            res = (round(clamp(self.Alpha, 0, 255)))
            if res == 0 or res == 256:
                print(res)
            win32gui.SetLayeredWindowAttributes(Window, win32api.RGB(0, 0, 0), round(clamp(self.Alpha, 0, 255)), win32con.LWA_ALPHA)
        else:
            win32gui.SetLayeredWindowAttributes(Window, win32api.RGB(0, 0, 0), 255, win32con.ULW_ALPHA)

        if is_login_screen:
            return False

        return self.Foreground

class Button():
    def __init__(self, position, size, name, State=False, Tab=False):

        self.position = position
        self.size = size
        self.name = name
        self.State = State
        self.DelayTime = time.time()
        self.Tab = Tab
        self.rounding = 0

        self.starttime = time.time()
        self.show = False
        self.CustomColorR = Colors.DisableColor[0]
        self.CustomColorG = Colors.DisableColor[1]
        self.CustomColorB = Colors.DisableColor[2]
        self.CustomColor = (self.CustomColorR, self.CustomColorG, self.CustomColorB)


    def Update(self, screen, mousepos, framedelta):

        if mousepos[0] > self.position[0] and mousepos[0] < self.position[0] + self.size[0] and mousepos[1] > self.position[1] and mousepos[1] < self.position[1] + self.size[1]:

            if pygame.mouse.get_pressed()[0] and self.DelayTime + 0.15 <= time.time():
                self.State = not self.State
                self.DelayTime = time.time()

            if pygame.mouse.get_pressed()[2] and self.DelayTime + 0.15 <= time.time():
                self.Tab = not self.Tab
                self.DelayTime = time.time()

        if self.show == True and self.State == True:
            # color animation
            self.CustomColorR -= (self.CustomColorR - Colors.ColorStyle[0]) * (1 / framedelta) * 3
            self.CustomColorG -= (self.CustomColorG - Colors.ColorStyle[1]) * (1 / framedelta) * 3
            self.CustomColorB -= (self.CustomColorB - Colors.ColorStyle[2]) * (1 / framedelta) * 3
            self.CustomColor = (clamp(self.CustomColorR, 0, 255), clamp(self.CustomColorG, 0, 255), clamp(self.CustomColorB, 0, 255))
            # button design
            pygame.draw.rect(screen, Colors.ColorStyle, (self.position[0], self.position[1], self.size[0], self.size[1]), border_radius=self.rounding)
            pygame.draw.rect(screen, self.CustomColor, (self.position[0] + 2, self.position[1] + 2, self.size[0] - 4, self.size[1] - 4), border_radius=self.rounding)
            rect = Colors.FontMed.render(str(self.name), True, (0, 0, 0))
            screen.blit(rect, (self.position[0] - round(rect.get_width() / 2) + round(self.size[0] / 2), self.position[1] + 3))
        else:
            # color animation
            self.CustomColorR -= (self.CustomColorR - Colors.DisableColor[0]) * (1 / framedelta) * 10
            self.CustomColorG -= (self.CustomColorG - Colors.DisableColor[1]) * (1 / framedelta) * 10
            self.CustomColorB -= (self.CustomColorB - Colors.DisableColor[2]) * (1 / framedelta) * 10
            self.CustomColor = (clamp(self.CustomColorR, 0, 255), clamp(self.CustomColorG, 0, 255), clamp(self.CustomColorB, 0, 255))

            # button design
            pygame.draw.rect(screen, Colors.ColorStyle, (self.position[0], self.position[1], self.size[0], self.size[1]), border_radius=self.rounding)
            pygame.draw.rect(screen, self.CustomColor, (self.position[0] + 2, self.position[1] + 2, self.size[0] - 4, self.size[1] - 4), border_radius=self.rounding)
            rect = Colors.FontMed.render(str(self.name), True, Colors.TextColor)
            screen.blit(rect, (self.position[0] - round(rect.get_width() / 2) + round(self.size[0] / 2), self.position[1] + 3))

        if self.show == False:
            self.CustomColor = Colors.DisableColor
            self.CustomColorR = Colors.DisableColor[0]
            self.CustomColorG = Colors.DisableColor[1]
            self.CustomColorB = Colors.DisableColor[2]

        return self.State, self.Tab

def Refreshscreen():
    pygame.display.flip()

class Slider():
    def __init__(self, position, size, name, start, end):
        self.position = position
        self.size = size
        self.name = name
        self.start = start
        self.end = end
        self.State = 0
        self.OutputState = 0
        self.OutputTab = False
        self.slider_size = (10, 30)
        self.show = False
        self.SliderVisState = 0
        self.Mbdown = False
        self.rounding = 0
        self.Multiplier = (self.end - self.start) / self.size[0]
        self.VisualState = round(self.start + self.State * self.Multiplier)

        pygame.font.init()
        self.font = pygame.font.SysFont("Microsoft Sans Serif", 15, False, False)

    def UpdateState(self):
        self.VisualState = round(self.start + self.State * self.Multiplier)

    def Update(self, screen, mousepos, framedelta):
        pygame.draw.rect(screen, Colors.HighlightBackground, (self.position[0], self.position[1], self.size[0], 5), border_radius=self.rounding)
        pygame.draw.rect(screen, Colors.ColorStyle, (self.position[0], self.position[1], self.SliderVisState, 5), border_radius=self.rounding)

        self.VisualState = round(self.start + self.State * self.Multiplier)
        self.SliderVisState -= (self.SliderVisState - self.State) * (1 / framedelta) * 12

        rect = self.font.render(str(self.VisualState), True, Colors.TextColor)
        screen.blit(self.font.render(str(self.name), True, Colors.TextColor), (self.position[0], self.position[1] - 20))

        if mousepos[0] > self.position[0] - 1 and mousepos[0] < self.position[0] + self.size[0] + 1 and mousepos[1] > self.position[1] and mousepos[1] < self.position[1] + self.size[1]:
            if pygame.mouse.get_pressed()[0]:
                self.Mbdown = True

        if pygame.mouse.get_pressed()[0] == False:
            self.Mbdown = False

        if self.Mbdown == True:
            if mousepos[0] > self.position[0] - 1 and mousepos[0] < self.position[0] + self.size[0] + 1:
                self.State = (mousepos[0] - self.position[0])

            if mousepos[0] > self.position[0] + self.size[0]:
                self.State = self.size[0]

            if mousepos[0] < self.position[0]:
                self.State = 0

        screen.blit(rect, (self.position[0] + self.size[0] - rect.get_width(), self.position[1] + 5))


        if self.show == False:
            self.SliderVisState = 0

        return self.VisualState, self.OutputTab


class Selector():
    def __init__(self, position, size, name, array):
        self.position = position
        self.size = size
        self.rounding = 0
        self.array = array
        self.name = name

        self.selected = 0

        self.clicked = False
        self.Delaytime = time.time()
        self.iwannadie = 0


    def Update(self, screen, mousepos, framedelta):
        baserect = pygame.draw.rect(screen, Colors.HighlightBackground, (self.position[0], self.position[1], self.size[0], self.size[1]), border_radius=self.rounding)

        rect = Colors.FontMed.render(str(self.array[self.selected]), True, Colors.TextColor)
        screen.blit(rect, (baserect.centerx - rect.get_width()/2, baserect.centery - rect.get_height()/2))

        if baserect.collidepoint(mousepos[0], mousepos[1]):
            if pygame.mouse.get_pressed()[0] and self.Delaytime + 0.15 < time.time():
                self.clicked = not self.clicked
                self.Delaytime = time.time()



        if self.clicked == True:
            pygame.draw.rect(screen, Colors.HighlightBackground, (self.position[0], self.position[1], self.size[0], rect.get_height() * len(self.array) + ((baserect.centery - rect.get_height()/2)-self.position[1])*2))


            for i in range(0, len(self.array)):

                rect = Colors.FontMed.render(str(self.array[i]), True, Colors.TextColor)
                screen.blit(rect, (baserect.centerx - rect.get_width()/2, baserect.centery - rect.get_height()/2 + rect.get_height()*i))

                if mousepos[0] > self.position[0] and mousepos[0] < self.position[0] + self.size[0]:
                    if mousepos[1] > self.position[1] + rect.get_height() * i and mousepos[1] < self.position[1] + rect.get_height() * (i+1):
                        pygame.draw.rect(screen, (255, 255, 255), (self.position[0], self.position[1] + rect.get_height() * i, self.size[0], rect.get_height() + ((baserect.centery - rect.get_height()/2)-self.position[1])*2), width=1)
                        if pygame.mouse.get_pressed()[0] and self.Delaytime + 0.15 < time.time():
                            self.Delaytime = time.time()
                            self.selected = i
                            self.clicked = False
                            self.iwannadie = self.array[self.selected]
                            self.array.pop(self.selected)
                            self.array = [self.iwannadie] + self.array
                            self.selected = 0

        return self.array[self.selected], self.clicked

class ColorPicker():
    def __init__(self, position, size, name):
        self.name = name
        self.position = position
        self.State = True
        self.size = size
        self.Outputstate = (0, 0, 0)
        self.image = pygame.image.load("Data\Images\picker.png")
        self.image = pygame.transform.scale(self.image, size)
        # self.image = pygame.draw.circle(self.image, (255, 0, 0), (100, 100), 5)
        self.picker = pygame.image.load("Data\Images\circle.png")
        self.picker = pygame.transform.scale(self.picker, (self.image.get_width() / 12, self.image.get_height() / 12))
        self.picker_x, self.picker_y = self.position[0] + self.image.get_width() / 2 - self.picker.get_width() / 2, self.position[1] + self.image.get_height() / 2 - self.picker.get_height() / 2
        self.color = (255, 255, 255)
        self.color_display_size = (self.image.get_width(), 20)
        self.color_display_rounding = 0
        self.font = default_font
        self.font_size = default_font_size

        self.brightness = 0
        self.processedcolor = self.color
        self.starttime = time.time()
        self.opened = False


    def Update(self, screen, mousepos, framedelta):
        if self.opened == True:
            screen.blit(self.image, (self.position[0], self.position[1]))
            screen.blit(self.picker, (self.picker_x, self.picker_y))

            if mousepos[0] > self.position[0] and mousepos[0] < self.image.get_width() + self.position[0] and mousepos[1] > self.position[1] and mousepos[1] < self.image.get_height() + self.position[1]:
                if pygame.mouse.get_pressed()[0]:
                    self.picker_x, self.picker_y = mousepos[0] - self.picker.get_width() / 2, mousepos[1] - self.picker.get_height() / 2
                    self.color = (screen.get_at((int(mousepos[0]), int(mousepos[1]))))[:3]
                    self.processedcolor = (clamp(round(self.color[0] - self.brightness * (255 / self.size[1])), 0, 255),
                                           clamp(round(self.color[1] - self.brightness * (255 / self.size[1])), 0, 255),
                                           clamp(round(self.color[2] - self.brightness * (255 / self.size[1])), 0, 255))

            # darkness slider
            pygame.draw.rect(screen, Colors.HighlightBackground, (self.position[0] + self.size[0] + 5, self.position[1], 5, self.size[1]))
            pygame.draw.rect(screen, self.processedcolor, (self.position[0] + self.size[0] + 5, self.position[1] + self.brightness, 5, self.size[1] - self.brightness))

            if mousepos[0] > self.position[0] + self.size[0] + 5 and mousepos[0] < self.position[0] + self.size[1] + 10 and mousepos[1] > self.position[1] - 1 and mousepos[1] < self.position[1] + self.size[1] + 1:
                if pygame.mouse.get_pressed()[0] == True:
                    self.brightness = mousepos[1] - self.position[1]
                    self.processedcolor = (clamp(round(self.color[0] - self.brightness * (255 / self.size[1])), 0, 255),
                                           clamp(round(self.color[1] - self.brightness * (255 / self.size[1])), 0, 255),
                                           clamp(round(self.color[2] - self.brightness * (255 / self.size[1])), 0, 255))

            if mousepos[0] > self.position[0] and mousepos[0] < self.position[0] + self.size[0] and mousepos[1] > self.position[1] and mousepos[1] < self.size[1] + self.position[1]:
                if pygame.mouse.get_pressed()[2] == True:
                    if self.starttime + 0.25 < time.time():
                        self.starttime = time.time()
                        self.opened = not self.opened
        else:
            pygame.draw.rect(screen, self.processedcolor, (self.position[0], self.position[1], 30, 30))
            screen.blit(Colors.FontMed.render(str(self.name), True, self.processedcolor), (self.position[0], self.position[1] + 30))


            if mousepos[0] > self.position[0] and mousepos[0] < self.position[0] + 30 and mousepos[1] > self.position[1] and mousepos[1] < 30 + self.position[1]:
                if pygame.mouse.get_pressed()[2] == True:
                    if self.starttime + 0.25 < time.time():
                        self.starttime = time.time()
                        self.opened = not self.opened

        return self.processedcolor

class Checkbox():
    def __init__(self, pos, size, name, color):
        self.pos = pos
        self.size = size
        self.name = name
        self.color = color
        self.clicked = False
        self.delaytime = time.time()
        self.show = False
        self.CustomColorR = Colors.DisableColor[0]
        self.CustomColorG = Colors.DisableColor[1]
        self.CustomColorB = Colors.DisableColor[2]
        self.CustomColor = (self.CustomColorR, self.CustomColorG, self.CustomColorB)

    def Update(self, screen, Mousepos, framedelta):



        if Mousepos[0] > self.pos[0] and Mousepos[0] < self.pos[0] + self.size[0] and Mousepos[1] > self.pos[1] and Mousepos[1] < self.pos[1] + self.size[1]:
            if pygame.mouse.get_pressed()[0] and self.delaytime + 0.1 < time.time():
                self.clicked = not self.clicked
                self.delaytime = time.time()


        if self.show == True and self.clicked == True:
            self.CustomColorR -= (self.CustomColorR - Colors.ColorStyle[0]) * (1 / framedelta) * 7
            self.CustomColorG -= (self.CustomColorG - Colors.ColorStyle[1]) * (1 / framedelta) * 7
            self.CustomColorB -= (self.CustomColorB - Colors.ColorStyle[2]) * (1 / framedelta) * 7
            self.CustomColor = (clamp(self.CustomColorR, 0, 255), clamp(self.CustomColorG, 0, 255), clamp(self.CustomColorB, 0, 255))
        else:
            self.CustomColorR -= (self.CustomColorR - Colors.DisableColor[0]) * (1 / framedelta) * 13
            self.CustomColorG -= (self.CustomColorG - Colors.DisableColor[1]) * (1 / framedelta) * 13
            self.CustomColorB -= (self.CustomColorB - Colors.DisableColor[2]) * (1 / framedelta) * 13
            self.CustomColor = (clamp(self.CustomColorR, 0, 255), clamp(self.CustomColorG, 0, 255), clamp(self.CustomColorB, 0, 255))

        if self.show == False:
            self.CustomColorR = Colors.DisableColor[0]
            self.CustomColorG = Colors.DisableColor[1]
            self.CustomColorB = Colors.DisableColor[2]
            self.CustomColor = Colors.DisableColor

        rect = pygame.draw.rect(screen, self.CustomColor, (self.pos[0], self.pos[1], self.size[0], self.size[1]))
        rect = pygame.draw.rect(screen, Colors.ColorStyle, (self.pos[0], self.pos[1], self.size[0], self.size[1]), width=2)


        textrect = Colors.FontMed.render(str(self.name), True, Colors.TextColor)
        screen.blit(textrect, (self.pos[0] + self.size[0] + 5, rect.centery - textrect.get_height()/2))

        return self.clicked

class Searchbox():
    def __init__(self, position, size, name, array):
        self.position = position
        self.size = size
        self.rounding = 0

        self.name = name
        self.array = array
        self.foundarray = []
        self.selected = 0
        self.clicked = False
        self.Delaytime = time.time()
        self.show = time.time()
        self.showing = False

        self.text = ""
        self.textstop = False

    def Update(self, screen, mousepos, framedelta):
        rectangle = pygame.draw.rect(screen, Colors.HighlightBackground, (self.position[0], self.position[1], self.size[0], self.size[1]), border_radius=self.rounding)

        namerect = Colors.FontMed.render(str(self.name), True, Colors.TextColor)
        screen.blit(namerect, (rectangle.centerx - namerect.get_width() / 2, self.position[1] - namerect.get_height()))

        if mousepos[0] > self.position[0] and mousepos[0] < self.position[0] + self.size[0] and mousepos[1] > self.position[1] and mousepos[1] < self.position[1] + self.size[1]:
            if pygame.mouse.get_pressed()[0] == True and self.Delaytime < time.time():
                self.clicked = not self.clicked
                self.Delaytime = time.time() + 0.5
        else:
            if pygame.mouse.get_pressed()[0] == True:
                self.clicked = False

        text = Colors.FontMed.render(str(self.text), True, Colors.TextColor)
        screen.blit(text, (self.position[0], rectangle.centery - text.get_height() / 2))

        # text input
        if self.clicked == True:

            if keyboard.get_hotkey_name() != "space" and keyboard.get_hotkey_name() != "enter" and keyboard.get_hotkey_name() != "backspace":
                if self.textstop == False:
                    self.text += keyboard.get_hotkey_name()
                    self.textstop = True

                if keyboard.get_hotkey_name() == "":
                    self.textstop = False
            else:
                if keyboard.get_hotkey_name() == "backspace":
                    if self.textstop == False:
                        self.text = self.text[:-1]
                        self.textstop = True

                    if keyboard.get_hotkey_name() == "":
                        self.textstop = False


            if self.show < time.time():
                self.show = time.time() + 0.5
                self.showing = not self.showing

            if self.showing == True:
                pygame.draw.rect(screen, Colors.TextColor, (self.position[0] + text.get_width(), self.position[1] + 1, 1, self.size[1] - 2), border_radius=self.rounding)


        for element in range(0, len(self.array)):
            if self.text in str(self.array[element]).lower():
                self.foundarray.append(self.array[element])


        for newelelemnt in range(0, len(self.foundarray)):
            elementrect = Colors.FontMed.render(str(self.foundarray[newelelemnt]), True, (255, 255, 255))
            if mousepos[0] > self.position[0] and mousepos[0] < self.position[0] + self.size[0]:
                if mousepos[1] > rectangle.centery - elementrect.get_height()/2 + newelelemnt * elementrect.get_height() + self.size[1]:
                    if mousepos[1] < rectangle.centery - elementrect.get_height()/2 + newelelemnt * elementrect.get_height() + self.size[1] + 17:
                        rectheight = rectangle.centery - elementrect.get_height()/2 + newelelemnt * elementrect.get_height() + self.size[1]
                        rectright = rectangle.centerx - elementrect.get_width() / 2
                        pygame.draw.rect(screen, Colors.TextColor, (rectright - 1, rectheight - 1, elementrect.get_rect()[2] + 2, elementrect.get_rect()[3] + 2))
                        pygame.draw.rect(screen, Colors.HighlightBackground, (rectright, rectheight, elementrect.get_rect()[2], elementrect.get_rect()[3]))
                        if pygame.mouse.get_pressed()[0] == True:
                            self.text = str(self.foundarray[newelelemnt])
            screen.blit(elementrect, (rectangle.centerx - elementrect.get_width() / 2, rectangle.centery - elementrect.get_height() / 2 + newelelemnt * elementrect.get_height() + self.size[1]))


        if len(self.foundarray) > 0:
            self.foundarray.clear()

        return self.array[self.selected], self.clicked

class LogoDisplayer():
    def __init__(self, Speed, ScreenRes):
        self.Speed = Speed
        self.AnimSpeed = 5
        self.res = ScreenRes
        self.FLogo = pygame.image.load("Data/Images/Original.png")
        self.RestLogo = pygame.image.load("Data/Images/Rest.png")
        self.ScaledF = pygame.transform.scale(self.FLogo, (self.FLogo.get_width()*0.35, self.FLogo.get_height()*0.35))
        self.ScaledRest = pygame.transform.scale(self.RestLogo, (self.RestLogo.get_width()*0.35, self.RestLogo.get_height()*0.35))

        self.FLogo_XOffset = 0
        self.RestLogo_XOffset = 500

        self.AnimState = 1
        self.starttime = time.time()
        self.Stockalpha = 255

    def Update(self, framedelta, screen):
        # before animation
        if self.starttime + 1 < time.time() and self.AnimState == 1:
            self.AnimState = 2
            self.starttime = time.time()
            # startanimaton
        # display F UTURE
        if self.AnimState == 2:
            self.FLogo_XOffset -= clamp((self.FLogo_XOffset + 160) / framedelta * self.AnimSpeed, -self.Speed, self.Speed)
            self.RestLogo_XOffset -= clamp((self.RestLogo_XOffset - 95) / framedelta * self.AnimSpeed, -self.Speed*2, self.Speed*2)

        # Go back to original
        if self.RestLogo_XOffset - 95 < 1 and self.AnimState == 2:
            self.AnimState = 3
            self.starttime = time.time()

        # animate going back
        if self.AnimState == 3 and self.starttime + 0.2 < time.time():
            self.FLogo_XOffset -= clamp((self.FLogo_XOffset) / framedelta * self.AnimSpeed, -self.Speed, self.Speed)
            self.RestLogo_XOffset -= clamp((self.RestLogo_XOffset - 500) / framedelta * 2, -self.Speed*2, self.Speed*2)

        # logo fade
        if self.AnimState == 3 and self.FLogo_XOffset > -1:
            self.AnimState = 4
            self.starttime = time.time()

        if self.AnimState == 4 and self.starttime + 0.2 < time.time():
            self.Stockalpha -= clamp((self.Stockalpha) / framedelta * self.AnimSpeed, -self.Speed, self.Speed)
            self.ScaledF.set_alpha(self.Stockalpha)

        # show buttons and all
        if self.AnimState == 4 and self.Stockalpha < 2:
            self.Stockalpha = 0
            self.AnimState = 5


        if self.AnimState < 5:
            pygame.draw.rect(screen, (20, 20, 20), (0, 0, self.res[0], self.res[1]))
            screen.blit(self.ScaledRest, (self.res[0] / 2 - self.ScaledF.get_width() / 2 - self.RestLogo_XOffset, self.res[1] / 2 - self.ScaledF.get_height() / 2))
            pygame.draw.rect(screen, (20, 20, 20), (self.res[0]/2 + self.ScaledF.get_width()/2 + self.FLogo_XOffset - 1000, 0, 1000, self.res[1]))
            screen.blit(self.ScaledF, (self.res[0] / 2 - self.ScaledF.get_width() / 2 + self.FLogo_XOffset,self.res[1] / 2 - self.ScaledF.get_height() / 2))

class Loading():
    def __init__(self):
        self.X = 0
        self.X1 = 0
        self.X2 = 0
        self.alpha = 0

        self.maxsize = 80
        self.size = 0
        self.Color1 = (255, 255, 255)
        self.Color2 = (0, 0, 0)

        self.backcolor = (0, 0, 0)
        self.background = Colors.Background

        self.speed = 0.1

        self.backgroundoverlay = pygame.Surface(pygame.display.get_window_size())
        self.pos = (pygame.display.get_window_size()[0] / 2, pygame.display.get_window_size()[1] / 2)
        self.backgroundoverlay.set_alpha(self.alpha)
        self.backgroundoverlay.fill(self.backcolor)


    def Update(self, screen, State):
        if State == True:
            if self.alpha < 150:
                self.alpha = self.alpha + 2

            if self.size < self.maxsize:
                self.size = self.size + 0.8

        if State == False:
            if self.alpha > 1:
                self.alpha = self.alpha - 2

            if self.size > 1:
                self.size = self.size - 0.8

        if self.size > 1:
            screen.blit(self.backgroundoverlay, (0, 0))
            self.backgroundoverlay.set_alpha(self.alpha)
            self.backgroundoverlay.fill(self.backcolor)


            self.X = self.X + self.speed
            self.X1 = self.X1 + self.speed / 1.9
            self.X2 = self.X2 + self.speed / 4

            speedup = 1 + math.sin(self.X1)
            for i in range(0, 90):
                adder = i / 40 * speedup

                offset = (math.cos(self.X + speedup + adder + self.X2) * self.size, math.sin(self.X + speedup + adder) * self.size)
                self.loadingpos = (self.pos[0] + offset[0], self.pos[1] + offset[1])
                pygame.draw.circle(screen, self.Color1, self.loadingpos, 5)

                shift = 41
                offset = (math.cos(self.X + speedup + adder + self.X2 + shift) * self.size, math.sin(self.X + speedup + adder + shift) * self.size)
                self.loadingpos = (self.pos[0] + offset[0], self.pos[1] + offset[1])
                pygame.draw.circle(screen, self.Color2, self.loadingpos, 6)
        else:
            self.X = 0
            self.X1 = 0
            self.X2 = 0

class LoginScreen():
    def __init__(self):

        startcsgo.Launcher(False, False, False)

        self.state = False

        self.FLogo = pygame.image.load("Data/Images/Original.png")
        self.res = (410, 220)
        self.textfield_size = (300, 30)
        self.textfield_posz = 20
        self.submit_button_size = (100, 26)
        self.submit_button_posz = 190

        self.time_wait_before_steam_starts = 20
        self.time_login_inited = time.time()

        self.CORRECT = "dev"  # password
        self.INCORRECT = False

        self.link = "https://google.de"
        self.clicked = False
        self.Delaytime = time.time()
        self.Caretshow = True
        self.pressable_buttons = ("a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z,1,2,3,4,5,6,7,8,9,0,!,§,$,%,&,&,/,(,),=")
        self.pressable_buttons_list = self.pressable_buttons.split(",")

        self.textstop = False
        self.text = ""

        self.drawloginscreen = True
        self.loadingstate = 0
        self.request_time = time.time()
        self.correct_pass = False

        self.account_name = GetActiveAccount()
        self.license_is_valid = CheckIfUserLicenseIsValid(Generator(self.account_name))

        self.correct_acc = CheckIfUserExists(Generator(self.account_name))
        if self.correct_acc:
            self.correct_pass = CheckIfPasswordIsCorrect(Generator(self.account_name), Generator(self.text.upper()))

        license_path = ""
        license_path = license_path + os.path.dirname(os.path.abspath(__file__))
        # reformat
        license_path_list = license_path.split("""\\""")
        license_path_list.remove("Modules")
        license_path = ""
        for element in license_path_list:
            license_path = license_path + str(element) + "\\"

        self.count_web_helpers = len(GetWebHelpersList())
        self.loadingscreen = Loading()
        self.loading = False
        self.Loaded = False

    def Update(self, screenres, screen, is_loading):

        if is_loading:
            self.loading = True
            self.Loaded = True
        else:
            self.loading = False
            if self.Loaded == True:
                self.drawloginscreen = False

        if is_loading and self.time_login_inited + self.time_wait_before_steam_starts < time.time() and self.count_web_helpers < 8:
            self.loading = True
            self.count_web_helpers = len(GetWebHelpersList())
            self.time_login_inited = time.time()

        if not self.license_is_valid:
            self.correct_acc = False

        if self.correct_acc == True:
            if self.drawloginscreen == True:
                if self.loading == False:
                    self.account_name = GetActiveAccount()

                pygame.draw.rect(screen, Colors.Background, (0, 0, self.res[0], self.res[1]))
                scaledLogo = pygame.transform.scale(self.FLogo, (40, 60))
                screen.blit(scaledLogo, (self.res[0] / 2 - scaledLogo.get_width() / 2, 10))

                pygame.draw.rect(screen, Colors.TextColor, (self.res[0] / 2 - self.textfield_size[0] / 2,self.res[1] / 2 - self.textfield_size[1] / 2 + self.textfield_posz, self.textfield_size[0],self.textfield_size[1]))
                pygame.draw.rect(screen, Colors.Background, (2 + self.res[0] / 2 - self.textfield_size[0] / 2,2 + self.res[1] / 2 - self.textfield_size[1] / 2 + self.textfield_posz,-4 + self.textfield_size[0], -4 + self.textfield_size[1]))

                mousepos = pygame.mouse.get_pos()

                if pygame.mouse.get_pressed()[0] == True and self.Delaytime < time.time():
                    if mousepos[0] > self.res[0] / 2 - self.textfield_size[0] / 2 and mousepos[0] < self.res[0] / 2 - self.textfield_size[0] / 2 + self.textfield_size[0]:
                        if mousepos[1] > self.res[1] / 2 - self.textfield_size[1] / 2 + self.textfield_posz and mousepos[1] < self.res[1] / 2 - self.textfield_size[1] / 2 + self.textfield_size[1] + self.textfield_posz:
                            self.clicked = True
                            self.Delaytime = time.time() + 0.5
                        else:
                            self.clicked = False
                            self.Delaytime = time.time() + 0.5

                if self.clicked == True and not self.loading:
                    if self.Delaytime + 0.5 < time.time():
                        self.Delaytime = time.time()
                        self.Caretshow = not self.Caretshow

                if self.clicked == True and self.loading == False:
                    keyboard_hotkey_name = keyboard.get_hotkey_name()

                    if keyboard_hotkey_name != "" and self.textstop == False and keyboard_hotkey_name != "backspace":
                        self.textstop = True

                        for letter in self.pressable_buttons_list:
                            if letter == keyboard.get_hotkey_name():
                                self.text += keyboard.get_hotkey_name()

                    if keyboard_hotkey_name == "backspace":
                        if self.textstop == False:
                            self.text = self.text[:-1]
                            self.textstop = True

                    if keyboard_hotkey_name == "":
                        self.textstop = False

                TextFont = Colors.FontBig.render(str(self.text.upper()), True, Colors.TextColor)
                screen.blit(TextFont, (self.res[0] / 2 - self.textfield_size[0] / 2 + 2,self.res[1] / 2 - self.textfield_size[1] / 2 + 3 + self.textfield_posz))

                if self.Caretshow and self.clicked == True:
                    pygame.draw.rect(screen, Colors.TextColor, (self.res[0] / 2 - self.textfield_size[0] / 2 + 5 + TextFont.get_rect()[2],self.res[1] / 2 - self.textfield_size[1] / 2 + 3 + self.textfield_posz, 2, 24))

                SubmitFont = Colors.FontBig.render("Submit", True, Colors.TextColor)
                pygame.draw.rect(screen, Colors.TextColor, (self.res[0] / 2 - self.submit_button_size[0] / 2,self.submit_button_posz - self.submit_button_size[1] / 2, self.submit_button_size[0],self.submit_button_size[1]))
                pygame.draw.rect(screen, Colors.Background, (2 + self.res[0] / 2 - self.submit_button_size[0] / 2,2 + self.submit_button_posz - self.submit_button_size[1] / 2, -4 + self.submit_button_size[0],-4 + self.submit_button_size[1]))
                screen.blit(SubmitFont, (self.res[0] / 2 - SubmitFont.get_size()[0] / 2, self.submit_button_posz - SubmitFont.get_size()[1] / 2))

                steamname = Colors.FontBig.render(self.account_name, True, Colors.TextColor)
                screen.blit(steamname, (self.res[0] / 2 - steamname.get_size()[0] / 2, self.submit_button_posz - steamname.get_size()[1] / 2 - 100))

                if mousepos[0] > self.res[0] / 2 - self.submit_button_size[0] / 2 and mousepos[0] < self.res[0] / 2 + self.submit_button_size[0] / 2:
                    if mousepos[1] > self.submit_button_posz - self.submit_button_size[1] / 2 and mousepos[1] < self.submit_button_posz + self.submit_button_size[1] / 2:
                        if pygame.mouse.get_pressed()[0] == True and not self.loading:
                            self.loading = True

                            if self.request_time + 0.01 < time.time():

                                self.correct_acc_local = CheckValid()

                                self.correct_acc = CheckIfUserExists(Generator(self.account_name))
                                if self.correct_acc and self.correct_acc_local:
                                    self.correct_pass = CheckIfPasswordIsCorrect(Generator(self.account_name), Generator(self.text.upper()))
                                    self.license_is_valid = CheckIfUserLicenseIsValid(Generator(self.account_name))

                            self.request_time = time.time()

                            if self.correct_pass and self.correct_acc and self.correct_acc_local and self.license_is_valid:
                                self.state = True

                            else:
                                self.loading = False
                                self.INCORRECT = True
                                self.IncorrectDelay = time.time()

                if self.INCORRECT == True and self.correct_acc:
                    if self.IncorrectDelay + 1 < time.time():
                        self.INCORRECT = False
                    if self.correct_acc_local == False:
                        # startcsgo.Launcher(True, False)
                        errorfont = Colors.FontBig.render("Invalid Account", True, (255, 100, 100))
                        screen.blit(errorfont, (self.res[0] / 2 - errorfont.get_size()[0] / 2,self.submit_button_posz - errorfont.get_size()[1] / 2 - 30))

                    else:
                        errorfont = Colors.FontBig.render("Incorrect Password", True, (255, 100, 100))
                        screen.blit(errorfont, (self.res[0] / 2 - errorfont.get_size()[0] / 2, self.submit_button_posz - errorfont.get_size()[1] / 2 - 30))

            self.loadingscreen.Update(screen, self.loading)
        else:
            self.loading = False
            pygame.draw.rect(screen, Colors.Background, (0, 0, self.res[0], self.res[1]))
            scaledLogo = pygame.transform.scale(self.FLogo, (40, 60))
            screen.blit(scaledLogo, (self.res[0] / 2 - scaledLogo.get_width() / 2, 10))
            steamname = Colors.FontBig.render(self.account_name, True, Colors.TextColor)
            screen.blit(steamname, (self.res[0] / 2 - steamname.get_size()[0] / 2, self.submit_button_posz - steamname.get_size()[1] / 2 - 100))
            font = Colors.FontBig.render("Buy a Subscription!", True, (100, 255, 100))
            screen.blit(font, (self.res[0] / 2 - font.get_size()[0] / 2, self.submit_button_posz - font.get_size()[1] / 2 - 60))

            mousepos = pygame.mouse.get_pos()

            link = Colors.FontBig.render(str(self.link), True, (42, 129, 233))

            if mousepos[0] > self.res[0] / 2 - link.get_size()[0] / 2 and mousepos[0] < self.res[0] / 2 + link.get_size()[0] / 2:
                if mousepos[1] > self.submit_button_posz - link.get_size()[1] / 2 - 30 and mousepos[1] < self.submit_button_posz + link.get_size()[1] / 2 - 30:
                    if pygame.mouse.get_pressed()[0] and self.Delaytime + 0.3 < time.time():
                        self.Delaytime = time.time()
                        callcommand = "explorer " + str(self.link)
                        subprocess.call(callcommand)

            screen.blit(link, (self.res[0] / 2 - link.get_size()[0] / 2, self.submit_button_posz - link.get_size()[1] / 2 - 30))

        return self.state