import keyboard
import time
from Offsets.offsets import m_iObserverMode, m_iHealth

thirdperson = False
time_updated_button = -1
updating_interval_button = 0.3


def ThirdpersonFunction(localplayer, pm, client):
    global thirdperson, time_updated_button

    if keyboard.is_pressed("v") and time_updated_button + updating_interval_button < time.time():
        if not thirdperson:
            try:
                health = pm.read_uint(localplayer + m_iHealth)
                if health > 0:
                    pm.write_int(localplayer + m_iObserverMode, 1)
                    thirdperson = True
            except:
                pass

        elif thirdperson:
            try:
                health = pm.read_uint(localplayer + m_iHealth)
                if health > 0:
                    pm.write_int(localplayer + m_iObserverMode, 0)
                    thirdperson = False
            except:
                pass

        time_updated_button = time.time()

    # elif State == False and pm.read_int(localPlayer + m_iObserverMode) != 0:
    #     try:
    #         if health > 0:
    #             pm.write_int(localPlayer + m_iObserverMode, 0)
    #     except:
    #         pass
