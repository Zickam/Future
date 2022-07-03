import time

import win32api, win32con

import random, keyboard

from Offsets.offsets import *
from Modules.weaponIds import pistols, knives, smgs, snipers, rifles, misc, machine_guns, shotguns

def currWeaponId(localplayer, engine, pm, client):

    iCurWeaponAdress = pm.read_uint(localplayer + m_hActiveWeapon) & 0xFFF
    m_iBase = pm.read_uint(client + dwEntityList + (iCurWeaponAdress - 1) * 0x10)
    curr_weapon_id = pm.read_uint(m_iItemDefinitionIndex + m_iBase)

    return curr_weapon_id

wanna_scope = False
time_to_sleep_when_scoping = 0.5
time_update_scope = -1

def makeSnipersScopingIfNot(engine_pointer, engine, pm, client, localplayer):
    global wanna_scope, time_update_scope

    try:
        curr_weapon_id = currWeaponId(localplayer, engine, pm, client)
        scoped = pm.read_uint(localplayer + m_bIsScoped)

        # pm.write_int(client + m_bIsScoped, 1)
        if curr_weapon_id in snipers:
            print("sniper", scoped)
            if (win32api.GetKeyState(win32con.VK_RBUTTON) < 0) and time_update_scope + time_to_sleep_when_scoping <= time.time():
                wanna_scope = not wanna_scope
                time_update_scope = time.time()

            if not scoped and wanna_scope:
                # pm.write_uint(client + m_bIsScoped, 1)
                pm.write_uint(client + dwForceAttack2, 1)
                pm.write_uint(client + dwForceAttack2, 0)

        else:
            if wanna_scope:
                pm.write_uint(client + dwForceAttack2, 0)
                wanna_scope = False

    except Exception as _ex:
        # print("makeSnipersScoping again broken (incorrect weapon id)", _ex)
        pass

def Normalize(x, y):

        while x < -180:
            x += 360
        while x > 180:
            x -= 360
        while y > 89:
            y = 89
        while y < -89:
            y = -89

        return x, y

old_punch_x, old_punch_y = 0, 0
def Recoil(AimBot_btn, pm, client, engine, engine_pointer, localplayer):
    global old_punch_x, old_punch_y

        # iCurWeaponAdress = pm.read_uint(localplayer + m_hActiveWeapon) & 0xFFF
        # m_iBase = pm.read_uint(client + dwEntityList + (iCurWeaponAdress - 1) * 0x10)
        # pm.write_float(m_iBase + m_fAccuracyPenalty, 0.0)

    attack = pm.read_uint(client + dwForceAttack)

    makeSnipersScopingIfNot(engine_pointer, engine, pm, client, localplayer)

    if attack == 7 or attack == 6 or attack == 5:
        curr_weapon = currWeaponId(localplayer, engine, pm, client)
        if curr_weapon not in knives and curr_weapon not in misc:

            # custom settings for every weapon type

            multiplier = 2

            if curr_weapon in pistols:
                multiplier = 1.5

            elif curr_weapon in snipers:
                multiplier = 1

            elif curr_weapon in rifles:
                multiplier = 2

            elif curr_weapon in smgs:
                multiplier = 2.5

            elif curr_weapon in machine_guns:
                multiplier = 2

            elif curr_weapon in shotguns:
                multiplier = 1.3

            shots_fired = pm.read_uint(localplayer + m_iShotsFired)

            if shots_fired > 1:

                curr_x = pm.read_float(engine_pointer + dwClientState_ViewAngles + 0x4)
                curr_y = pm.read_float(engine_pointer + dwClientState_ViewAngles)
                # Normalizing

                punch_angle_x = pm.read_float(localplayer + m_aimPunchAngle + 0x4) * multiplier
                punch_angle_y = pm.read_float(localplayer + m_aimPunchAngle) * multiplier

                newAngle_x = curr_x + old_punch_x - punch_angle_x
                newAngle_y = curr_y + old_punch_y - punch_angle_y
                newAngle_x, newAngle_y = Normalize(newAngle_x, newAngle_y)

                if not AimBot_btn or not keyboard.is_pressed(str("alt")):
                    pm.write_float(engine_pointer + dwClientState_ViewAngles + 0x4, newAngle_x)
                    pm.write_float(engine_pointer + dwClientState_ViewAngles, newAngle_y)

                # print("oldpunch_x, oldpunch_y", old_punch_x, old_punch_y)

                old_punch_x = punch_angle_x
                old_punch_y = punch_angle_y


                # print("curr_x, curr_y", curr_x, curr_y)
                # print("punch_angle_x, punch_angle_y", punch_angle_x, punch_angle_y)
                # print("newAngle_x, newAngle_y", newAngle_x, newAngle_y)
                # time.sleep(1)

    if pm.read_uint(localplayer + m_iShotsFired) == 0:
        old_punch_x = 0.0
        old_punch_y = 0.0

    return old_punch_x, old_punch_y



time_to_sleep = 0.05
_time = time.time()

starttime = time.time()
Framedelta = 0
ShootAgain = False
timeshoot = 50
Frames = 0


def RapidFireForPistols(engine, pm, client, localplayer):
    global timeshoot, _time, Frames, starttime, ShootAgain, Framedelta, mouse

    try:
        curr_weapon_id = currWeaponId(localplayer, engine, pm, client)

        if curr_weapon_id in pistols:
            if (win32api.GetKeyState(0x01) == -128 or win32api.GetKeyState(0x01) == -127) and _time + time_to_sleep <= time.time():
                Frames = Frames + 1
                if time.time() > starttime + 0.25:
                    Framedelta = 1 / (Frames * 4)
                    Frames = 0
                    starttime = time.time()

                if timeshoot > 0:
                    timeshoot = timeshoot - Framedelta * 100

                if ShootAgain == True and timeshoot < 1:
                    ShootAgain = False
                    pm.write_int(client + dwForceAttack, 6)

                pm.write_int(client + dwForceAttack, 6)
                timeshoot = random.randint(10, 25)
                ShootAgain = True

                _time = time.time()

    except Exception as _ex:
        # print("RapidFire again broken (incorrect weapon id)", _ex)
        pass
