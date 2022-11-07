showCheatFPS = False
showGUIFPS = False
DEV = True # search for 'security' through the file for usage (very important)
need_to_update_offsets = False
need_admin = False
need_to_check_for_dependencies = False

csgo_started = False
all_detected_correctly = False
offsets_updated = False
is_loading = False
is_logged_in = False
threads = {}
is_gui_running = False

MAX_WINDOW_FPS = 60
TIME_TO_WAIT_FOR_CSGO_STARTS = 1
SCREEN_SIZE = (410, 410)
LOGIN_SCREEN_SIZE = (410, 220)

logs_folder = "logs"
logs_file = "logs.log"

import os
import sys
import subprocess

try:
    from loguru import logger
except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'loguru'])
    print("Installed loguru")

try:
    log_file_path = os.path.join(logs_folder, logs_file)
    logger.add(log_file_path, format="[{level}] {time} {message}",
               level="DEBUG", rotation="1 MB", compression="zip")
except Exception as err:
    raise err


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


def initGuiVars():
    overlay = initscreen(resolution=LOGIN_SCREEN_SIZE)
    screen = overlay.screen
    window = gui.Window(SCREEN_SIZE, [10, 10], overlay)  # login window
    clock = pygame.time.Clock()

    return window, screen, overlay, clock


def loginScreenUpdate(overlay, window, clock, screen):
    global is_login_screen, is_loading, is_logged_in

    if not DEV:  # security
        LoginScreen = gui.LoginScreen(ServerDB.Client.CheckIfServerOnline(), overlay)
        Displayer = LogoDisplayer(overlay)

        is_login_screen = True

    else:
        is_logged_in = True
        is_login_screen = False
        is_loading = False
        overlay = initscreen(resolution=SCREEN_SIZE)
        screen = overlay.screen
        window = gui.Window(SCREEN_SIZE, [10, 10], overlay)  # login window
        clock = pygame.time.Clock()
        return window, screen, overlay, clock


    while 1:
        mousepos = pygame.mouse.get_pos()
        pygameevent = pygame.event.get()

        framedelta = 1 + clock.get_fps()

        Shown = window.Update(framedelta, is_login_screen, mousepos, pygameevent)

        if Shown: break

        is_logged_in = gui.LoginScreen.Update(LoginScreen, SCREEN_SIZE, overlay, is_loading, window.pygameevent)

        if is_logged_in:
            is_loading = True

        if is_logged_in and csgo_started:
            is_loading = False

            if (overlay.winsize[2], overlay.winsize[3]) == LOGIN_SCREEN_SIZE:
                is_login_screen = False
                overlay = initscreen(resolution=SCREEN_SIZE)
                screen = overlay.screen
                window = gui.Window(SCREEN_SIZE, (10, 10), overlay)  # normal gui
                clock = pygame.time.Clock()
  # security
                Displayer = LogoDisplayer(overlay)
 # security
            LogoDisplayer.Update(Displayer)

        if showGUIFPS:
            showGUIFPSFunc(int(clock.get_fps()))

        gui.refreshscreen()
        clock.tick(MAX_WINDOW_FPS)

    return window, screen, overlay, clock


def designsApply(gui_grid):
    if gui.Colors.ColorStyle != gui_grid.Settings.ColorStyle.processedcolor:
        gui.Colors.ColorStyle = gui_grid.Settings.ColorStyle.processedcolor

    if gui.Colors.HighlightBackground != gui_grid.Settings.Highlight.processedcolor:
        gui.Colors.HighlightBackground = gui_grid.Settings.Highlight.processedcolor

    if gui.ChangeAlpha != gui_grid.Settings.ChangeTransparency.clicked:
        gui.ChangeAlpha = gui_grid.Settings.ChangeTransparency.clicked

    if gui.Colors.Transparency != gui_grid.Settings.Transparency.VisualState:
        gui.Colors.Transparency = gui_grid.Settings.Transparency.VisualState


