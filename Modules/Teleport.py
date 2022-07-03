import time
import keyboard
from Offsets.offsets import dwbSendPackets


starttime = time.time()
Lag = False

def Teleport(teleport_delay_start, teleport_delay_between, pm, engine):
    global starttime, Lag
    if starttime + teleport_delay_start/1000 < time.time():
        if keyboard.is_pressed("space") and Lag == False:
            pm.write_bool(engine + dwbSendPackets, False)
            starttime = time.time()
            Lag = True



    if starttime + teleport_delay_between/1000 < time.time() and Lag == True:
        starttime = time.time()
        pm.write_bool(engine + dwbSendPackets, True)
        Lag = False

