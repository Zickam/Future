from Modules import installer

installer.installerfunction()
import pygame.time, json, pymem, pymem.process, time

from _thread import start_new_thread

from Modules import gui, startcsgo, ConfigManager

from Offsets.offsets import *
from Modules import BHOP, ChamsFunction, FovFunction, GlowESP, NoFlashFunction, RadarFunction, Thirdperson, \
    Triggerbot, Aimbot, Slowwalk, FakeLag, Teleport, ToxicChat, \
    RecoilSystem, EntitiesIterator, FastPeek, Misc, hitsound

from Modules.gui import Initscreen
from Modules.gui import LogoDisplayer
from Offsets.Updater import updateOffsets

showCheatFPS = False
showGUIFPS = False
DEV = False
login_success = False
csgo_started = False
login = False
all_detected_correctly = False
is_loading = False

def getskins():
    skinlist = []
    with open("Data/Structs/skins.json") as file:
        options = json.load(file)
        for element in options:
            skinlist.append(str(element))
    return skinlist

def getweapons():
    idlist = []
    namelist = []
    dmglist = []
    rangelist = []
    armorpen = []
    with open("Data/Structs/WeaponSpecs.json") as file:
        options = json.load(file)
        for element in options:
            idlist.append(element)
        for element in range(0, len(idlist)):
            namelist.append(options[idlist[element]]["name"])
            dmglist.append(options[idlist[element]]["damage"])
            rangelist.append(options[idlist[element]]["accrange"])
            armorpen.append(options[idlist[element]]["armorpen"])
    return idlist, namelist, dmglist, rangelist, armorpen