def guiUpdater(gui_grid_class):
    global csgo_started, is_loading, is_logged_in, is_gui_running
    try:
        window, screen, overlay, clock = initGuiVars()

        window, screen, overlay, clock = loginScreenUpdate(overlay, window, clock, screen)

        from Modules.gui.gui import GuiGrid
        gui_grid: GuiGrid = gui_grid_class.gui_grid

        while 1:
            mousepos = pygame.mouse.get_pos()
            pygameevent = pygame.event.get()

            framedelta = 1 + clock.get_fps()

            Shown = window.Update(framedelta, is_login_screen, mousepos, pygameevent)

            objects_shown = []
            objects_not_shown = []

            if Shown == True:

                gui_grid_class.gui_grid._updateDependencies(screen, mousepos, pygameevent, framedelta)

                designsApply(gui_grid)

            if showGUIFPS:
                showGUIFPSFunc(int(clock.get_fps()))

            gui.refreshscreen()
            clock.tick(MAX_WINDOW_FPS)

    except Exception as err:
        print(err)
        raise err

    # finally:
    #     is_gui_running = False
    #     sys.exit()

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


def guiInit():
    global is_gui_running
    _gui = gui.Gui()
    gui_grid = _gui.gui_grid

    thread = start_new_thread(guiUpdater, (_gui, ))

    threads["gui_thread"] = thread
    is_gui_running = True

    return gui_grid


def login():
    """This function wait for user to log in"""

    gui_grid = guiInit()

    if DEV: # security
        return True, gui_grid

    time_to_wait = time.time()
    while 1:
        if time_to_wait - 1 < time.time() and not is_logged_in:
            time.sleep(0.001)
            time_to_wait = time.time()
        else:
            return True, gui_grid


def offsetsUpdater():
    global offsets_updated
    """Calls updateOffsets()"""

    if need_to_update_offsets and not offsets_updated:
        logIt("Checking offsets...")

        res = updateOffsets()

        logIt(res, type="Offsets updater")
        if res is not True:
            logIt("Something went wrong during offsets updating", type="ERROR")
            showMessageBox("Future. Error handling", res)
            quit(-1)

        else:
            logIt(text="Offsets updated", type="START")
            offsets_updated = True

    else:
        logIt("Offsets updater is disabled", type="START")


def detectPm():

    pm = 0
    time_interval = 5
    time_updated = -1

    while 1:

        if time_updated + time_interval < time.time():
            logIt("Trying to detect pm", type="START")
            time_updated = time.time()
            try:
                pm = pymem.Pymem("csgo.exe")

            except Exception as _ex:
                if str(_ex) == "Could not find process: csgo.exe":
                    logIt(f"csgo_started - {csgo_started}", type="WARNING")
                    logIt("Ive removed function to start csgo from this line", type="START")

        if pm:
            return pm


def detectClient(pm):
    try:
        client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
        if client:
            logIt("Window detected correctly", type="START")
            return client

        else:
            return False
    except Exception as err:
        if str(err) == "'NoneType' object has no attribute 'lpBaseOfDll'":
            logIt("Waiting for csgo to start")
            return False


def detectEngine(pm):
    try:
        engine = pymem.process.module_from_name(pm.process_handle, "engine.dll").lpBaseOfDll
        if engine:
            logIt("Engine detected", type="START")
            return engine

        else:
            return False
    except Exception as err:
        logIt(err)
        return False


