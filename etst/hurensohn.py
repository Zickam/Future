import pymem.process
from offsets import *
from classids import *
import time
from convar import *


pm = pymem.Pymem("csgo.exe")
client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
engine = pymem.process.module_from_name(pm.process_handle, "engine.dll").lpBaseOfDll
engine_pointer = pm.read_uint(engine + dwClientState)
localplayer = pm.read_uint(client + dwLocalPlayer)
glowmanager = pm.read_uint(client + dwGlowObjectManager)


# remove smokes
def class_id(entity):
    client_networkable = pm.read_uint(entity + 0x8)
    dwGetClientClassFn = pm.read_uint(client_networkable + 0x8)
    entity_client_class = pm.read_uint(dwGetClientClassFn + 0x1)
    class_id = pm.read_uint(entity_client_class + 0x14)
    return class_id
def get_name(entity: int):
    player_info = pm.read_uint(engine_pointer + dwClientState_PlayerInfo)

    player_info_items = pm.read_uint(pm.read_uint(player_info + 0x40) + 0xC)
    info = pm.read_uint(player_info_items + 0x28 + (entity * 0x34))

    if info > 0:
        return pm.read_string(info + 0x10)
def NoSmoke():

    glow_objects_list = []

    try:
        glow_objects_list.clear()
        for i in range(1, 1024):
            glow_object = pm.read_uint(pm.read_uint(client + dwGlowObjectManager) + 0x38 * (i - 1) + 0x4)

            if glow_object != 0:
                if class_id(glow_object) == None:
                    continue
                if glow_object not in glow_objects_list:
                    glow_objects_list.append({"objectid": glow_object, "id":class_id(glow_object)})

    except Exception as err:
        pass

    for object in glow_objects_list:
        if object["id"] == 157:
            #pm.write_float(object["objectid"] + m_vecOrigin, 0.0)
            #pm.write_float(object["objectid"] + m_vecOrigin + 0x4, 0.0)
            pm.write_float(object["objectid"] + m_vecOrigin + 0x8, pm.read_float(object["objectid"] + m_vecOrigin + 0x8) - 2.9)
def night_mode(brightness):
    entity_list = []


    try:
        entity_list.clear()
        for i in range(0, 1024):
            entity = pm.read_uint(client + dwEntityList + i * 0x10)

            if entity != 0:
                if class_id(entity) == None:
                    continue
                if [entity, class_id(entity)] not in entity_list:
                    entity_list.append([i, entity, class_id(entity)])
    except Exception as err:
        pass

    try:
        for entity in entity_list:
            if entity[2] == 69:
                pm.write_int(entity[1] + m_bUseCustomAutoExposureMin, 1)
                pm.write_int(entity[1] + m_bUseCustomAutoExposureMax, 110)
                pm.write_float(entity[1] + m_flCustomAutoExposureMin, brightness)
                pm.write_float(entity[1] + m_flCustomAutoExposureMax, brightness)

    except Exception as err:
        pass
def spectator_list():

    spectators = []
    entity_list = []

    try:
        entity_list.clear()
        for i in range(0, 1024):
            entity = pm.read_uint(client + dwEntityList + i * 0x10)

            if entity != 0:
                if class_id(entity) == None:
                    continue
                if [entity, class_id(entity)] not in entity_list:
                    entity_list.append([i, entity, class_id(entity)])
    except Exception as err:
        pass

    try:
        spectators.clear()

        if pm.read_uint(localplayer + m_iHealth) <= 0:
            spectators.clear()

        for entity in entity_list:
            if entity[2] == 40:
                player_name = get_name(entity[0])
                if player_name == None or player_name == 'GOTV':
                    continue

                teamEnt = pm.read_int(entity + m_iTeamNum)
                teamPly = pm.read_int(localplayer + m_iTeamNum)

                if teamEnt == teamPly:
                    observed_target_handle = pm.read_uint(entity[1] + m_hObserverTarget) & 0xFFF
                    spectated = pm.read_uint(client + dwEntityList + (observed_target_handle - 1) * 0x10)

                    if spectated == localplayer:
                        spectators.append(get_name(entity[0]))



    except Exception as err:
        pass

    print(spectators)

while True:
    NoSmoke()


