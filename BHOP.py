import keyboard, time
from pynput.mouse import Controller
from offsets import dwForceJump, m_fFlags, dwForceRight, dwForceLeft

def BHOPFunction(pm, client, localplayer, Autostrafesens, AutoStrafe):

    CMouse = Controller()

    if keyboard.is_pressed("space"):
        force_jump = client + dwForceJump
        on_ground = pm.read_uint(localplayer + m_fFlags)
        force_d = client + dwForceRight
        force_a = client + dwForceLeft

        if AutoStrafe:
            if CMouse.position[0] > 961:
                pm.write_int(force_d, 1)
            if CMouse.position[0] < 959:
                pm.write_int(force_a, 1)


            if CMouse.position[0] == 960:
                pm.write_int(force_a, 2)
                pm.write_int(force_d, 2)



        if localplayer and on_ground:
            if on_ground == 257 or on_ground == 263 or on_ground == 1281 or on_ground == 1287:
                pm.write_int(force_jump, 5)
                time.sleep(0.05)
                pm.write_int(force_jump, 4)