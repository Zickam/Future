import psutil, os, subprocess

def GetActiveProcesses():
    WindowList = []

    for process in psutil.process_iter():
        Pid = str(process).split("(pid=")[1].split(",")[0]
        Name = str(process).split("name='")[1].split(",")[0].replace("'", "")
        WindowList.append((str(Name) + "," + str(Pid)))

    return WindowList

def RestartSteam():
    for process in psutil.process_iter():
        if "steam.exe" in str(process.name):
            psutil.Process.terminate(process)

    letters = ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z")
    for letter in letters:
        if os.path.exists(letter + ":\\"):
            os.startfile(os.path.abspath(os.path.join(str(letter.upper()) + ":\\Program Files (x86)\\Steam\\steam.exe")))
            print("Steam > restarted")
            break
def StartSteam():
    letters = ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w","x", "y", "z")
    for letter in letters:
        if os.path.exists(letter + ":\\"):
            os.startfile(
                os.path.abspath(os.path.join(str(letter.upper()) + ":\\Program Files (x86)\\Steam\\steam.exe")))
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

    if quit == True:
        Quit()

    elif restartsteam == False and quit == False:

        for element in GetActiveProcesses():
            if element.split(",")[0] == "steam.exe":
                print("Steam > \t already open")
                Steam = True

        if Steam == False:
            letters = ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v","w", "x", "y", "z")
            for letter in letters:
                if os.path.exists(letter + ":\\"):
                    os.startfile(os.path.abspath(os.path.join(str(letter.upper()) + ":\\Program Files (x86)\\Steam\\steam.exe")))
                    print("Starting > \t steam.exe")
                    Steam = True
                    break

        if Steam == True:
            for element in GetActiveProcesses():
                if element.split(",")[0] == "steam.exe":
                    Steam = True

                if element.split(",")[0] == "steamwebhelper.exe":
                    Steam_web_helper_count += 1

            if Steam_web_helper_count > 5:
                print("Steam > \t launched")
                for element in GetActiveProcesses():
                    if element.split(",")[0] == "csgo.exe":
                        CSGO = True

            if CSGO == False and launchcsgo:
                print("Launching > \t Counter Strike Global Offensive")
                subprocess.call('cmd /c start steam://rungameid/730')
            elif CSGO == True:
                print("CSGO  > \t already open")


