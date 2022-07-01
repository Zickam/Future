from offsets import dwLocalPlayer, m_iCrosshairId, dwEntityList, m_iTeamNum, dwForceAttack, dwClientState_ViewAngles, m_aimPunchAngle, m_aimPunchAngleVel, m_fAccuracyPenalty, m_viewPunchAngle, m_iShotsFired, m_vecVelocity, m_iHealth, m_lifeState, dwForceAttack2, m_bIsScoped, m_fAccuracyPenalty

import time, random, keyboard
from Modules.weaponIds import pistols, knives, smgs, snipers, rifles, misc, machine_guns, shotguns
from Modules.RecoilSystem import currWeaponId

Delay = 0
ResetDelay = False
Frames = 0
starttime = time.time()
Framedelta = 0
ShootAgain = False
timeshoot = 50
HotKey = "alt"

old_entity = -1

def TriggerBotFunction(entities, Trigbotdelay, Team, Enemy, Humanizer, OnPress, shoothighacc, speed, pm, client, localplayer, localTeam, engine_pointer):
    global Delay, ResetDelay, Frames, starttime, Framedelta, timeshoot, ShootAgain, old_entity

    try:
        if (OnPress and keyboard.is_pressed(str(HotKey))) or not OnPress:
            Frames = Frames + 1
            if time.time() > starttime + 0.25:
                Framedelta = 1 / (Frames*4)
                Frames = 0
                starttime = time.time()

            if ResetDelay == True:
                Delay = Trigbotdelay
                ResetDelay = False

            if Delay > 0:
                Delay = Delay - Framedelta*100
            if timeshoot > 0:
                timeshoot = timeshoot - Framedelta*100

            crosshairID = pm.read_uint(localplayer + m_iCrosshairId)
            entityPlayerLookAt = pm.read_uint(client + dwEntityList + (crosshairID - 1) * 0x10)
            crosshairTeam = pm.read_uint(entityPlayerLookAt + m_iTeamNum)

            if crosshairID > 0 and crosshairID < 32:
                if entityPlayerLookAt == old_entity:
                    if Enemy == 1:
                        if localTeam != crosshairTeam:
                            entity_health = entities[entityPlayerLookAt]["entity_health"]
                            entity_lifeint = entities[entityPlayerLookAt]["entity_lifeint"]
                            entity_lifebool = entities[entityPlayerLookAt]["entity_lifebool"]
                            if entity_lifeint == 0 and entity_lifebool == False and entity_health > 0:

                                if Delay < 1:
                                    if shoothighacc == True:
                                        # pm.write_uint(client + dwForceAttack2, 1)
                                        velx = pm.read_float(localplayer + m_vecVelocity)
                                        vely = pm.read_float(localplayer + m_vecVelocity + 0x4)
                                        velz = pm.read_float(localplayer + m_vecVelocity + 0x8)

                                        if abs(velx) + abs(vely) + abs(velz) < speed:
                                            pm.write_int(client + dwForceAttack, 6)
                                            Delay = Trigbotdelay/1000
                                        if Humanizer > 0:
                                            RandomValue = random.randint(0, 100)
                                            timeshoot = random.randint(10, 25)
                                            if RandomValue > (100-Humanizer):
                                                ShootAgain = True
                                    else:
                                        pm.write_int(client + dwForceAttack, 6)
                                        Delay = Trigbotdelay/1000
                                        if Humanizer > 0:
                                            RandomValue = random.randint(0, 100)
                                            timeshoot = random.randint(10, 25)
                                            if RandomValue > (100 - Humanizer):
                                                ShootAgain = True

                            if ShootAgain == True and timeshoot < 1:
                                ShootAgain = False
                                pm.write_int(client + dwForceAttack, 6)

                    if Team == 1:

                        if localTeam == crosshairTeam:
                            entity_health = entities[entityPlayerLookAt]["entity_health"]
                            entity_lifeint = entities[entityPlayerLookAt]["entity_lifeint"]
                            entity_lifebool = entities[entityPlayerLookAt]["entity_lifebool"]
                            if entity_lifeint == 0 and entity_lifebool == False and entity_health > 0:
                                if Delay < 1:
                                    if shoothighacc == True:
                                        velx = pm.read_float(localplayer + m_vecVelocity)
                                        vely = pm.read_float(localplayer + m_vecVelocity + 0x4)
                                        velz = pm.read_float(localplayer + m_vecVelocity + 0x8)

                                        if abs(velx) + abs(vely) + abs(velz) < speed:

                                            # pm.write_uint(client + dwForceAttack2, 1)
                                            pm.write_uint(client + dwForceAttack, 6)
                                            Delay = Trigbotdelay/1000

                                        else:
                                            pm.write_uint(client + dwForceAttack, 6)

                                        if Humanizer > 0:
                                            RandomValue = random.randint(0, 100)
                                            timeshoot = random.randint(10, 25)
                                            if RandomValue > (100 - Humanizer):
                                                ShootAgain = True
                                    else:
                                        pm.write_int(client + dwForceAttack, 6)
                                        Delay = Trigbotdelay/1000
                                        if Humanizer > 0:
                                            RandomValue = random.randint(0, 100)
                                            timeshoot = random.randint(10, 25)
                                            if RandomValue > (100 - Humanizer):
                                                ShootAgain = True

                            if ShootAgain == True and timeshoot < 1:
                                ShootAgain = False
                                pm.write_int(client + dwForceAttack, 6)

                else:
                    if Enemy == 1:
                        if localTeam != crosshairTeam:
                            entity_health = entities[entityPlayerLookAt]["entity_health"]
                            entity_lifeint = entities[entityPlayerLookAt]["entity_lifeint"]
                            entity_lifebool = entities[entityPlayerLookAt]["entity_lifebool"]
                            if entity_lifeint == 0 and entity_lifebool == False and entity_health > 0:

                                if Delay < 1:
                                    if shoothighacc == True:
                                        # pm.write_uint(client + dwForceAttack2, 1)
                                        velx = pm.read_float(localplayer + m_vecVelocity)
                                        vely = pm.read_float(localplayer + m_vecVelocity + 0x4)
                                        velz = pm.read_float(localplayer + m_vecVelocity + 0x8)

                                        if abs(velx) + abs(vely) + abs(velz) < speed:
                                            pm.write_int(client + dwForceAttack, 6)
                                            Delay = Trigbotdelay / 1000
                                        if Humanizer > 0:
                                            RandomValue = random.randint(0, 100)
                                            timeshoot = random.randint(10, 25)
                                            if RandomValue > (100 - Humanizer):
                                                ShootAgain = True
                                    else:
                                        pm.write_int(client + dwForceAttack, 6)
                                        Delay = Trigbotdelay / 1000
                                        if Humanizer > 0:
                                            RandomValue = random.randint(0, 100)
                                            timeshoot = random.randint(10, 25)
                                            if RandomValue > (100 - Humanizer):
                                                ShootAgain = True

                            if ShootAgain == True and timeshoot < 1:
                                ShootAgain = False
                                pm.write_int(client + dwForceAttack, 6)

                    if Team == 1:

                        if localTeam == crosshairTeam:
                            entity_health = entities[entityPlayerLookAt]["entity_health"]
                            entity_lifeint = entities[entityPlayerLookAt]["entity_lifeint"]
                            entity_lifebool = entities[entityPlayerLookAt]["entity_lifebool"]
                            if entity_lifeint == 0 and entity_lifebool == False and entity_health > 0:

                                if Delay < 1:
                                    if shoothighacc == True:
                                        velx = pm.read_float(localplayer + m_vecVelocity)
                                        vely = pm.read_float(localplayer + m_vecVelocity + 0x4)
                                        velz = pm.read_float(localplayer + m_vecVelocity + 0x8)

                                        if abs(velx) + abs(vely) + abs(velz) < speed:
                                            # pm.write_uint(client + dwForceAttack2, 1)
                                            pm.write_uint(client + dwForceAttack, 6)
                                            Delay = Trigbotdelay / 1000
                                        if Humanizer > 0:
                                            RandomValue = random.randint(0, 100)
                                            timeshoot = random.randint(10, 25)
                                            if RandomValue > (100 - Humanizer):
                                                ShootAgain = True
                                    else:
                                        pm.write_int(client + dwForceAttack, 6)
                                        Delay = Trigbotdelay / 1000
                                        if Humanizer > 0:
                                            RandomValue = random.randint(0, 100)
                                            timeshoot = random.randint(10, 25)
                                            if RandomValue > (100 - Humanizer):
                                                ShootAgain = True

                            if ShootAgain == True and timeshoot < 1:
                                ShootAgain = False
                                pm.write_int(client + dwForceAttack, 6)

                if 0.015 + starttime <= time.time():
                    pm.write_uint(client + dwForceAttack, 4)
                    starttime = time.time()
                # pm.write_uint(client + dwForceAttack2, 0)
                old_entity = entityPlayerLookAt

    except:
        pass

