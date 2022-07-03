import keyboard, time

from Offsets.offsets import dwForceLeft, dwForceRight, m_iCrosshairId

delta_time = time.time()
lastpeek = time.time()
state = False

peeked = False

def FastPeek(entities, localplayer, pm, client, engine, engine_pointer):
    global delta_time, state, peeked, lastpeek
    if keyboard.is_pressed("c") and delta_time + 0.15 < time.time():
        state = not state
        delta_time = time.time()

    if state == True and keyboard.is_pressed("alt"):
        crosshairID = pm.read_uint(localplayer + m_iCrosshairId)

        if crosshairID > 0 and crosshairID < 32 and peeked == False and lastpeek + 0.5 < time.time():
            lastpeek = time.time()
            peeked = True
            delta_time = time.time()

    if peeked == True:
        if keyboard.is_pressed("d"):
            pm.write_int(client + dwForceLeft, 1)
            pm.write_int(client + dwForceRight, 0)

        if keyboard.is_pressed("a"):
            pm.write_int(client + dwForceLeft, 0)
            pm.write_int(client + dwForceRight, 1)

        if delta_time + 0.5 < time.time():
            delta_time = time.time()
            peeked = False
            print("Reset")
            if keyboard.is_pressed("a"):
                pm.write_int(client + dwForceLeft, 4)
                pm.write_int(client + dwForceRight, 4)

            if keyboard.is_pressed("d"):
                pm.write_int(client + dwForceLeft, 4)
                pm.write_int(client + dwForceRight, 4)