def varsInit():
    global csgo_started, is_logged_in

    if is_logged_in:

        logIt(f"{Fore.GREEN}Logged in, starting CS:GO...{Style.RESET_ALL}", type="START")

        time.sleep(TIME_TO_WAIT_FOR_CSGO_STARTS)

        pm = detectPm()
        if not pm:
            return varsInit()

        try:
            logIt("CS:GO Detected", type="START")

            client = detectClient(pm)
            if not client:
                return varsInit()

            engine = detectEngine(pm)
            if not engine:
                return varsInit()

            engine_pointer = pm.read_uint(engine + dwClientState)

            if client and engine and engine_pointer:
                logIt(f"{client, engine, engine_pointer}", type="START")

                offsetsUpdater()

                print()

                logIt(f"{Fore.GREEN}All detected correctly{Style.RESET_ALL}", type="START")

                # os.system("cls")
                csgo_started = True
                return (pm, client, engine, engine_pointer)

            else:
                return varsInit()

        except Exception as _ex:
            if str(_ex) == "Could not find process: csgo.exe":
                logIt("Start CSGO!", type="START")
                return varsInit()
            elif str(_ex) == "'NoneType' object has no attribute 'lpBaseOfDll'":
                logIt("Waiting for CSGO to start", type="START")
                return varsInit()
            else:
                logIt(f"Some problem: {_ex}", type="START")
                return varsInit()
    else:
        logIt(f"{Fore.RED}Login failed{Style.RESET_ALL}", type="START")
        return (False, False, False, False)


def mainThread(pm, client, engine, engine_pointer, buttons):
    global csgo_started

    try:

        pm.write_uint(client + dwbSendPackets, 1)

        time.sleep(2)

        while 1:

            if not is_gui_running:
                sys.exit()

            if showCheatFPS:
                ExecutionsCounter()

            try:
                # ConfigLoad = buttons["Config"][1]["Load"][0].State
                # ConfigSave = buttons["Config"][1]["Save"][0].State

                ConfigSave = False
                ConfigLoad = False
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
                    raise _ex
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
            # raise _ex

            main_init()


@logger.catch
def main():
    global is_logged_in
    """
    Waits for user to log in and then 
    proceeds to main cheat function
    """

    try:
        is_logged_in, gui_grid = login()
    except Exception as err:
        logIt(type="GUI_ERROR", text=str(err))
        raise err

    logIt(f"{Fore.GREEN}Logged in, starting cheat...{Style.RESET_ALL}", type="START")
    # os.system("cls")

    pm, client, engine, engine_pointer = varsInit()
    if pm and client and engine and engine_pointer:
        mainThread(pm, client, engine, engine_pointer, gui_grid)

    else:
        logIt("state 1 occured!!!!!!! (search for it in main file)")  # i dont think it has ever occured
        pm, client, engine, engine_pointer = varsInit()
        mainThread(pm, client, engine, engine_pointer, gui_grid)


if __name__ == "__main__":
    try:
        if need_admin:
            from Modules import utils

            utils.requestAdminRights()

        if need_to_check_for_dependencies:
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

        try:
            from Modules import Aimbot, BHOP, ChamsFunction, ConfigManager, EntitiesIterator, FakeLag, FastPeek, FovFunction, \
                GlowESP, Hitsound, Installer, Misc, NoFlashFunction, RadarFunction, RecoilSystem, Slowwalk, Startcsgo, Teleport, \
                Thirdperson, ToxicChat, Triggerbot, utils

        except ImportError as err:
            from Modules.utils import showMessageBox
            from Modules.logIt import logIt

            index = err.msg.find("(") - 1
            if err.msg[:index] == "cannot import name 'dwbSendPackets' from 'Offsets.offsets'":
                logIt(type="ERROR", text=err)
                showMessageBox("Future. ERROR handle", "Please reboot your pc or reinstall the cheat haha")
                exit(-1)

            else:
                logIt(type="ERROR", text=err)
                showMessageBox("Future. ERROR handle", err)

            raise err

        from Offsets.offsets import *

        import ServerDB.Client
        from Modules.utils import showMessageBox
        from Modules.logIt import logIt
        from Modules.gui import gui
        from Modules.gui.gui import initscreen, Gui
        from Modules.gui.gui import LogoDisplayer
        from Offsets.Updater import updateOffsets

        main()

    except Exception as err:
        print(err)
        raise err

    except KeyboardInterrupt as err:
        print(err)
        quit()

    # finally:
    #     sys.exit()
    #     quit()