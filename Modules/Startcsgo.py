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

def RestartSteam():
    for process in psutil.process_iter():
        if "steam.exe" in str(process.name):
            psutil.Process.terminate(process)

    letters = ("abcdefghijklmnopqrstuvwxyz")
    for letter in letters:
        if os.path.exists(letter + ":\\"):
            os.startfile(os.path.abspath(os.path.join(str(letter.upper()) + ":\\Program Files (x86)\\Steam\\steam.exe")))
            print("Steam > restarted")
            break

def StartSteam():
    letters = ("abcdefghijklmnopqrstuvwxyz")
    for letter in letters:
        if os.path.exists(letter + ":\\"):
            os.startfile(os.path.abspath(os.path.join(str(letter.upper()) + ":\\Program Files (x86)\\Steam\\steam.exe")))
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
def Launcher(restartsteam, quit, launchcsgo=True):
    global Steam, Steam_web_helper_count, CSGO

    if restartsteam == True:
        RestartSteam()
        print("Restart")


    if quit == True:
        Quit()

    elif restartsteam == False and quit == False:

        Steam, CSGO, processlist = GetActiveProcesses()
        if Steam == "":
            StartSteam()
        else:
            print("Steam open")

        if CSGO == "":
            subprocess.call('cmd /c start steam://rungameid/730')
        else:
            print("CSGO open")



