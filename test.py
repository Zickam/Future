if Enemy == 1:
    if localTeam != crosshairTeam:
        entity_health = entities[entityPlayerLookAt]["entity_health"]
        entity_lifeint = entities[entityPlayerLookAt]["entity_lifeint"]
        entity_lifebool = entities[entityPlayerLookAt]["entity_lifebool"]
        if entity_lifeint == 0 and entity_lifebool == False and entity_health > 0:

            if Delay < 1:
                if shoothighacc == True:
                    pm.write_uint(client + dwForceAttack2, 1)
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
                        pm.write_uint(client + dwForceAttack2, 1)
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
pm.write_uint(client + dwForceAttack2, 0)
old_entity = entityPlayerLookAt