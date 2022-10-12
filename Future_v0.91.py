showCheatFPS = False
showGUIFPS = False
DEV = False
needAdmin = False
login_success = False
csgo_started = False
login = False
all_detected_correctly = False
is_loading = False


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


gui_program_frames = 0
gui_program_frames_sum = 0
gui_program_count_seconds = 0
gui_program_start_time = -1

def showGUIFPSFunc(fps):
    global gui_program_frames, gui_program_start_time, gui_program_count_seconds, gui_program_frames_sum

    gui_program_frames += 1
    if gui_program_start_time + 1 < time.time():
        gui_program_frames_old = gui_program_frames
        gui_program_start_time = time.time()
        gui_program_frames_sum += gui_program_frames
        gui_program_frames = 0
        gui_program_count_seconds += 1
        gui_program_avg_fps = int(gui_program_frames_sum / gui_program_count_seconds)

        logIt(
            f"GUI_FPS: {Fore.LIGHTBLUE_EX}{gui_program_frames_old}{Style.RESET_ALL} AVG_GUI_FPS: {Fore.LIGHTBLUE_EX}{gui_program_avg_fps}{Style.RESET_ALL} CLOCK_FPS: {Fore.LIGHTBLUE_EX}{fps}{Style.RESET_ALL}",
            type="GUI_FPS")


def gui_updater(buttons_grid, buttons):
    global login_success, csgo_started, is_loading

    login_screen_size = (410, 220)
    screen_size = (410, 410)
    screen = Initscreen(resolution=login_screen_size)
    window = gui.Window(screen_size, [10, 10], screen)  # login window

    clock = pygame.time.Clock()

    LoginScreen = gui.LoginScreen(ServerDB.Client.CheckIfServerOnline())
    Displayer = LogoDisplayer(screen)



    is_login_screen = True

    while 1:
        Mousepos = pygame.mouse.get_pos()
        Framedelta = 1 + clock.get_fps()

        modules_to_display = getActiveModules(buttons)
        Shown = window.Update(modules_to_display, Framedelta, is_login_screen)

        objects_shown = []
        objects_not_shown = []

        login_success = gui.LoginScreen.Update(LoginScreen, screen_size, screen, is_loading, window.pygameevent)

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
                window = gui.Window(screen_size, (10, 10), screen)  # normal gui
                clock = pygame.time.Clock()

                Displayer = LogoDisplayer(screen)

            LogoDisplayer.Update(Displayer)

        if showGUIFPS:
            showGUIFPSFunc(int(clock.get_fps()))

        gui.Refreshscreen()
        clock.tick(60)


main_program_frames = 0
main_program_frames_sum = 0
main_program_count_seconds = 0
main_program_start_time = -1

def ExecutionsCounter():
    global main_program_frames, main_program_start_time, main_program_count_seconds, main_program_frames_sum

    main_program_frames += 1
    if main_program_start_time + 1 < time.time():
        main_program_frames_old = main_program_frames
        main_program_start_time = time.time()
        main_program_frames_sum += main_program_frames
        main_program_frames = 0
        main_program_count_seconds += 1
        main_program_avg_fps = int(main_program_frames_sum / main_program_count_seconds)

        logIt(
            f"IC: {Fore.LIGHTBLUE_EX}{main_program_frames_old}{Style.RESET_ALL} AVG_IC: {Fore.LIGHTBLUE_EX}{main_program_avg_fps}{Style.RESET_ALL}",
            type="IC")


def loginAndGUI():
    buttons_class = gui.Buttons()
    buttons_grid, buttons = buttons_class.buttons_grid, buttons_class.buttons
    start_new_thread(gui_updater, (buttons_grid, buttons,))

    time_to_wait = time.time()
    while 1:
        if time_to_wait - 1 < time.time() and not login_success:
            time.sleep(0.001)
            time_to_wait = time.time()
        else:
            return True, buttons


