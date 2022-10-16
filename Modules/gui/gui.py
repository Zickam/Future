import keyboard
import os
import math
import psutil
import pygame.display
import time
import win32api
from Modules import Startcsgo
from Modules.Startcsgo import RestartSteam
import win32con
import win32gui
import datetime
import subprocess
from pynput.mouse import Controller
from hashlib import sha256
from Modules.LicenseChecker import GetActiveAccount, CheckValid, GetWebHelpersList
from Modules.Generator import Generator
from ServerDB.Client import CheckIfUserExists, CheckIfPasswordIsCorrect, CheckIfUserLicenseIsValid, FetchUserTimeLicenseExpire
import json

class Buttons:
    def __init__(self):

        visualspng = pygame.image.load("Data/Images/Visuals.png")
        aimbotpng = pygame.image.load("Data/Images/Aimbot.png")
        miscpng = pygame.image.load("Data/Images/Misc.png")
        scriptspng = pygame.image.load("Data/Images/Scripts.png")
        configpng = pygame.image.load("Data/Images/Config.png")

        # window
        button_size = (80, 25)
        firstlvlbutton_size = (80, 50)
        slider_size = (80, 10)
        slider_offsets = (0, 13)
        checkbox_size = (18, 18)
        checkbox_offset = (0, 3)

        self.buttons_grid = {
            "Visuals": {"type": "FirstLevelButton", "picture": visualspng, "pos": (0, 0),
                        "size": firstlvlbutton_size, "dependencies": {
                    "GlowESP": {"type": "button", "pos": (0, 0), "size": button_size, "dependencies": {
                        "EnemyR": {"type": "button", "pos": (0, 0), "size": button_size},
                        "EnemyG": {"type": "button", "pos": (0, 0), "size": button_size},
                        "EnemyB": {"type": "button", "pos": (0, 0), "size": button_size},
                        "TeamR": {"type": "button", "pos": (0, 0), "size": button_size},
                        "TeamG": {"type": "button", "pos": (0, 0), "size": button_size},
                        "TeamB": {"type": "button", "pos": (0, 0), "size": button_size},
                    }},
                    "Sky": {"type": "button", "pos": (0, 0), "size": button_size, "dependencies": {
                        "skySelector": {"type": "selector", "pos": (0, 20), "size": button_size,
                                        "array": ["cs_tibet", "embassy", "italy", "jungle", "nukeblank", "office",
                                                  "sky_cs15_daylight01_hdr", "sky_cs15_daylight02_hdr",
                                                  "sky_cs15_daylight03_hdr", "sky_cs15_daylight04_hdr",
                                                  "sky_csgo_cloudy01", "sky_csgo_night02", "sky_csgo_night02b",
                                                  "sky_day02_05", "sky_dust", "sky_lunacy", "sky_venice", "vertigo",
                                                  "vertigoblue_hdr", "vietnam", ]},
                    }},
                    "Radar": {"type": "button", "pos": (0, 0), "size": button_size},
                    "Chams": {"type": "button", "pos": (0, 0), "size": button_size, "dependencies": {
                        "Glow": {"type": "button", "pos": (0, 0), "size": button_size},
                        "Color": {"type": "colorPicker", "pos": (0, 0), "size": (100, 100)},
                        "Color1": {"type": "colorPicker", "pos": (110, -30), "size": (100, 100)}
                    }},
                    "NoFlash": {"type": "button", "pos": (0, 0), "size": button_size},
                    "FOV": {"type": "button", "pos": (0, 0), "size": button_size, "dependencies": {
                        "Hands": {"type": "slider", "pos": slider_offsets, "size": slider_size, "start": 70,
                                  "end": 170},
                        "Fov": {"type": "slider", "pos": slider_offsets, "size": slider_size, "start": 70,
                                "end": 170},
                        "Reset FOV": {"type": "button", "pos": (0, 0), "size": button_size},
                    }},
                    "3D Person": {"type": "button", "pos": (0, 0), "size": button_size},
                    "Grenade Prediction": {"type": "button", "pos": (0, 0), "size": button_size},
                    "Night Mode": {"type": "button", "pos": (0, 0), "size": button_size, "dependencies": {
                        "Brightness": {"type": "slider", "pos": slider_offsets, "size": slider_size, "start": 1,
                                       "end": 200},
                    }},
                    "No Smoke": {"type": "button", "pos": (0, 0), "size": button_size},
                    "ShowFPS": {"type": "button", "pos": (0, 0), "size": button_size},

                }},
            "Combat": {"type": "FirstLevelButton", "picture": aimbotpng, "pos": (0, 0), "size": firstlvlbutton_size,
                       "dependencies": {
                           "AimBot": {"type": "button", "pos": (0, 0), "size": button_size, "dependencies": {
                               "Enemies": {"type": "button", "pos": (0, 0), "size": button_size},
                               "Team": {"type": "button", "pos": (0, 0), "size": button_size},
                               "Markplayer": {"type": "button", "pos": (0, 0), "size": button_size},
                               "AimFOV": {"type": "slider", "pos": (0, 25), "size": slider_size, "start": 1,
                                          "end": 90},
                               "Smooth": {"type": "slider", "pos": (0, 25), "size": slider_size, "start": 0,
                                          "end": 100},
                               "Overaim": {"type": "slider", "pos": (0, 25), "size": slider_size, "start": 0,
                                           "end": 20},
                               "Selector": {"type": "selector", "pos": (0, 20), "size": button_size,
                                            "array": ["Head", "Chest", "Stomach"]},
                               "Selector1": {"type": "selector", "pos": (90, -10), "size": button_size,
                                             "array": ["Crosshair", "Distance"]},
                               "Multipoint": {"type": "button", "pos": (90, -240), "size": button_size},
                           }},
                           "TriggerBot": {"type": "button", "pos": (0, 0), "size": button_size, "dependencies": {
                               "Highacc": {"type": "button", "pos": (0, 0), "size": button_size},
                               "MaxSpeed": {"type": "slider", "pos": (0, 15), "size": slider_size, "start": 0,
                                            "end": 300},

                               "OnPress": {"type": "button", "pos": (0, 8), "size": button_size},
                               "Enemies": {"type": "button", "pos": (0, 8), "size": button_size},
                               "Team": {"type": "button", "pos": (0, 8), "size": button_size},
                               "Humanizer": {"type": "slider", "pos": (0, 23), "size": slider_size, "start": 0,
                                             "end": 100},
                               # PercentChance
                               "Delay": {"type": "slider", "pos": (0, 20), "size": slider_size, "start": 0,
                                         "end": 1000},
                               # milliseconds
                           }},
                           "Recoil": {"type": "button", "pos": (0, 0), "size": button_size},
                           "RapidFire": {"type": "button", "pos": (0, 0), "size": button_size},
                           "FastPeek": {"type": "button", "pos": (0, 0), "size": button_size}
                       }},
            "Misc": {"type": "FirstLevelButton", "picture": miscpng, "pos": (0, 0), "size": firstlvlbutton_size,
                     "dependencies": {
                         "SkinChange": {"type": "button", "pos": (0, 0), "size": button_size, "dependencies": {
                             "Skin name": {"type": "searchbox", "pos": (0, 0), "size": button_size,
                                           "array": self.getskins()},
                             "Weapon": {"type": "searchbox", "pos": (110, -30), "size": button_size,
                                        "array": self.getweapons()[1]},
                             "Update": {"type": "button", "pos": (0, -110), "size": button_size},
                         }},

                         "ToxicChat": {"type": "button", "pos": (0, 0), "size": button_size, "dependencies": {
                             "KillCounter": {"type": "button", "pos": (0, 0), "size": button_size},
                             "AfterKill": {"type": "button", "pos": (0, 0), "size": button_size},
                             "Spam": {"type": "button", "pos": (0, 0), "size": button_size},

                         }},

                         "Sound": {"type": "button", "pos": (0, 0), "size": button_size, "dependencies": {
                             "OnHit": {"type": "button", "pos": (0, 0), "size": button_size},
                             "OnKill": {"type": "button", "pos": (0, 0), "size": button_size},
                             "SelectSound": {"type": "selector", "pos": (0, 0), "size": button_size,
                                             "array": ["Neverlose", "Bell", "Cod", "Fatality"]},
                         }},
                         "FakeLag": {"type": "button", "pos": (0, 0), "size": button_size, "dependencies": {
                             "DelayStart": {"type": "slider", "pos": (0, 10), "size": slider_size, "start": 10,
                                            "end": 100},
                             # milliseconds
                             "DelayBetween": {"type": "slider", "pos": (0, 17), "size": slider_size, "start": 10,
                                              "end": 300},
                             # milliseconds
                         }},
                         "Teleport": {"type": "button", "pos": (0, 0), "size": button_size, "dependencies": {
                             "DelayStart": {"type": "slider", "pos": (0, 10), "size": slider_size, "start": 0,
                                            "end": 5000},
                             # milliseconds
                             "DelayBetween": {"type": "slider", "pos": (0, 17), "size": slider_size, "start": 0,
                                              "end": 800},
                             # milliseconds
                         }},
                         "BunnyHop": {"type": "button", "pos": (0, 0), "size": button_size, "dependencies": {
                             "AutoStrafe": {"type": "button", "pos": (0, 0), "size": button_size},
                         }},
                         "Slowwalk": {"type": "button", "pos": (0, 0), "size": button_size, "dependencies": {
                             "Speed": {"type": "slider", "pos": slider_offsets, "size": slider_size, "start": 0,
                                       "end": 200},
                         }},
                         "ForceCrosshair": {"type": "checkbox", "pos": checkbox_offset, "size": checkbox_size},
                         "ClanTag": {"type": "checkbox", "pos": checkbox_offset, "size": checkbox_size},
                         "DevCommands": {"type": "button", "pos": (0, 0), "size": button_size}
                     }},
            "Scripts": {"type": "FirstLevelButton", "picture": scriptspng, "pos": (0, 0),
                        "size": firstlvlbutton_size, "dependencies": {
                    "Load": {"type": "scriptmanager", "pos": (0, 0), "size": (290, 335)},

                }},
            "Config": {"type": "FirstLevelButton", "picture": configpng, "pos": (0, 0), "size": firstlvlbutton_size,
                       "dependencies": {
                           "Load": {"type": "button", "pos": (0, 0), "size": button_size},
                           "Save": {"type": "button", "pos": (0, 0), "size": button_size},
                           "ConfigSelector": {"type": "selector", "pos": (0, 0), "size": button_size,
                                              "array": ["Custom", "Rage", "Semi", "Legit", "Dev"]},
                       }},
            "Settings": {"type": "FirstLevelButton", "picture": miscpng, "pos": (0, 0), "size": firstlvlbutton_size,
                         "dependencies": {
                             "Transparency": {"type": "slider", "pos": slider_offsets, "size": slider_size,
                                              "start": 50, "end": 255},
                             "Change Transparency": {"type": "checkbox", "pos": checkbox_offset,
                                                     "size": checkbox_size},
                             "Highlight": {"type": "colorPicker", "pos": (0, 0), "size": (100, 100)},
                             "Colorstyle": {"type": "colorPicker", "pos": (110, -30), "size": (100, 100)},
                         }},
            # "Reset": {"pos": (0, 0), "size": button_size}
            "End": {"type": "end"}
        }

        def iterateThroughButtonDependencies(object_name, object_dependencies, start_pos_dependencies):

            objects = {}
            for object_name, object_props in object_dependencies.items():
                if object_props["type"] == "button":
                    pos_x = object_props["pos"][0] + start_pos_dependencies[0]
                    pos_y = object_props["pos"][1] + start_pos_dependencies[1]
                    _object = Button((pos_x, pos_y), object_props["size"], object_name)
                    start_pos_dependencies[1] += gap_y

                elif object_props["type"] == "selector":
                    pos_x = object_props["pos"][0] + start_pos_dependencies[0]
                    pos_y = object_props["pos"][1] + start_pos_dependencies[1]
                    _object = Selector((pos_x, pos_y), object_props["size"], object_name, object_props["array"])
                    start_pos_dependencies[1] += gap_y

                elif object_props["type"] == "slider":
                    pos_x = object_props["pos"][0] + start_pos_dependencies[0]
                    pos_y = object_props["pos"][1] + start_pos_dependencies[1]
                    _object = Slider((pos_x, pos_y), object_props["size"], object_name, object_props["start"],
                                         object_props["end"])
                    start_pos_dependencies[1] += gap_y


                elif object_props["type"] == "checkbox":
                    pos_x = object_props["pos"][0] + start_pos_dependencies[0]
                    pos_y = object_props["pos"][1] + start_pos_dependencies[1]
                    _object = Checkbox((pos_x, pos_y), object_props["size"], object_name, (255, 255, 255))
                    start_pos_dependencies[1] += gap_y


                elif object_props["type"] == "colorPicker":
                    pos_x = object_props["pos"][0] + start_pos_dependencies[0]
                    pos_y = object_props["pos"][1] + start_pos_dependencies[1]
                    _object = ColorPicker((pos_x, pos_y), object_props["size"], object_name)
                    start_pos_dependencies[1] += gap_y

                elif object_props["type"] == "searchbox":
                    pos_x = object_props["pos"][0] + start_pos_dependencies[0]
                    pos_y = object_props["pos"][1] + start_pos_dependencies[1]
                    _object = Searchbox((pos_x, pos_y), object_props["size"], object_name,
                                            object_props["array"])
                    start_pos_dependencies[1] += gap_y

                elif object_props["type"] == "scriptmanager":
                    pos_x = object_props["pos"][0] + start_pos_dependencies[0]
                    pos_y = object_props["pos"][1] + start_pos_dependencies[1]
                    _object = ScriptManager((pos_x, pos_y), object_props["size"])
                    start_pos_dependencies[1] += gap_y

                elif object_props["type"] == "end":
                    continue

                if "dependencies" in object_props:
                    _start_pos_for_dependencies = [start_pos_dependencies[0] + gap_x,
                                                   start_pos_dependencies[1] - gap_y]
                    dependencies = iterateThroughButtonDependencies(object_name, object_props["dependencies"],
                                                                    _start_pos_for_dependencies)

                else:
                    dependencies = None
                objects[object_name] = [_object, dependencies]
            start_pos_dependencies[0] += gap_x

            return objects

        self.buttons = {}
        pos = [10, 60]
        gap_y = button_size[1] + 5
        gap_x = button_size[0] + 10

        gap_y_first_level_btn = firstlvlbutton_size[1] + 5

        start_pos = [pos[0], pos[1]]
        start_pos_default = [pos[0], pos[1]]

        for object_name, object_props in self.buttons_grid.items():
            if object_props["type"] == "FirstLevelButton":
                pos_x = object_props["pos"][0] + start_pos[0]
                pos_y = object_props["pos"][1] + start_pos[1]
                _object = FirstLevelButton(object_props["picture"], (pos_x, pos_y), object_props["size"],
                                               object_name)

            if object_props["type"] == "end":
                break

            if "dependencies" in object_props:
                start_pos_for_dependencies = [pos_x + gap_x, start_pos_default[1]]
                dependencies = iterateThroughButtonDependencies(object_name, object_props["dependencies"],
                                                                start_pos_for_dependencies)
            else:
                dependencies = None

            self.buttons[object_name] = [_object, dependencies]
            start_pos[1] += gap_y_first_level_btn


    def getskins(self):
        skinlist = []
        with open("Data/Structs/skins.json") as file:
            options = json.load(file)
            for element in options:
                skinlist.append(str(element))
        return skinlist

    def getweapons(self):
        from pathlib import Path

        weapons_specs_file = os.path.join(Path(__file__).parents[2], "Data\\Structs\\WeaponSpecs.json")

        idlist = []
        namelist = []
        dmglist = []
        rangelist = []
        armorpen = []
        with open(weapons_specs_file, "r") as file:
            options = json.load(file)
            for element in options:
                idlist.append(element)
            for element in range(0, len(idlist)):
                namelist.append(options[idlist[element]]["name"])
                dmglist.append(options[idlist[element]]["damage"])
                rangelist.append(options[idlist[element]]["accrange"])
                armorpen.append(options[idlist[element]]["armorpen"])
        return idlist, namelist, dmglist, rangelist, armorpen

