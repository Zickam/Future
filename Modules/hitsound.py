from pygame import mixer
from offsets import dwEntityList, m_iCrosshairId, m_iHealth
import time

mixer.init()

neverlose = mixer.Sound("Modules/neverlose.wav")
bell = mixer.Sound("Modules/bell.wav")
cod = mixer.Sound("Modules/cod.wav")
fatality = mixer.Sound("Modules/fatality.wav")

mixer.Sound.set_volume(neverlose, 0.3)
mixer.Sound.set_volume(bell, 0.3)
mixer.Sound.set_volume(cod, 0.3)
mixer.Sound.set_volume(fatality, 0.3)


health = 0
entityPlayerLookAt = 0
starttime = time.time()
Target = 0

def playsound(entities, pm, client, localplayer, localteam, soundname, on_kill, on_hit):
    global entityPlayerLookAt, health, starttime, Target

    if on_hit:
        crosshairID = pm.read_uint(localplayer + m_iCrosshairId)
        if crosshairID != 0:

            if entityPlayerLookAt == 420 and health == 420:
                entityPlayerLookAt = pm.read_uint(client + dwEntityList + (crosshairID - 1) * 0x10)
                health = entities[entityPlayerLookAt]["entity_health"]
            else:
                entityPlayerLookAt = pm.read_uint(client + dwEntityList + (crosshairID - 1) * 0x10)

                entity_health = entities[entityPlayerLookAt]["entity_health"]

                if health != entity_health:
                    if soundname == "Neverlose":
                        mixer.Sound.play(neverlose)
                    elif soundname == "Bell":
                        mixer.Sound.play(bell)
                    elif soundname == "Cod":
                        mixer.Sound.play(cod)
                    elif soundname == "Fatality":
                        mixer.Sound.play(fatality)

                    health = entity_health

        elif crosshairID == 0:
            health = 420
            entityPlayerLookAt = 420

    if on_kill:
        entitylist = []
        for entity, entity_props in entities.items():
            try:
                entity_team = entity_props["entity_team"]
                crosshairID = pm.read_uint(localplayer + m_iCrosshairId)
                entity_pos_in_iteration = entity_props["i"]

                if crosshairID == entity_pos_in_iteration + 1 and Target == 0:
                    Target = entity

                entity_health = pm.read_uint(Target + m_iHealth)

                if entity_health == 0:
                    if soundname == "Neverlose":
                        mixer.Sound.play(neverlose)
                    elif soundname == "Bell":
                        mixer.Sound.play(bell)
                    elif soundname == "Cod":
                        mixer.Sound.play(cod)
                    elif soundname == "Fatality":
                        mixer.Sound.play(fatality)
                    Target = 0

                if Target != 0 and starttime + 1 < time.time():
                    starttime = time.time()
                    Target = 0

                if (entity_team != localteam) and entity != 0:
                    if entity not in entitylist:
                        entitylist.append(entity)

            except Exception as _ex:
                pass


