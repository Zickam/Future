def requestAdminRights():
    import ctypes, sys
    from Modules.logIt import logIt

    if ctypes.windll.shell32.IsUserAnAdmin() == 0:
        logIt("Requesting admin perms", type="START")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

    if ctypes.windll.shell32.IsUserAnAdmin() == 0:
        logIt("We need admin rights to proceed", type="START")
        quit()


def waitForPressSpace(text="Press space to close window"):
    import keyboard, time
    print("-" * int(len(text) * 1.05))
    print(text)

    while 1:
        if keyboard.is_pressed("space"):
            exit()

        else:
            time.sleep(0.01)

def showMessageBox(title: str, text: str):
    import ctypes
    ctypes.windll.user32.MessageBoxW(0, str(text), str(title), 0)