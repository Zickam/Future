import time
from Offsets.offsets import dwbSendPackets


starttime = time.time()
Lag = False

def FakeLagFunction(State, Delay1, Delay2, pm, engine):
    global starttime, Lag

    try:
        pm.write_bool(engine + dwbSendPackets, True)
        if State == True:
            if starttime + Delay1/1000 < time.time() and Lag == False:
                pm.write_bool(engine + dwbSendPackets, False)
                Lag = True

                starttime = time.time()

            if starttime + Delay2/1000 < time.time() and Lag == True:
                pm.write_bool(engine + dwbSendPackets, True)
                starttime = time.time()
                Lag = False

        if State == False:
            if pm.read_bool(engine + dwbSendPackets) == False:
                pm.write_bool(engine + dwbSendPackets, True)

    except:
        pass