# window
def Buttons():
    button_size = (80, 25)
    slider_size = (80, 10)
    slider_offsets = (0, 13)
    checkbox_size = (18, 18)
    checkbox_offset = (0, 3)

    buttons_grid = {
        "Visuals": {"type": "button", "pos": (0, 0), "size": button_size, "dependencies": {
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
                             "array": [    "cs_tibet","embassy","italy","jungle","nukeblank","office","sky_cs15_daylight01_hdr","sky_cs15_daylight02_hdr","sky_cs15_daylight03_hdr","sky_cs15_daylight04_hdr","sky_csgo_cloudy01","sky_csgo_night02","sky_csgo_night02b","sky_day02_05","sky_dust","sky_lunacy","sky_venice","vertigo","vertigoblue_hdr","vietnam",]},
            }},
            "Radar": {"type": "button", "pos": (0, 0), "size": button_size},
            "Chams": {"type": "button", "pos": (0, 0), "size": button_size, "dependencies": {
                "Glow": {"type": "button", "pos": (0, 0), "size": button_size},
                "Color": {"type": "colorPicker", "pos": (0, 0), "size": (100, 100)},
                "Color1": {"type": "colorPicker", "pos": (110, -30), "size": (100, 100)}
            }},
            "NoFlash": {"type": "button", "pos": (0, 0), "size": button_size},
            "FOV": {"type": "button", "pos": (0, 0), "size": button_size, "dependencies": {
                "Hands": {"type": "slider", "pos": slider_offsets, "size": slider_size, "start": 70, "end": 170},
                "Fov": {"type": "slider", "pos": slider_offsets, "size": slider_size, "start": 70, "end": 170},
                "Reset FOV": {"type": "button", "pos": (0, 0), "size": button_size},
            }},
            "3D Person": {"type": "button", "pos": (0, 0), "size": button_size},
            "Grenade Prediction": {"type": "button", "pos": (0, 0), "size": button_size},
            "Night Mode": {"type": "button", "pos": (0, 0), "size": button_size, "dependencies": {
                "Brightness": {"type": "slider", "pos": slider_offsets, "size": slider_size, "start": 1, "end": 200},
            }},
            "No Smoke": {"type": "button", "pos": (0, 0), "size": button_size},
            "ShowFPS": {"type": "button", "pos": (0, 0), "size": button_size},


        }},
        "Combat": {"type": "button", "pos": (0, 0), "size": button_size, "dependencies": {
            "AimBot": {"type": "button", "pos": (0, 0), "size": button_size, "dependencies": {
                "Enemies": {"type": "button", "pos": (0, 0), "size": button_size},
                "Team": {"type": "button", "pos": (0, 0), "size": button_size},
                "Markplayer": {"type": "button", "pos": (0, 0), "size": button_size},
                "AimFOV": {"type": "slider", "pos": (0, 25), "size": slider_size, "start": 1, "end": 90},
                "Smooth": {"type": "slider", "pos": (0, 25), "size": slider_size, "start": 0, "end": 100},
                "Overaim": {"type": "slider", "pos": (0, 25), "size": slider_size, "start": 0, "end": 20},
                "Selector": {"type": "selector", "pos": (0, 20), "size": button_size, "array": ["Head", "Chest", "Stomach"]},
                "Selector1": {"type": "selector", "pos": (90, -10), "size": button_size, "array": ["Crosshair", "Distance"]},
                "Multipoint": {"type": "button", "pos": (90, -240), "size": button_size},
            }},
            "TriggerBot": {"type": "button", "pos": (0, 0), "size": button_size, "dependencies": {
                "Highacc": {"type": "button", "pos": (0, 0), "size": button_size},
                "MaxSpeed": {"type": "slider", "pos": (0, 15), "size": slider_size, "start": 0, "end": 300},

                "OnPress": {"type": "button", "pos": (0, 8), "size": button_size},
                "Enemies": {"type": "button", "pos": (0, 8), "size": button_size},
                "Team": {"type": "button", "pos": (0, 8), "size": button_size},
                "Humanizer": {"type": "slider", "pos": (0, 23), "size": slider_size, "start": 0, "end": 100},
                # PercentChance
                "Delay": {"type": "slider", "pos": (0, 20), "size": slider_size, "start": 0, "end": 1000},
                # milliseconds
            }},
            "Recoil": {"type": "button", "pos": (0, 0), "size": button_size},
            "RapidFire": {"type": "button", "pos": (0, 0), "size": button_size},
            "FastPeek": {"type": "button", "pos": (0, 0), "size": button_size}
        }},
        "Misc": {"type": "button", "pos": (0, 0), "size": button_size, "dependencies": {
            "SkinChange": {"type": "button", "pos": (0, 0), "size": button_size, "dependencies": {
                "Skin name": {"type": "searchbox", "pos": (0, 0), "size": button_size, "array": getskins()},
                "Weapon": {"type": "searchbox", "pos": (110, -30), "size": button_size, "array": getweapons()[1]},
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
                "DelayStart": {"type": "slider", "pos": (0, 10), "size": slider_size, "start": 10, "end": 100},
                # milliseconds
                "DelayBetween": {"type": "slider", "pos": (0, 17), "size": slider_size, "start": 10, "end": 300},
                # milliseconds
            }},
            "Teleport": {"type": "button", "pos": (0, 0), "size": button_size, "dependencies": {
                "DelayStart": {"type": "slider", "pos": (0, 10), "size": slider_size, "start": 0, "end": 5000},
                # milliseconds
                "DelayBetween": {"type": "slider", "pos": (0, 17), "size": slider_size, "start": 0, "end": 800},
                # milliseconds
            }},
            "BunnyHop": {"type": "button", "pos": (0, 0), "size": button_size, "dependencies": {
                "AutoStrafe": {"type": "button", "pos": (0, 0), "size": button_size},
            }},
            "Slowwalk": {"type": "button", "pos": (0, 0), "size": button_size, "dependencies": {
                "Speed": {"type": "slider", "pos": slider_offsets, "size": slider_size, "start": 0, "end": 200},
            }},
            "ForceCrosshair": {"type": "checkbox", "pos": checkbox_offset, "size": checkbox_size},
            "ClanTag": {"type": "checkbox", "pos": checkbox_offset, "size": checkbox_size},

        }},
        "Config": {"type": "button", "pos": (0, 0), "size": button_size, "dependencies": {
            "Load": {"type": "button", "pos": (0, 0), "size": button_size},
            "Save": {"type": "button", "pos": (0, 0), "size": button_size},
            "ConfigSelector": {"type": "selector", "pos": (0, 0), "size": button_size,
                               "array": ["Custom", "Rage", "Semi", "Legit", "Dev"]},
        }},
        "Settings": {"type": "button", "pos": (0, 0), "size": button_size, "dependencies": {
            "Transparency": {"type": "slider", "pos": slider_offsets, "size": slider_size, "start": 50, "end": 255},
            "Change Transparency": {"type": "checkbox", "pos": checkbox_offset, "size": checkbox_size},
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
                _object = gui.Button((pos_x, pos_y), object_props["size"], object_name)
                start_pos_dependencies[1] += gap_y

            elif object_props["type"] == "selector":
                pos_x = object_props["pos"][0] + start_pos_dependencies[0]
                pos_y = object_props["pos"][1] + start_pos_dependencies[1]
                _object = gui.Selector((pos_x, pos_y), object_props["size"], object_name, object_props["array"])
                start_pos_dependencies[1] += gap_y

            elif object_props["type"] == "slider":
                pos_x = object_props["pos"][0] + start_pos_dependencies[0]
                pos_y = object_props["pos"][1] + start_pos_dependencies[1]
                _object = gui.Slider((pos_x, pos_y), object_props["size"], object_name, object_props["start"],
                                     object_props["end"])
                start_pos_dependencies[1] += gap_y

            elif object_props["type"] == "colorPickerButton":
                pos_x = object_props["pos"][0] + start_pos_dependencies[0]
                pos_y = object_props["pos"][1] + start_pos_dependencies[1]
                _object = gui.ColorPickerButton((pos_x, pos_y), object_props["size"], object_name, (255, 255, 255),
                                                (20, 20, 20))
                start_pos_dependencies[1] += gap_y

            elif object_props["type"] == "checkbox":
                pos_x = object_props["pos"][0] + start_pos_dependencies[0]
                pos_y = object_props["pos"][1] + start_pos_dependencies[1]
                _object = gui.Checkbox((pos_x, pos_y), object_props["size"], object_name, (255, 255, 255))
                start_pos_dependencies[1] += gap_y


            elif object_props["type"] == "colorPicker":
                pos_x = object_props["pos"][0] + start_pos_dependencies[0]
                pos_y = object_props["pos"][1] + start_pos_dependencies[1]
                _object = gui.ColorPicker((pos_x, pos_y), object_props["size"], object_name)
                start_pos_dependencies[1] += gap_y

            elif object_props["type"] == "searchbox":
                pos_x = object_props["pos"][0] + start_pos_dependencies[0]
                pos_y = object_props["pos"][1] + start_pos_dependencies[1]
                _object = gui.Searchbox((pos_x, pos_y), object_props["size"], object_name, object_props["array"])
                start_pos_dependencies[1] += gap_y

            elif object_props["type"] == "end":
                continue

            if "dependencies" in object_props:
                _start_pos_for_dependencies = [start_pos_dependencies[0] + gap_x, start_pos_dependencies[1] - gap_y]
                dependencies = iterateThroughButtonDependencies(object_name, object_props["dependencies"],
                                                                _start_pos_for_dependencies)

            else:
                dependencies = None
            objects[object_name] = [_object, dependencies]
        start_pos_dependencies[0] += gap_x

        return objects

    buttons = {}
    pos = [10, 80]
    gap_y = button_size[1] + 5
    gap_x = button_size[0] + 10
    start_pos = [pos[0], pos[1]]

    for object_name, object_props in buttons_grid.items():
        if object_props["type"] == "button":
            pos_x = object_props["pos"][0] + start_pos[0]
            pos_y = object_props["pos"][1] + start_pos[1]
            _object = gui.Button((pos_x, pos_y), object_props["size"], object_name)

        elif object_props["type"] == "selector":
            pos_x = object_props["pos"][0] + start_pos[0]
            pos_y = object_props["pos"][1] + start_pos[1]
            _object = gui.Selector((pos_x, pos_y), object_props["size"], object_name, object_props["array"])


        elif object_props["type"] == "end":
            break

        if "dependencies" in object_props:
            start_pos_for_dependencies = [pos_x + gap_x, pos_y]
            dependencies = iterateThroughButtonDependencies(object_name, object_props["dependencies"],
                                                            start_pos_for_dependencies)

        else:
            dependencies = None

        buttons[object_name] = [_object, dependencies]
        start_pos[1] += gap_y

    # for button, props in buttons_grid.items():
    #     print(button, props)

    return buttons_grid, buttons

def getActiveModules(buttons):
    row = []
    for first_level, first_level_depends in buttons.items():

        for second_level, second_level_depends in first_level_depends[1].items():
            if hasattr(second_level_depends[0], "State"):
                if second_level_depends[0].State == True:
                    row.append(second_level)

    funcs_to_not_to_load = ["Load", "Save", "SkinChange", "FOV", "3D Person", "Radar", "GlowESP", "Chams", "Recoil",
                            "ToxicChat", "Highlight", "Colorstyle", ]

    for i in funcs_to_not_to_load:
        if i in row:
            row.remove(i)

    return row

def gui_updater(buttons_grid, buttons):

    global login_success, csgo_started, is_loading

    login_screen_size = (410, 220)
    screen_size = (410, 410)
    screen = Initscreen(resolution=login_screen_size)
    window = gui.Window(screen_size, [10, 10], screen) # login window
    clock = pygame.time.Clock()

    LoginScreen = gui.LoginScreen()
    Displayer = LogoDisplayer(100, screen_size)

    is_login_screen = True

    while 1:
        Mousepos = pygame.mouse.get_pos()
        Framedelta = 1 + clock.get_fps()

        modules_to_display = getActiveModules(buttons)
        Shown = window.Update(modules_to_display, Framedelta, is_login_screen)

        objects_shown = []
        objects_not_shown = []

        login_success = gui.LoginScreen.Update(LoginScreen, screen_size, screen, is_loading)

        if Shown == True:
            def unTabDependencies(dependencies):

                for object_name, object_props in dependencies.items():
                    if hasattr(object_props[0], "Tab"):
                        object_props[0].Tab = False

            def changeTabInRowExcludeOne(_object_name, row):

                for object_name, object_props in row.items():
                    object_init = object_props[0]
                    if object_init.name != _object_name:
                        object_init.Tab = False

            def iterateThroughButtonDependencies(object_name, object_dependencies):

                for object_name, object_props in object_dependencies.items():
                    _object = object_props[0]
                    dependencies = object_props[1]
                    _object.Update(screen, Mousepos, Framedelta)
                    if hasattr(_object, "Tab"):
                        if _object.Tab == True:
                            changeTabInRowExcludeOne(object_name, object_dependencies)
                            if dependencies != None:
                                objects_shown.append(dependencies.values())
                            _object.Update(screen, Mousepos, Framedelta)
                            if dependencies != None:
                                iterateThroughButtonDependencies(object_name, dependencies)

                        elif _object.Tab == False:
                            if dependencies != None:
                                unTabDependencies(dependencies)
                                objects_not_shown.append(dependencies.values())

                    if hasattr(_object, "State"):
                        if _object.State == True:
                            _object.Update(screen, Mousepos, Framedelta)

            for object_name, object_props in buttons.items():
                _object = object_props[0]
                dependencies = object_props[1]
                _object.Update(screen, Mousepos, Framedelta)
                if hasattr(_object, "Tab"):
                    if _object.Tab == True:
                        changeTabInRowExcludeOne(object_name, buttons)
                        objects_shown.append(dependencies.values())
                        if dependencies != None:
                            iterateThroughButtonDependencies(object_name, dependencies)


                    elif _object.Tab == False:
                        unTabDependencies(dependencies)
                        objects_not_shown.append(dependencies.values())

                if hasattr(_object, "State"):
                    if _object.State == True:
                        _object.Update(screen, Mousepos, Framedelta)

            for i in objects_shown:
                for j in i:
                    j[0].show = True

            for i in objects_not_shown:
                for j in i:
                    j[0].show = False

            gui.Colors.ColorStyle = buttons["Settings"][1]["Colorstyle"][0].processedcolor
            gui.Colors.HighlightBackground = buttons["Settings"][1]["Highlight"][0].processedcolor
            gui.ChangeAlpha = buttons["Settings"][1]["Change Transparency"][0].clicked
            gui.Colors.Transparency = buttons["Settings"][1]["Transparency"][0].VisualState

        if login_success:
            is_loading = True

        if login_success and csgo_started:
            is_loading = False

            if pygame.display.get_window_size() == login_screen_size:
                is_login_screen = False
                screen = Initscreen(resolution=screen_size)
                window = gui.Window(screen_size, (10, 10), screen) # normal gui
                clock = pygame.time.Clock()

                Displayer = LogoDisplayer(100, screen_size)

            LogoDisplayer.Update(Displayer, Framedelta, screen)

        if showGUIFPS:
            print(clock.get_fps())

        gui.Refreshscreen()
        clock.tick(60)


Frames = 0
Frames_sum = 0
count_seconds = 0
starttime = time.time()


def ExecutionsCounter():
    global Frames, starttime, count_seconds, Frames_sum

    Frames += 1
    if starttime + 1 < time.time():
        starttime = time.time()
        print("IC:", Frames, end=" ")
        Frames_sum += Frames
        Frames = 0
        count_seconds += 1
        print("Avg IC:", int(Frames_sum / count_seconds))

def loginAndGUI():

    buttons_grid, buttons = Buttons()
    start_new_thread(gui_updater, (buttons_grid, buttons,))

    time_to_wait = time.time()
    while 1:
        if time_to_wait - 1 < time.time() and not login_success:
            time.sleep(0.001)
            time_to_wait = time.time()

        else:
            print("login returned tryue")
            return True, buttons

def main_init():

    global csgo_started, login

    if login:

        pm = 0
        time_to_wait = time.time()
        while 1:

            if time_to_wait + 5 < time.time():
                print("Trying to detect")
                time_to_wait = time.time()
                try:
                    pm = pymem.Pymem("csgo.exe")

                except Exception as _ex:
                    if str(_ex) == "Could not find process: csgo.exe":
                        print("csgo_styarted - ", csgo_started)
                        if not csgo_started:
                            csgo_started = startcsgo.Launcher(False, False)

            if pm:
                break
        try:
            if pm:
                print("CS:GO Detected")

            client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
            if client:
                print("Window detected correctly")
            engine = pymem.process.module_from_name(pm.process_handle, "engine.dll").lpBaseOfDll
            if engine:
                print("Engine detected")
            engine_pointer = pm.read_uint(engine + dwClientState)
            print(client, engine, engine_pointer)

            print("Checking offsets...")
            print(updateOffsets())
            print()

            if pm and client and engine and engine_pointer:
                print("All detected correctly")
                csgo_started = True
                return (pm, client, engine, engine_pointer)

        except Exception as _ex:
            if str(_ex) == "Could not find process: csgo.exe":
                print("Start CSGO!")
                return main_init()
            elif str(_ex) == "'NoneType' object has no attribute 'lpBaseOfDll'":
                print("Waiting for CSGO to start")
                time.sleep(5)
                return main_init()
            else:
                print("Some problem: ", _ex)

    else:
        print("Login failed")
        return (False, False, False, False)

def main(pm, client, engine, engine_pointer, buttons):

    global csgo_started

    try:

        pm.write_uint(client + dwbSendPackets, 1)

        time.sleep(2)

        while 1:

            if showCheatFPS:
                ExecutionsCounter()

            try:
                ConfigLoad = buttons["Config"][1]["Load"][0].State
                ConfigSave = buttons["Config"][1]["Save"][0].State

                if ConfigSave:
                    time.sleep(0.1)
                    from Modules.ConfigManager import SaveConfig
                    Configname = buttons["Config"][1]["ConfigSelector"][0].array[
                        buttons["Config"][1]["ConfigSelector"][0].selected]
                    SaveConfig(buttons, str(Configname))
                    buttons["Config"][1]["Save"][0].State = 0

                if ConfigLoad == True:

                    time.sleep(0.1)
                    Configname = buttons["Config"][1]["ConfigSelector"][0].array[
                        buttons["Config"][1]["ConfigSelector"][0].selected]
                    Config = ConfigManager.LoadConfig(str(Configname))

                    row_objects = []

                    def iterateThroughButtonDependencies(object_name, object_dependencies):

                        for object_name, object_props in object_dependencies.items():
                            _object = object_props[0]
                            dependencies = object_props[1]

                            row_objects.append(_object)

                            if hasattr(_object, "Tab"):
                                if dependencies != None:
                                    iterateThroughButtonDependencies(object_name, dependencies)

                    for object_name, object_props in buttons.items():
                        _object = object_props[0]
                        dependencies = object_props[1]

                        row_objects.append(_object)

                        if hasattr(_object, "Tab"):
                            if dependencies != None:
                                iterateThroughButtonDependencies(object_name, dependencies)

                    row_states_to_load = []

                    def iterateThroughConfigDependencies(object_name, object_dependencies):

                        for object_name, object_props in object_dependencies.items():
                            _object_state = object_props[0]
                            dependencies = object_props[1]

                            row_states_to_load.append(_object_state)

                            if dependencies != None:
                                iterateThroughConfigDependencies(object_name, dependencies)

                    for object_name, object_props in Config.items():
                        _object_state = object_props[0]
                        dependencies = object_props[1]

                        row_states_to_load.append(_object_state)

                        if dependencies != None:
                            iterateThroughConfigDependencies(object_name, dependencies)

                    for i in range(len(row_objects)):

                        if row_states_to_load[i][0] == "State":
                            row_objects[i].State = row_states_to_load[i][1]

                        elif row_states_to_load[i][0] == "VisualState":
                            row_objects[i].VisualState = row_states_to_load[i][1]
                            row_objects[i].State = row_states_to_load[i][1]
                            if hasattr(row_objects[i], "UpdateState"):
                                row_objects[i].UpdateState()

                        elif row_states_to_load[i][0] == "OutputState":
                            row_objects[i].OutputState = row_states_to_load[i][1]

                        elif row_states_to_load[i][0] == "selected":
                            row_objects[i].array = row_states_to_load[i][1]
                            row_objects[i].selected = row_states_to_load[i][2]

                        elif row_states_to_load[i][0] == "processedcolor":
                            row_objects[i].processedcolor = row_states_to_load[i][1]

                        elif row_states_to_load[i][0] == "text":
                            row_objects[i].text = row_states_to_load[i][1]

                        elif row_states_to_load[i][0] == "clicked":
                            row_objects[i].clicked = row_states_to_load[i][1]

                    buttons["Config"][1]["Load"][0].State = False

            except Exception as _ex:
                if str(_ex) == "Could not find process: csgo.exe":
                    print("Start CSGO!")
                elif str(_ex) == "'NoneType' object has no attribute 'lpBaseOfDll'":
                    print("Waiting for CSGO starting")
                    time.sleep(5)
                    main_init()
                else:
                    print("Some problem: ", _ex)

            try:

                # define some variables
                glow_manager = pm.read_uint(client + dwGlowObjectManager)
                localplayer = pm.read_uint(client + dwLocalPlayer)

                if localplayer and glow_manager:

                    localteam = pm.read_uint(localplayer + m_iTeamNum)
                    # some btns for EntitiesIterator optimization
                    ESP_btn = buttons["Visuals"][1]["GlowESP"][0].State
                    AimBot_btn = buttons["Combat"][1]["AimBot"][0].State
                    Aimbot_element = buttons["Combat"][1]["AimBot"][1]["Selector"][0].array
                    AimBot_infos = (AimBot_btn, Aimbot_element)
                    entities = EntitiesIterator.Entities(ESP_btn, AimBot_infos, pm, client)

                    # Misc.RoundStart(pm, client)



                    # night mode
                    # night_mode_btn = buttons["Visuals"][1]["Night Mode"][0].State
                    # if night_mode_btn:
                    #     Misc.night_mode(buttons["Visuals"][1]["Night Mode"][1]["Brightness"][0].VisualState, pm, client)

                    # smoke removal
                    # no_smoke_btn = buttons["Visuals"][1]["No Smoke"][0].State
                    # if no_smoke_btn:
                    #     Misc.NoSmoke(pm, client)


                    # grenade preview and showfps
                    # grenade_preview_btn = buttons["Visuals"][1]["Grenade Prediction"][0].State
                    # Misc.GrenadePrediction(grenade_preview_btn, pm)
                    # show_fps = buttons["Visuals"][1]["ShowFPS"][0].State
                    # Misc.ShowFPS(show_fps, pm)
                    Misc.ChangeSky(buttons["Visuals"][1]["Sky"][1]["skySelector"][0].array[buttons["Visuals"][1]["Sky"][1]["skySelector"][0].selected], pm)


                    # GlowESP
                    if ESP_btn:
                        glowesp_teamred = buttons["Visuals"][1]["GlowESP"][1]["TeamR"][0].State
                        glowesp_teamgreen = buttons["Visuals"][1]["GlowESP"][1]["TeamG"][0].State
                        glowesp_teamblue = buttons["Visuals"][1]["GlowESP"][1]["TeamB"][0].State
                        glowesp_enemyred = buttons["Visuals"][1]["GlowESP"][1]["EnemyR"][0].State
                        glowesp_enemygreen = buttons["Visuals"][1]["GlowESP"][1]["EnemyG"][0].State
                        glowesp_enemyblue = buttons["Visuals"][1]["GlowESP"][1]["EnemyB"][0].State

                        GlowESP.GlowESPFunction(entities, glowesp_teamred, glowesp_teamgreen, glowesp_teamblue,
                                                glowesp_enemyred, glowesp_enemygreen, glowesp_enemyblue, glow_manager,
                                                localplayer, localteam, pm, client)

                    # Radar

                    if buttons["Visuals"][1]["Radar"][0].State:
                        RadarFunction.RadarFunction(entities, pm, client)

                    # Chams

                    if buttons["Visuals"][1]["Chams"][0].State:
                        Chams_color = buttons["Visuals"][1]["Chams"][1]["Color"][0].processedcolor
                        Chams_color1 = buttons["Visuals"][1]["Chams"][1]["Color1"][0].processedcolor
                        Chams_glow = buttons["Visuals"][1]["Chams"][1]["Glow"][0].State
                        ChamsFunction.ChamsFunction(entities, Chams_color, Chams_color1, Chams_glow, localplayer,
                                                    localteam, pm, client, engine)

                    else:
                        ChamsFunction.RESET(entities, pm, client, engine)

                    # No Flash

                    if buttons["Visuals"][1]["NoFlash"][0].State:
                        NoFlashFunction.NoFlashFunction(localplayer, pm, client)

                    # FOV

                    if buttons["Visuals"][1]["FOV"][0].State:
                        Fov_hands = buttons["Visuals"][1]["FOV"][1]["Hands"][0].VisualState
                        Fov_slider = buttons["Visuals"][1]["FOV"][1]["Fov"][0].VisualState
                        FOV_reset = buttons["Visuals"][1]["FOV"][1]["Reset FOV"][0].State
                        FovFunction.FOVFunction(FOV_reset, Fov_hands, Fov_slider, localplayer, pm, client)

                    # Thirdperson

                    Trdperson_btn = buttons["Visuals"][1]["3D Person"][0].State
                    Thirdperson.ThirdpersonFunction(Trdperson_btn, pm, client)

                    # bhop

                    if buttons["Misc"][1]["BunnyHop"][0].State:
                        bhop_autostrafe = buttons["Misc"][1]["BunnyHop"][1]["AutoStrafe"][0].State

                        BHOP.BHOPFunction(pm, client, localplayer, 2, bhop_autostrafe)

                    # combat

                    # triggerbot
                    # if pm.read_bool(localplayer + m_bIsScoped):
                    #     print(pm.read_float(localplayer + m_fAccuracyPenalty))

                    if buttons["Combat"][1]["TriggerBot"][0].State:
                        triggerbot_delay = buttons["Combat"][1]["TriggerBot"][1]["Delay"][0].VisualState
                        triggerbot_enem = buttons["Combat"][1]["TriggerBot"][1]["Enemies"][0].State
                        triggerbot_team = buttons["Combat"][1]["TriggerBot"][1]["Team"][0].State
                        triggerbot_humanizer = buttons["Combat"][1]["TriggerBot"][1]["Humanizer"][0].VisualState
                        triggerbot_onpress = buttons["Combat"][1]["TriggerBot"][1]["OnPress"][0].State
                        triggerbot_highacc = buttons["Combat"][1]["TriggerBot"][1]["Highacc"][0].State
                        triggerbot_speed = buttons["Combat"][1]["TriggerBot"][1]["MaxSpeed"][0].VisualState
                        Triggerbot.TriggerBotFunction(entities, triggerbot_delay, triggerbot_team, triggerbot_enem,
                                                      triggerbot_humanizer, triggerbot_onpress, triggerbot_highacc,
                                                      triggerbot_speed, pm, client, localplayer, localteam,
                                                      engine_pointer)

                    # recoil

                    punch_x_to_reduce, punch_y_to_reduce = 0.0, 0.0
                    if buttons["Combat"][1]["Recoil"][0].State:
                        punch_x_to_reduce, punch_y_to_reduce = RecoilSystem.Recoil(AimBot_btn, pm, client, engine,
                                                                                   engine_pointer, localplayer)

                    # aimbot

                    if AimBot_btn:
                        aimbot_enemies = buttons["Combat"][1]["AimBot"][1]["Enemies"][0].State
                        aimbot_team = buttons["Combat"][1]["AimBot"][1]["Team"][0].State
                        aimbot_markplayer = buttons["Combat"][1]["AimBot"][1]["Markplayer"][0].State
                        aimbot_distance = buttons["Combat"][1]["AimBot"][1]["Selector1"][0].array[buttons["Combat"][1]["AimBot"][1]["Selector1"][0].selected]
                        aimbot_fov = buttons["Combat"][1]["AimBot"][1]["AimFOV"][0].VisualState
                        aimbot_smooth = buttons["Combat"][1]["AimBot"][1]["Smooth"][0].VisualState
                        aimbot_overaim = buttons["Combat"][1]["AimBot"][1]["Overaim"][0].VisualState
                        aimbot_multipoint = buttons["Combat"][1]["AimBot"][1]["Multipoint"][0].State
                        aimbot_target = buttons["Combat"][1]["AimBot"][1]["Selector"][0].array[
                            buttons["Combat"][1]["AimBot"][1]["Selector"][0].selected]
                        Aimbot.Aimbot(punch_x_to_reduce, punch_y_to_reduce, entities, "alt", aimbot_distance,
                                      aimbot_enemies, aimbot_team, aimbot_markplayer, aimbot_fov, aimbot_target,
                                      aimbot_smooth, aimbot_overaim, aimbot_multipoint, pm, client, glow_manager,
                                      localplayer, localteam, engine_pointer)

                    if buttons["Combat"][1]["RapidFire"][0].State:
                        RecoilSystem.RapidFireForPistols(engine, pm, client, localplayer)

                    if buttons["Combat"][1]["FastPeek"][0].State:
                        FastPeek.FastPeek(entities, localplayer, pm, client, engine, engine_pointer)

                    if buttons["Misc"][1]["Slowwalk"][0].State:
                        slowwalk_speed = buttons["Misc"][1]["Slowwalk"][1]["Speed"][0].VisualState
                        Slowwalk.SlowwalkFunction(slowwalk_speed, pm, client, localplayer)

                    if buttons["Misc"][1]["ForceCrosshair"][0].clicked:
                        Misc.CrosshairOnAWP(localplayer, pm, client, engine, engine_pointer)

                    if buttons["Misc"][1]["ClanTag"][0].clicked:
                        Misc.ChangeClanTag(localplayer, pm, engine, engine_pointer, client)

                    fakelag_btn = buttons["Misc"][1]["FakeLag"][0].State
                    if fakelag_btn:
                        fakelag_delaystart = buttons["Misc"][1]["FakeLag"][1]["DelayStart"][0].VisualState
                        fakelag_delaybetwn = buttons["Misc"][1]["FakeLag"][1]["DelayBetween"][0].VisualState
                        FakeLag.FakeLagFunction(fakelag_btn, fakelag_delaystart, fakelag_delaybetwn, pm, engine)

                    if buttons["Misc"][1]["Teleport"][0].State:
                        teleport_delay_start = buttons["Misc"][1]["Teleport"][1]["DelayStart"][0].VisualState
                        teleport_delay_between = buttons["Misc"][1]["Teleport"][1]["DelayBetween"][0].VisualState
                        Teleport.Teleport(teleport_delay_start, teleport_delay_between, pm, engine)

                    if buttons["Misc"][1]["ToxicChat"][0].State:
                        toxicchat_killscounter = buttons["Misc"][1]["ToxicChat"][1]["KillCounter"][0].State
                        if toxicchat_killscounter:
                            round_started = Misc.RoundStart(entities, pm, client)
                        else:
                            round_started = False
                        toxicchat_kill = buttons["Misc"][1]["ToxicChat"][1]["AfterKill"][0].State
                        toxicchat_spam = buttons["Misc"][1]["ToxicChat"][1]["Spam"][0].State
                        ToxicChat.ToxicChat(entities, toxicchat_killscounter, round_started, toxicchat_kill, toxicchat_spam, pm, client, localplayer, localteam)


                    if buttons["Misc"][1]["Sound"][0].State:
                        on_kill = buttons["Misc"][1]["Sound"][1]["OnKill"][0].State
                        on_hit = buttons["Misc"][1]["Sound"][1]["OnHit"][0].State
                        sound_name = buttons["Misc"][1]["Sound"][1]["SelectSound"][0].array[buttons["Misc"][1]["Sound"][1]["SelectSound"][0].selected]
                        hitsound.playsound(entities, pm, client, localplayer, localteam, sound_name, on_kill, on_hit)




            except Exception as _ex:
                if str(_ex) == "Could not find process: csgo.exe":
                    print("Start CSGO!")
                    main_init()
                elif str(_ex) == "'NoneType' object has no attribute 'lpBaseOfDll'":
                    print("Waiting for CSGO starting")
                    time.sleep(15)
                    main_init()
                else:
                    print("Some error: ", _ex)

    except Exception as _ex:
        if str(_ex) == "Could not find process: csgo.exe":
            main_init()
        elif str(_ex) == "'NoneType' object has no attribute 'lpBaseOfDll'":
            print("Waiting for CS:GO starting")
            time.sleep(15)
            main_init()
        else:
            # if "Could not open process: (int)" restart steam... its vac bypass from injector
            if "Could not open process" in str(_ex):
                error_word_list = str(_ex).split(" ")
                if int(error_word_list[len(error_word_list) - 1]) > 1:
                    print("Make function to restart steam")

            print("other error")
            print("Some error: ", _ex)
            main_init()

def mainOrder():

    global login

    print("there")
    login, buttons = loginAndGUI()
    print("here")
    pm, client, engine, engine_pointer = main_init()
    if pm and client and engine and engine_pointer:
        main(pm, client, engine, engine_pointer, buttons)

    else:
        print("state 1 occured!!!!!!! (search for it in main file)")
        pm, client, engine, engine_pointer = main_init()
        main(pm, client, engine, engine_pointer, buttons)

if __name__ == "__main__":
    mainOrder()

