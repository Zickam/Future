from Modules import ConsoleCommand
import random
from offsets import *
from Modules import Aimbot
import time
from Modules.configs import *

Target = 0
starttime = time.time()
loc_kills = 0

def ToxicChat(entities, KillsCounter, RoundStarted, Kill, Spam, pm, client, localplayer, localplayer_team):
    global Target, starttime, loc_kills

    entitylist = []
    if Spam == True and starttime + 1 < time.time():
        starttime = time.time()
        ConsoleCommand.SendConsoleCommand("say " + str(random.choice(phrases_for_toxicchat)))

    if KillsCounter:
        if RoundStarted:
            print("should be 0")
            loc_kills = 0

        for entity, entity_props in entities.items():
            try:
                entity_team = entity_props["entity_team"]
                crosshairID = pm.read_uint(localplayer + m_iCrosshairId)
                entity_pos_in_iteration = entity_props["i"]

                if crosshairID == entity_pos_in_iteration + 1 and Target == 0:
                    Target = entity

                entity_health = pm.read_uint(Target + m_iHealth)

                if entity_health == 0:
                    loc_kills += 1
                    ConsoleCommand.SendConsoleCommand("say " + str(loc_kills))
                    Target = 0

                if Target != 0 and starttime + 1 < time.time():
                    starttime = time.time()
                    Target = 0

                if (entity_team != localplayer_team) and entity != 0:
                    if entity not in entitylist:
                        entitylist.append(entity)

            except Exception as _ex:
                pass



    if Kill == True:

        for entity, entity_props in entities.items():
            try:
                entity_team = entity_props["entity_team"]
                crosshairID = pm.read_uint(localplayer + m_iCrosshairId)
                entity_pos_in_iteration = entity_props["i"]

                if crosshairID == entity_pos_in_iteration + 1 and Target == 0:
                    Target = entity

                entity_health = pm.read_uint(Target + m_iHealth)

                if entity_health == 0:
                    ConsoleCommand.SendConsoleCommand("say " + str(random.choice(phrases_for_toxicchat)))
                    Target = 0

                if Target != 0 and starttime + 1 < time.time():
                    starttime = time.time()
                    Target = 0

                if (entity_team != localplayer_team) and entity != 0:
                    if entity not in entitylist:
                        entitylist.append(entity)

            except Exception as _ex:
                pass