def main_init():
    global csgo_started, login

    if login:

        pm = 0
        time_to_wait = time.time()
        logIt(f"{Fore.GREEN}Logged in, starting CS:GO...{Style.RESET_ALL}", type="START")

        while 1:

            if time_to_wait + 5 < time.time():
                logIt("Trying to detect", type="START")
                time_to_wait = time.time()
                try:
                    pm = pymem.Pymem("csgo.exe")

                except Exception as _ex:
                    if str(_ex) == "Could not find process: csgo.exe":
                        logIt(f"csgo_started - {csgo_started}", type="WARNING")
                        logIt("Ive removed function to start csgo from this line", type="START")

            if pm:
                break
        try:
            if pm:
                logIt("CS:GO Detected", type="START")

            client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
            if client:
                logIt("Window detected correctly", type="START")
            engine = pymem.process.module_from_name(pm.process_handle, "engine.dll").lpBaseOfDll
            if engine:
                logIt("Engine detected", type="START")
            engine_pointer = pm.read_uint(engine + dwClientState)

            logIt(f"{client, engine, engine_pointer}", type="START")

            logIt("Checking offsets...")
            logIt(updateOffsets(), type="START")
            print()

            if pm and client and engine and engine_pointer:
                logIt(f"{Fore.GREEN}All detected correctly{Style.RESET_ALL}", type="START")

                os.system("cls")
                csgo_started = True
                return (pm, client, engine, engine_pointer)

        except Exception as _ex:
            if str(_ex) == "Could not find process: csgo.exe":
                logIt("Start CSGO!", type="START")
                return main_init()
            elif str(_ex) == "'NoneType' object has no attribute 'lpBaseOfDll'":
                logIt("Waiting for CSGO to start", type="START")
                time.sleep(5)
                return main_init()
            else:
                logIt(f"Some problem: {_ex}", type="START")

    else:
        logIt(f"{Fore.RED}Login failed{Style.RESET_ALL}", type="START")
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

                    Configname = buttons["Config"][1]["ConfigSelector"][0].array[
                        buttons["Config"][1]["ConfigSelector"][0].selected]
                    ConfigManager.SaveConfig(buttons, str(Configname))
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
                    logIt("Start CSGO!", type="START")
                elif str(_ex) == "'NoneType' object has no attribute 'lpBaseOfDll'":
                    logIt("Waiting for CSGO starting", type="START")
                    time.sleep(5)
                    main_init()
                else:
                    logIt(f"Some problem: {_ex}", type="START")

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
                    Misc.ChangeSky(buttons["Visuals"][1]["Sky"][1]["skySelector"][0].array[
                                       buttons["Visuals"][1]["Sky"][1]["skySelector"][0].selected], pm)

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

                    Thirdperson_btn = buttons["Visuals"][1]["3D Person"][0].State
                    if Thirdperson_btn:
                        Thirdperson.ThirdpersonFunction(localplayer, pm, client)

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
                        aimbot_distance = buttons["Combat"][1]["AimBot"][1]["Selector1"][0].array[
                            buttons["Combat"][1]["AimBot"][1]["Selector1"][0].selected]
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

                    if buttons["Misc"][1]["DevCommands"][0].State:
                        Misc.devCommands()
                        print("set dev commands")

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
                        ToxicChat.ToxicChat(entities, toxicchat_killscounter, round_started, toxicchat_kill,
                                            toxicchat_spam, pm, client, localplayer, localteam)

                    if buttons["Misc"][1]["Sound"][0].State:
                        on_kill = buttons["Misc"][1]["Sound"][1]["OnKill"][0].State
                        on_hit = buttons["Misc"][1]["Sound"][1]["OnHit"][0].State
                        sound_name = buttons["Misc"][1]["Sound"][1]["SelectSound"][0].array[
                            buttons["Misc"][1]["Sound"][1]["SelectSound"][0].selected]
                        Hitsound.playsound(entities, pm, client, localplayer, localteam, sound_name, on_kill, on_hit)




            except Exception as _ex:
                if str(_ex) == "Could not find process: csgo.exe":
                    logIt("Start CSGO!")
                    main_init()
                elif str(_ex) == "'NoneType' object has no attribute 'lpBaseOfDll'":
                    logIt("Waiting for CSGO starting")
                    time.sleep(15)
                    main_init()
                else:
                    logIt(f"Some error: {_ex}", type="START")
                    raise _ex


    except Exception as _ex:
        if str(_ex) == "Could not find process: csgo.exe":
            main_init()
        elif str(_ex) == "'NoneType' object has no attribute 'lpBaseOfDll'":
            logIt("Waiting for CS:GO starting")
            time.sleep(15)
            main_init()
        else:
            # if "Could not open process: (int)" restart steam... its vac bypass from injector
            if "Could not open process" in str(_ex):
                error_word_list = str(_ex).split(" ")
                if int(error_word_list[len(error_word_list) - 1]) > 1:
                    logIt("Make function to restart steam", type="DEBUG")

            logIt("other error")
            logIt(f"Some error: {_ex}", type="START")
            raise _ex

            main_init()



def mainOrder():
    global login

    login, buttons = loginAndGUI()
    logIt(f"{Fore.GREEN}Logged in, starting cheat...{Style.RESET_ALL}", type="START")
    # os.system("cls")

    pm, client, engine, engine_pointer = main_init()
    if pm and client and engine and engine_pointer:
        main(pm, client, engine, engine_pointer, buttons)

    else:
        logIt("state 1 occured!!!!!!! (search for it in main file)")  # i dont think it has ever occured
        pm, client, engine, engine_pointer = main_init()
        main(pm, client, engine, engine_pointer, buttons)


if __name__ == "__main__":
    if needAdmin:
        from Modules import utils

        utils.requestAdminRights()

    from Modules import Installer

    Installer.installerfunction()

    import os
    import pygame.time
    import pymem
    import pymem.process
    import time
    from _thread import start_new_thread
    from colorama import Fore
    from colorama import Style

    from Modules import Aimbot, BHOP, ChamsFunction, ConfigManager, EntitiesIterator, FakeLag, FastPeek, FovFunction, \
        GlowESP, Hitsound, Installer, Misc, NoFlashFunction, RadarFunction, RecoilSystem, Slowwalk, Startcsgo, Teleport, \
        Thirdperson, ToxicChat, Triggerbot, utils

    from Offsets.offsets import *

    import ServerDB.Client
    from Modules.logIt import logIt
    from Modules.gui import gui
    from Modules.gui.gui import Initscreen
    from Modules.gui.gui import LogoDisplayer
    from Offsets.Updater import updateOffsets

    mainOrder()
