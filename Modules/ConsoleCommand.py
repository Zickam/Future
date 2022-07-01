import win32con
import ctypes
import ctypes.wintypes

class COPYDATASTRUCT(ctypes.Structure):
    _fields_ = [
        ('dwData', ctypes.wintypes.LPARAM),
        ('cbData', ctypes.wintypes.DWORD),
        ('lpData', ctypes.c_char_p)
    ]

def SendConsoleCommand(Command):

    FindWindow = ctypes.windll.user32.FindWindowW
    SendMessage = ctypes.windll.user32.SendMessageW

    hwnd = FindWindow('Valve001', None)
    cds = COPYDATASTRUCT()
    cds.dwData = 0
    str = bytes(Command, "utf-8")
    cds.cbData = ctypes.sizeof(ctypes.create_string_buffer(str))
    cds.lpData = ctypes.c_char_p(str)

    SendMessage(hwnd, win32con.WM_COPYDATA, 0, ctypes.byref(cds))