default_font_size = 15
default_font = "Microsoft Sans Serif"
ChangeAlpha = False

class Overlay:
    def __init__(self, rect: pygame.Rect):
        print("[overlay V0.5] > Initializing")
        pygame.init()
        os.environ["SDL_VIDEO_WINDOW_POS"] = str(pygame.display.Info().current_w) + "," + str(pygame.display.Info().current_h)

        # initialize window and make it transparent
        self.screen = pygame.display.set_mode((0, 0), pygame.NOFRAME)
        self.overlay_hwnd = pygame.display.get_wm_info()["window"]

        # get resolution / position
        self.hwnd_rect = rect

        # move window and make it visible
        win32gui.MoveWindow(self.overlay_hwnd, self.hwnd_rect[0], self.hwnd_rect[1], self.hwnd_rect[2], self.hwnd_rect[3], True)
        win32gui.ShowWindow(self.overlay_hwnd, win32con.SW_SHOW)

        # for fps
        self.framecap = 1000
        self.fps = 1
        self.clock = pygame.time.Clock()

        self.show_value = 254
        self.increaser = 1


    def overlaymode(self):
        win32gui.SetWindowLong(self.overlay_hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(self.overlay_hwnd, win32con.GWL_EXSTYLE) | win32con.WS_POPUP | win32con.WS_EX_LAYERED)
        win32gui.SetWindowLong(self.overlay_hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(self.overlay_hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_TRANSPARENT | win32con.WS_EX_LAYERED)
        win32gui.SetLayeredWindowAttributes(self.overlay_hwnd, win32api.RGB(0, 0, 0), 255, win32con.LWA_COLORKEY | win32con.LWA_ALPHA)
        win32gui.BringWindowToTop(self.overlay_hwnd)

    def windowmode(self):
        win32gui.SetWindowLong(self.overlay_hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(self.overlay_hwnd, win32con.GWL_EXSTYLE) | win32con.WS_POPUP | win32con.WS_EX_LAYERED)
        win32gui.SetWindowLong(self.overlay_hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(self.overlay_hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_TRANSPARENT | win32con.WS_EX_LAYERED)
        win32gui.SetLayeredWindowAttributes(self.overlay_hwnd, win32api.RGB(0, 0, 0), 255, win32con.LWA_COLORKEY | win32con.LWA_ALPHA)
        win32gui.BringWindowToTop(self.overlay_hwnd)

    def clamp(self, num, min_value, max_value):
        num = max(min(num, max_value), min_value)
        return num

    def show(self):
        if self.show_value >= 254:
            self.increaser = -250 * (1 / self.fps)
        if self.show_value <= 1:
            self.increaser = 250 * (1 / self.fps)
        self.show_value += self.increaser
        pygame.draw.rect(self.screen, (0, self.clamp(self.show_value, 0, 255), 0), (0, 0, self.hwnd_rect[2], self.hwnd_rect[3]), 4)

    def set_cap(self, framecap: int):
        self.framecap = framecap

    def update(self):
        self.clock.tick(self.framecap)
        self.fps = 1 + self.clock.get_fps()

        pygame.display.flip()
        return pygame.event.get()

    def display_fps(self):
        self.font = pygame.font.SysFont("Courier", 20, True, False)
        self.sprite = self.font.render(str(round(self.fps)), True, (255, 255, 0))
        pygame.draw.rect(self.screen, (40, 40, 40), (self.hwnd_rect[2] - self.sprite.get_width() - 5, 5, self.sprite.get_width(), 20))
        self.screen.blit(self.sprite, (self.hwnd_rect[2] - self.sprite.get_width() - 5, 5))

class color_changer:
    def __init__(self):
        self.SmoothedR = 255
        self.SmoothedG = 255
        self.SmoothedB = 255

    def color_surface(self, surface, color, fps):
        global SmoothedR, SmoothedG, SmoothedB
        arr = pygame.surfarray.pixels3d(surface)
        if fps == 0:
            self.SmoothedR -= (self.SmoothedR - color[0]) / 10
            self.SmoothedG -= (self.SmoothedG - color[1]) / 10
            self.SmoothedB -= (self.SmoothedB - color[2]) / 10
        else:
            self.SmoothedR -= (self.SmoothedR - color[0]) / (1 / fps) * 10
            self.SmoothedG -= (self.SmoothedG - color[1]) / (1 / fps) * 10
            self.SmoothedB -= (self.SmoothedB - color[2]) / (1 / fps) * 10
        for x in range(0, len(arr)):
            for y in range(0, len(arr[x])):
                if arr[x][y][0] != 0 and arr[x][y][1] != 0 and arr[x][y][2] != 0:
                    arr[x][y][0] = clamp(arr[x][y][0] - 255 + self.SmoothedR, 0, 255)
                    arr[x][y][1] = clamp(arr[x][y][1] - 255 + self.SmoothedG, 0, 255)
                    arr[x][y][2] = clamp(arr[x][y][2] - 255 + self.SmoothedB, 0, 255)

class Colors():
    Background = (20, 20, 20, 150)      # background
    LightBackground = (50, 50, 50)
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
    rect = win32gui.GetWindowRect(win32gui.GetDesktopWindow())
    print(f"[OVERLAY INITFUNCTION], {rect, resolution}")
    screen = Overlay(pygame.Rect(rect[2] / 2 - resolution[0] / 2, rect[3] / 2 - resolution[1] / 2, resolution[0], resolution[1]))
    return screen

class Window():
    def __init__(self, resolution, position, overlay):
        # window
        pygame.display.set_caption("Future")
        self.resolution = resolution
        self.ActiveModuleRes = resolution
        self.position = position
        self.CustomMouse = Controller()
        self.Foreground = True
        self.logo = pygame.image.load("Data\Images\Icon.png")
        self.starttime = time.time()

        self.overlay = overlay
        self.screen = overlay.screen
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

        self.pygameevent = None

        self.colorchanger = color_changer()


    def Update(self, ActiveModules, Framedelta, is_login_screen):
        Window = win32gui.FindWindow(None, "Future")
        WindowRect = win32gui.GetWindowRect(Window)

        Mousepos = pygame.mouse.get_pos()

        self.pygameevent = pygame.event.get()

        self.screen.fill(Colors.Background)
        # main window
        if self.Foreground == True:

            separate_line = pygame.draw.line(self.screen, (220, 220, 220), (70, 0), (70, 500), 2)

            # logo color change
            if self.LogoUpdate == True:
                self.coloredSurface = self.origSurface.copy()
                self.colorchanger.color_surface(self.coloredSurface, Colors.ColorStyle, self.clock.get_fps())

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


            for event in self.pygameevent:
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

            self.overlay = Overlay(pygame.Rect(0, 0, 1920, 1080))
            pygame.draw.rect(self.screen, (255, 255, 255), (0, 0, 10000, 10000))

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

class FirstLevelButton():
    def __init__(self, picture, position, size, name):
        self.pos = position
        self.size = size
        self.name = name
        self.Tab = False
        self.DelayTime = time.time()
        self.picture_update = False

        if picture.get_width() > 30 and picture.get_height() > 30:
            self.picture = pygame.transform.scale(picture, (50, 50))
        else:
            self.picture = picture

        self.coloredSurface = self.picture
        self.colorchanger = color_changer()

    def Update(self, screen, mousepos, framedelta):

        screen.blit(self.picture, self.pos)

        if mousepos[0] > self.pos[0] and mousepos[0] < self.pos[0] + self.size[0] and mousepos[1] > self.pos[1] and mousepos[1] < self.pos[1] + self.size[1]:
            if pygame.mouse.get_pressed()[2] and self.DelayTime + 0.15 <= time.time():
                self.Tab = not self.Tab
                self.DelayTime = time.time()

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
    def __init__(self, overlay):
        self.screen = overlay.screen
        self.i = 0
        self.speed = 0
        self.state = 1
        self.F = pygame.image.load("Data/Images/Future.png")
        self.scrsize = overlay.hwnd_rect[2], overlay.hwnd_rect[3]

        self.width = 165
        self.height = 70
        self.heightoffset = 35

        self.futuresurface = pygame.Surface((self.F.get_size()))

        self.futuresurface.fill(Colors.Background)

        self.futuresurface.blit(self.F, (0, 0))

        self.dark = (50, 50, 50)
        self.bright = (120, 120, 120)

    def Update(self):

        if self.state != 7:
            pygame.draw.rect(self.screen, Colors.Background, (0, 0, self.scrsize[0], self.scrsize[1]))

        if self.state == 1:
            self.speed += 3

        if self.state > 0 and self.state < 3:
            self.i = self.i + clamp(self.speed, -8, 8)

        if self.state == 3:
            self.i = self.i + clamp(self.speed, -3, 3)

        if self.state == 6:
            self.i = self.i + clamp(self.speed, -8, 8)

        if self.speed >= 8 and self.state == 1:
            self.state = 2

        # draw bottom lines
        pygame.draw.rect(self.screen, self.dark, (self.scrsize[0] / 2, self.scrsize[1] / 2 + self.heightoffset, clamp(self.i, 0, self.width), 1))
        pygame.draw.rect(self.screen, self.dark, (self.scrsize[0] / 2 - clamp(self.i, 0, self.width) + 1, self.scrsize[1] / 2 + self.heightoffset,
        clamp(self.i, 0, self.width), 1))

        # left right lines
        if self.i >= self.width:
            pygame.draw.rect(self.screen, self.dark, (self.scrsize[0] / 2 + self.width,
                                                 self.heightoffset + self.scrsize[1] / 2 - clamp(
                                                     (self.i - self.width) - 2, 0, self.height), 1,
                                                 clamp((self.i - self.width), 0, self.height + 1)))
            pygame.draw.rect(self.screen, self.dark, (self.scrsize[0] / 2 - self.width,
                                                 self.heightoffset + self.scrsize[1] / 2 - clamp(
                                                     (self.i - self.width) - 2, 0, self.height), 1,
                                                 clamp((self.i - self.width), 0, self.height + 1)))

        # draw top lines
        if self.i >= self.width + self.height:
            pygame.draw.rect(self.screen, self.dark, (
            self.scrsize[0] / 2 - self.width, self.scrsize[1] / 2 + self.heightoffset - self.height,
            clamp(self.i - self.width - self.height, 0, self.width), 1))
            pygame.draw.rect(self.screen, self.dark, (
            self.scrsize[0] / 2 + self.width - clamp(self.i - self.width - self.height, 0, self.width),
            self.scrsize[1] / 2 + self.heightoffset - self.height,
            clamp(self.i - self.width - self.height, 0, self.width), 1))

        # make brighter
        if self.i >= self.width * 2 + self.height and self.state == 2 and self.state != 6:
            self.state = 3
        if self.i >= self.width * 2 + self.height:
            val = self.width * 2 + self.height
            # draw bottom lines
            pygame.draw.rect(self.screen, self.bright, (
            self.scrsize[0] / 2, self.scrsize[1] / 2 + self.heightoffset, clamp(self.i - val, 0, self.width), 1))
            pygame.draw.rect(self.screen, self.bright, (
            self.scrsize[0] / 2 - clamp(self.i - val, 0, self.width) + 1, self.scrsize[1] / 2 + self.heightoffset,
            clamp(self.i - val, 0, self.width), 1))

            # left right lines
            if self.i >= self.width:
                pygame.draw.rect(self.screen, self.bright, (self.scrsize[0] / 2 + self.width,
                                                       self.heightoffset + self.scrsize[1] / 2 - clamp(
                                                           (self.i - val - self.width) - 2, 0, self.height), 1,
                                                       clamp((self.i - val - self.width), 0, self.height + 1)))
                pygame.draw.rect(self.screen, self.bright, (self.scrsize[0] / 2 - self.width,
                                                       self.heightoffset + self.scrsize[1] / 2 - clamp(
                                                           (self.i - val - self.width) - 2, 0, self.height), 1,
                                                       clamp((self.i - val - self.width), 0, self.height + 1)))

            # draw top lines
            if self.i >= self.width + self.height:
                pygame.draw.rect(self.screen, self.bright, (
                self.scrsize[0] / 2 - self.width, self.scrsize[1] / 2 + self.heightoffset - self.height,
                clamp(self.i - val - self.width - self.height, 0, self.width), 1))
                pygame.draw.rect(self.screen, self.bright, (
                self.scrsize[0] / 2 + self.width - clamp(self.i - val - self.width - self.height, 0, self.width),
                self.scrsize[1] / 2 + self.heightoffset - self.height,
                clamp(self.i - val - self.width - self.height, 0, self.width), 1))

        if self.i >= (self.width * 2 + self.height) * 2 and self.state == 3:
            self.state = 4

        # make lines brighter
        if self.state == 4:
            if self.bright[0] < 255:
                self.bright = (clamp(self.bright[0] + 40, 0, 255), clamp(self.bright[0] + 40, 0, 255),
                               clamp(self.bright[0] + 40, 0, 255))
            else:
                self.state = 5

        # make lines darker
        if self.state == 5:
            if self.bright[0] > self.dark[0]:
                self.bright = (clamp(self.bright[0] - 20, 0, 255), clamp(self.bright[0] - 20, 0, 255), clamp(self.bright[0] - 20, 0, 255))
            else:
                self.state = 6
                self.i = self.width * 2 + self.height
                self.speed = -10

        # end
        if self.state == 6 and self.i < 0:
            self.state = 7

        # center logo
        self.futuresurface.set_alpha(clamp(self.i, 0, 255))
        surface = pygame.transform.scale(self.futuresurface, (self.F.get_size()[0] / (3.8 - clamp(self.i / 50, -100, 2)),self.F.get_size()[1] / (3.7 - clamp(self.i / 50, -100, 2))))
        self.screen.blit(surface, (self.scrsize[0] / 2 - surface.get_width() / 2, self.scrsize[1] / 2 - surface.get_height() / 2))

        return self.state

class Loading():
    def __init__(self, overlay):
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

        self.backgroundoverlay = pygame.Surface((1000, 1000))
        self.pos = (overlay.hwnd_rect[2] / 2, overlay.hwnd_rect[3] / 2)
        self.backgroundoverlay.set_alpha(self.alpha)
        self.backgroundoverlay.fill(self.backcolor)


    def Update(self, overlay, State):
        screen = overlay.screen

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

class LoginScreen:
    def __init__(self, serverisonline, overlay):

        self.res = (410, 220)
        self.serverisonline = serverisonline
        self.FLogo = pygame.image.load("Data/Images/Original.png")
        self.account_name = GetActiveAccount()

        if serverisonline == True:

            csgo_works = Startcsgo.csgoWorks()
            steam_works = Startcsgo.steamWorks()

            if not steam_works and not csgo_works:
                Startcsgo.StartSteam()
                while not Startcsgo.steamWorks():
                    time.sleep(0.1)

            elif steam_works and not csgo_works:
                Startcsgo.RestartSteam()
                while not Startcsgo.steamWorks():
                    time.sleep(0.1)

            self.state = False

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
            self.loadingscreen = Loading(overlay)
            self.loading = False
            self.Loaded = False

            self.expire_timestamp = int(FetchUserTimeLicenseExpire(Generator(self.account_name)))
            self.expire_date = str(datetime.datetime.fromtimestamp(self.expire_timestamp)).split(" ")

            self.enterpressed = False

            self.restarted_steam = False


    def Update(self, screenres, overlay, is_loading, keyevent):
        screen = overlay.screen
        if self.serverisonline == True:
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
                        for event in keyevent:
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_BACKSPACE:
                                    self.text = self.text[:-1]
                                elif event.key != pygame.K_BACKSPACE and event.key != pygame.K_RETURN:
                                    self.text += event.unicode

                                if event.key == pygame.K_RETURN:
                                    self.enterpressed = True

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

                    if datetime.datetime.now().timestamp() < self.expire_timestamp:
                        TextFont = Colors.FontBig.render(self.expire_date[0], True, (100, 200, 100))
                    else:
                        TextFont = Colors.FontBig.render(self.expire_date[0], True, (200, 100, 100))
                    screen.blit(TextFont, (screenres[0] - TextFont.get_size()[0] - 10, 10))

                    if mousepos[0] > self.res[0] / 2 - self.submit_button_size[0] / 2 and mousepos[0] < self.res[0] / 2 + self.submit_button_size[0] / 2 or self.enterpressed:
                        if mousepos[1] > self.submit_button_posz - self.submit_button_size[1] / 2 and mousepos[1] < self.submit_button_posz + self.submit_button_size[1] / 2 or self.enterpressed:
                            if pygame.mouse.get_pressed()[0] == True or self.enterpressed:
                                if not self.loading:
                                    self.loading = True

                                    if self.request_time + 0.01 < time.time():

                                        if Startcsgo.csgoAndSteamWorks():
                                            self.correct_acc_local = True

                                        else:
                                            self.correct_acc_local = CheckValid()

                                        self.correct_acc = CheckIfUserExists(Generator(self.account_name))
                                        if self.correct_acc and self.correct_acc_local:
                                            self.correct_pass = CheckIfPasswordIsCorrect(Generator(self.account_name), Generator(self.text.upper()))
                                            self.license_is_valid = CheckIfUserLicenseIsValid(Generator(self.account_name))

                                    self.request_time = time.time()

                                    if self.correct_pass and self.correct_acc and self.correct_acc_local and self.license_is_valid:
                                        self.state = True
                                        Startcsgo.Launcher(False, True, False, True)

                                    else:
                                        self.loading = False
                                        self.INCORRECT = True
                                        self.IncorrectDelay = time.time()
                                        self.enterpressed = False

                    if self.INCORRECT == True and self.correct_acc:
                        if self.restarted_steam == False:
                            Startcsgo.Launcher(False, True, False, False)

                            self.restarted_steam = True
                        if self.IncorrectDelay + 1 < time.time():
                            self.INCORRECT = False
                        if self.correct_acc_local == False:
                            errorfont = Colors.FontBig.render("Invalid Account", True, (255, 100, 100))
                            screen.blit(errorfont, (self.res[0] / 2 - errorfont.get_size()[0] / 2, self.submit_button_posz - errorfont.get_size()[1] / 2 - 30))
                        else:
                            errorfont = Colors.FontBig.render("Incorrect Password", True, (255, 100, 100))
                            screen.blit(errorfont, (self.res[0] / 2 - errorfont.get_size()[0] / 2, self.submit_button_posz - errorfont.get_size()[1] / 2 - 30))

                self.loadingscreen.Update(overlay, self.loading)
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
        else:
            pygame.draw.rect(screen, Colors.Background, (0, 0, self.res[0], self.res[1]))

            sprite = Colors.FontBig.render("Database not available", True, (255, 100, 100))
            screen.blit(sprite, (self.res[0] / 2 - sprite.get_size()[0] / 2, self.res[1] - sprite.get_size()[1] / 2 - 90))

            scaledLogo = pygame.transform.scale(self.FLogo, (40, 60))
            screen.blit(scaledLogo, (self.res[0] / 2 - scaledLogo.get_width() / 2, 10))

            steamname = Colors.FontBig.render(self.account_name, True, Colors.TextColor)
            screen.blit(steamname, (self.res[0] / 2 - steamname.get_size()[0] / 2, self.res[1] - steamname.get_size()[1] / 2 - 130))

class ScriptManager:
    def __init__(self, pos, size):
        # get the run file and path of all "scripts"
        self.scriptpath = os.getcwd() + "\\scripts\\"
        self.file_list = os.listdir(self.scriptpath)
        self.win_size = (410, 380)
        self.pos = pos
        self.size = size

        self.clicked_mouse = False
        self.calc_time = 0
        self.delaytime = time.time()

        self.loaded_code = []
        self.loaded_script_names = []

        self.error = ""
        self.errortime = time.time()
        self.errorfile = ""
        self.errorscroll = 0
        self.errorsurface = pygame.Surface((self.size[0], 20))
        self.errorsurface.fill((Colors.Background))

        self.unallowedlist = ["unallowedlist", "with open", "while", "os.", "sys.", "Manager", "Colors.", "exec", "compile", "from", "import", "quit()", "exit()", "self.scriptpath", "self.file_list", "self.win_size", "self.pos", "self.size"
                             "self.clicked_mouse", "self.calc_time", "self.delaytime", "self.error", "self.errortime", "self.errorscroll", "self.errorsurface", "self.refreshpng"]

        self.refreshpng = pygame.image.load("Data/Images/Refresh.png")



    def Update(self, screen, mousepos, fps):
        # background
        pygame.draw.rect(screen, Colors.LightBackground, (self.pos[0] - 1, self.pos[1] - 1, self.size[0] + 2, self.size[1] + 2))
        pygame.draw.rect(screen, Colors.Background, (self.pos[0], self.pos[1], self.size[0], self.size[1]))
        pygame.draw.rect(screen, Colors.LightBackground, (self.pos[0] + 20, self.pos[1], 1, 20))
        pygame.draw.rect(screen, Colors.LightBackground, (self.pos[0], self.pos[1] + self.size[1] - 21, self.size[0], 1))

        # top bar
        pygame.draw.rect(screen, Colors.LightBackground, (self.pos[0], self.pos[1] + 20, self.size[0], 1))

        # refresh files
        screen.blit(self.refreshpng, (self.pos[0] + 20 / 2 - self.refreshpng.get_width() / 2, self.pos[1] + 20 / 2 - self.refreshpng.get_height() / 2))
        if mousepos[0] > self.pos[0] and mousepos[0] < self.pos[0] + 20 and mousepos[1] > self.pos[1] and mousepos[1] < self.pos[1] + 20:
            if pygame.mouse.get_pressed()[0] == True:
                self.clicked_mouse = True
            else:
                if self.clicked_mouse == True:
                    self.clicked_mouse = False
                    self.file_list = os.listdir(self.scriptpath)
                    self.loaded_code.clear()

        # calculating time ( added lag technically )
        self.calc_time -= (self.calc_time - round(1 / (1 + fps) * 10000)) * (1 / (1 + fps)) * 10
        if self.calc_time >= 10000:
            self.calc_time = 0
        sprite = Colors.FontSmall.render(str(round(self.calc_time)) + "ms", True, (190, 190, 190))
        screen.blit(sprite, (self.pos[0] + 25, self.pos[1] + 20 / 2 - sprite.get_height() / 2))

        # list all files
        for i in range(0, len(self.file_list)):
            sprite = Colors.FontSmall.render(str(self.file_list[i]), True, (190, 190, 190))
            screen.blit(sprite, (self.pos[0] + 10, self.pos[1] + 25 + i * 20))

            # more background to override long names
            pygame.draw.rect(screen, Colors.Background, (self.pos[0] + self.size[0] - 28, self.pos[1] + 21, 28, self.size[1] - 42))

            # if script not loaded
            if self.file_list[i] not in self.loaded_script_names:
                # add script
                if mousepos[0] > self.pos[0] + self.size[0] - 25 and mousepos[0] < self.pos[0] + self.size[0] and mousepos[1] > self.pos[1] + 25 + i * 20 and mousepos[1] < self.pos[1] + 25 + (i + 1) * 20:
                    pygame.draw.polygon(screen, (100, 250, 100), (
                    (2 + self.pos[0] + self.size[0] - 25, 2 + self.pos[1] + 25 + i * 20),
                    (2 + self.pos[0] + self.size[0] - 25, 16 + self.pos[1] + 25 + i * 20),
                    (16 + self.pos[0] + self.size[0] - 25, 8 + self.pos[1] + 25 + i * 20)))

                    if pygame.mouse.get_pressed()[0] == True and self.delaytime + 0.1 < time.time():

                        # save enviroment
                        with open(self.scriptpath + self.file_list[i], "r") as file:

                            passedtest = True
                            readfile = file.read()
                            lines = readfile.split("\n")
                            for x in range(0, len(self.unallowedlist)):
                                for y in range(0, len(lines)):
                                    if self.unallowedlist[x] in lines[y]:
                                        passedtest = False
                                        self.errortime = time.time()
                                        self.error = "not allowed to run! > '" + str(self.unallowedlist[x]) + "' in line: " + str(y+1)
                                        break
                            if passedtest == True:
                                self.loaded_script_names.append(self.file_list[i])
                                self.loaded_code.append(readfile)



                        self.delaytime = time.time()
                else:
                    pygame.draw.polygon(screen, (50, 150, 50), (
                    (2 + self.pos[0] + self.size[0] - 25, 2 + self.pos[1] + 25 + i * 20),
                    (2 + self.pos[0] + self.size[0] - 25, 16 + self.pos[1] + 25 + i * 20),
                    (16 + self.pos[0] + self.size[0] - 25, 8 + self.pos[1] + 25 + i * 20)))

            else:
                # remove script
                if mousepos[0] > self.pos[0] + self.size[0] - 25 and mousepos[0] < self.pos[0] + self.size[0] and mousepos[1] > self.pos[1] + 25 + i * 20 and mousepos[1] < self.pos[1] + 25 + (i + 1) * 20:
                    pygame.draw.polygon(screen, (100, 250, 100), (
                        (3 + self.pos[0] + self.size[0] - 25, 2 + self.pos[1] + 25 + i * 20),
                        (3 + self.pos[0] + self.size[0] - 25, 16 + self.pos[1] + 25 + i * 20),
                        (6 + self.pos[0] + self.size[0] - 25, 16 + self.pos[1] + 25 + i * 20),
                        (6 + self.pos[0] + self.size[0] - 25, 2 + self.pos[1] + 25 + i * 20)))

                    pygame.draw.polygon(screen, (100, 250, 100), (
                        (9 + self.pos[0] + self.size[0] - 25, 2 + self.pos[1] + 25 + i * 20),
                        (9 + self.pos[0] + self.size[0] - 25, 16 + self.pos[1] + 25 + i * 20),
                        (12 + self.pos[0] + self.size[0] - 25, 16 + self.pos[1] + 25 + i * 20),
                        (12 + self.pos[0] + self.size[0] - 25, 2 + self.pos[1] + 25 + i * 20)))

                    if pygame.mouse.get_pressed()[0] == True and self.delaytime + 0.1 < time.time():

                        self.loaded_code.remove(self.loaded_code[self.loaded_script_names.index(self.file_list[i])])
                        self.loaded_script_names.remove(self.loaded_script_names[self.loaded_script_names.index(self.file_list[i])])


                        self.delaytime = time.time()
                else:
                    pygame.draw.polygon(screen, (50, 150, 50), (
                        (3 + self.pos[0] + self.size[0] - 25, 2 + self.pos[1] + 25 + i * 20),
                        (3 + self.pos[0] + self.size[0] - 25, 16 + self.pos[1] + 25 + i * 20),
                        (6 + self.pos[0] + self.size[0] - 25, 16 + self.pos[1] + 25 + i * 20),
                        (6 + self.pos[0] + self.size[0] - 25, 2 + self.pos[1] + 25 + i * 20)))

                    pygame.draw.polygon(screen, (50, 150, 50), (
                        (9 + self.pos[0] + self.size[0] - 25, 2 + self.pos[1] + 25 + i * 20),
                        (9 + self.pos[0] + self.size[0] - 25, 16 + self.pos[1] + 25 + i * 20),
                        (12 + self.pos[0] + self.size[0] - 25, 16 + self.pos[1] + 25 + i * 20),
                        (12 + self.pos[0] + self.size[0] - 25, 2 + self.pos[1] + 25 + i * 20)))

        ## magic :)
        for i in range(0, len(self.loaded_code)):
            try:
                exec(compile(self.loaded_code[i], self.loaded_script_names[i], "exec"))
            except Exception as error:
                self.error = error
                self.loaded_code.remove(self.loaded_code[i])
                self.loaded_script_names.remove(self.loaded_script_names[i])
                self.errortime = time.time()


        # error handling
        if self.error != "":
            self.errorsurface.fill(Colors.Background)
            sprite = Colors.FontSmall.render(str(self.error), True, (190, 190, 190))
            self.errorsurface.blit(sprite, (clamp(-self.errorscroll + 5, -abs(self.size[0] - sprite.get_width() - 5), 5), 0))
            screen.blit(self.errorsurface, (self.pos[0], self.pos[1] + self.size[1] - self.errorsurface.get_height()))

            if sprite.get_width() > self.size[0]:
                if self.errortime + 1.5 < time.time():
                    if self.errorscroll < abs(self.size[0] - sprite.get_width()) * 5:
                        self.errorscroll += self.calc_time / 100
                    else:
                        self.error = ""
                        self.errorscroll = 0
            else:
                if self.errortime + 1.5 < time.time():
                    self.error = ""