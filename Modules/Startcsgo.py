import psutil, os, subprocess

def GetActiveProcesses():
    csgo = ""
    steam = ""
    WindowList = []

    for process in psutil.process_iter():
        Pid = str(process).split("(pid=")[1].split(",")[0]
        Name = str(process).split("name='")[1].split(",")[0].replace("'", "")
        WindowList.append((str(Name) + "," + str(Pid)))

        if Name == "steam.exe":
            steam_path = process.exe().split("\\")[:-1]
            for i in range(0, len(steam_path)):
                steam += steam_path[i] + "\\"
            steam = steam + "config\\"

        if Name == "csgo.exe":
            csgo = process.exe()

        if steam != "" and csgo != "":
            break
    return steam, csgo, WindowList


def steamWorks():
    for process in psutil.process_iter():
        if "steam.exe" in str(process.name):
            return True

    return False


def csgoWorks():
    for process in psutil.process_iter():
        if "csgo.exe" in str(process.name):
            return True

    return False


def csgoAndSteamWorks():
    steam = False
    csgo = False

    for process in psutil.process_iter():
        if "csgo.exe" in str(process.name):
            csgo = True

        elif "steam.exe" in str(process.name):
            steam = True

    if csgo and steam:
        return True

    return False


def RestartSteam():
    for process in psutil.process_iter():
        if "steam.exe" in str(process.name):
            psutil.Process.terminate(process)

    letters = ("abcdefghijklmnopqrstuvwxyz")
    for letter in letters:
        if os.path.exists(letter + ":\\"):
            # restarted = os.startfile(os.path.abspath(os.path.join(str(letter.upper()) + ":\\Program Files (x86)\\Steam\\steam.exe")))
            os.system('start "" "C:\Program Files (x86)\Steam\steam.exe"')
            print("Steam > restarted")
            break


def StartSteam():
    letters = ("abcdefghijklmnopqrstuvwxyz")
    for letter in letters:
        if os.path.exists(letter + ":\\"):
            os.system('start "" "C:\Program Files (x86)\Steam\steam.exe"')
            # started = os.startfile(
            #     os.path.abspath(os.path.join(str(letter.upper()) + ":\\Program Files (x86)\\Steam\\steam.exe")))

            print("Steam > started")
            break

def Quit():
    for process in psutil.process_iter():
        if "steam.exe" in str(process.name):
            psutil.Process.terminate(process)
        if "Counter-Strike: Global Offensive - Direct3D 9" in str(process.name):
            psutil.Process.terminate(process)

CSGO = False
Steam = False
Steam_web_helper_count = 0
def Launcher(restartsteam, clean_start, quit, loggedin, launchcsgo=True):
    global Steam, Steam_web_helper_count, CSGO

    if restartsteam == True:
        RestartSteam()
        print("Restart steam")


    if quit == True:
        print("quitted by startcsgo.launcher")
        Quit()

    elif clean_start:
        Steam, CSGO, processlist = GetActiveProcesses()

        if loggedin and not CSGO and Steam:
            os.system('start steam://rungameid/730')
            print("started csgo")

        elif Steam and not CSGO:
            print("gonna restart", Steam, CSGO)
            RestartSteam()

        elif not Steam and not CSGO and loggedin:
            StartSteam()
            os.system('start steam://rungameid/730')
            print("started steam and csgo")



    elif restartsteam == False and quit == False:

        Steam, CSGO, processlist = GetActiveProcesses()
        if Steam == "":
            StartSteam()
            print("started steam")
        else:
            print("Steam open")

        if CSGO == "":
            os.system('start steam://rungameid/730')
            print("started csgo")
        else:
            print("CSGO open")



