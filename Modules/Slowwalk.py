import keyboard

from offsets import dwForceBackward, dwForceForward, dwForceLeft, dwForceRight, m_vecVelocity
Walking = False
def SlowwalkFunction(speed, pm, client, localplayer):
    global Walking

    try:
        w = client + dwForceForward
        a = client + dwForceLeft
        s = client + dwForceBackward
        d = client + dwForceRight
        if keyboard.is_pressed("shift"):
            Walking = False

            velx = pm.read_float(localplayer + m_vecVelocity)
            vely = pm.read_float(localplayer + m_vecVelocity + 0x4)

            if abs(velx) > speed or abs(vely) > speed:
                if Walking == False:
                    pm.write_int(w, 4)
                    pm.write_int(a, 4)
                    pm.write_int(s, 4)
                    pm.write_int(d, 4)
            else:
                if keyboard.is_pressed("w"):
                    pm.write_int(w, 6)
                if keyboard.is_pressed("a"):
                    pm.write_int(a, 6)
                if keyboard.is_pressed("s"):
                    pm.write_int(s, 6)
                if keyboard.is_pressed("d"):
                    pm.write_int(d, 6)
        else:
            if Walking == False:
                Walking = True
                if keyboard.is_pressed("w"):
                    pm.write_int(w, 5)
                if keyboard.is_pressed("a"):
                    pm.write_int(a, 5)
                if keyboard.is_pressed("s"):
                    pm.write_int(s, 5)
                if keyboard.is_pressed("d"):
                    pm.write_int(d, 5)
    except:
        pass

