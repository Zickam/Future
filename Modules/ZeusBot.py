import pymem.process
from Offsets.offsets import *
from math import *
import numpy as np

pm = pymem.Pymem("csgo.exe")
client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
engine = pymem.process.module_from_name(pm.process_handle, "engine.dll").lpBaseOfDll
engine_pointer = pm.read_uint(engine + dwClientState)



def findclosestdistance(pm, client, enemies, team):
    localplayer = pm.read_uint(dwLocalPlayer + client)
    localplayer_team = pm.read_uint(localplayer + m_iTeamNum)

    player_bones = pm.read_uint(localplayer + m_dwBoneMatrix)
    player_x = pm.read_float(player_bones + 0x30 * 8 + 0xC)
    player_y = pm.read_float(player_bones + 0x30 * 8 + 0x1C)
    player_z = pm.read_float(player_bones + 0x30 * 8 + 0x2C)
    player_head_pos = np.array([player_x, player_y, player_z])

    vectors = dict()

    for i in range(1, 32):
        try:
            entity = pm.read_uint(client + dwEntityList + i * 0x10)

            if entity:
                entity_team = pm.read_uint(entity + m_iTeamNum)
                if (entity_team != localplayer_team and enemies) or (entity_team == localplayer_team and team):
                    entity_bones = pm.read_uint(entity + m_dwBoneMatrix)
                    entitypos_x = pm.read_float(entity_bones + 0x30 * 8 + 0xC)
                    entitypos_y = pm.read_float(entity_bones + 0x30 * 8 + 0x1C)
                    entitypos_z = pm.read_float(entity_bones + 0x30 * 8 + 0x2C)
                    entity_head_pos = np.array([entitypos_x, entitypos_y, entitypos_z])
                    entity_health = pm.read_int(entity + m_iHealth)
                    entity_dormant = pm.read_uint(entity + m_bDormant)

                    if entity_dormant == 0 and entity_health > 0:
                        vectors[entity] = entity_head_pos

        except:
            continue

    deltas = []
    deltas_names = []
    for entity, pos in vectors.items():
        delta_x = pos[0] - player_head_pos[0]
        delta_y = pos[1] - player_head_pos[1]
        delta_z = pos[2] - player_head_pos[2]
        delta_common = sqrt(delta_x ** 2 + delta_y ** 2 + delta_z ** 2)

        deltas.append(delta_common)
        deltas_names.append(entity)

    closest_enemy_index = deltas.index(min(deltas))
    closest_enemy = deltas_names[closest_enemy_index]

    return closest_enemy, delta_common
def calculateangle(pm, client, target, index):
    try:
        player = pm.read_uint(dwLocalPlayer + client)
        player_origin_x = pm.read_float(player + m_vecOrigin)
        player_origin_y = pm.read_float(player + m_vecOrigin + 0x4)
        player_origin_z = pm.read_float(player + m_vecOrigin + 0x8)

        velx = pm.read_float(target + m_vecVelocity)
        vely = pm.read_float(target + m_vecVelocity + 0x4)
        velz = pm.read_float(target + m_vecVelocity + 0x8)

        vec_x = pm.read_float(player + m_vecViewOffset)
        vec_y = pm.read_float(player + m_vecViewOffset + 0x4)
        vec_z = pm.read_float(player + m_vecViewOffset + 0x8)

        my_pos_x = player_origin_x - vec_x - velx / 120
        my_pos_y = player_origin_y - vec_y - vely / 120
        my_pos_z = player_origin_z + vec_z - velz / 120

        entity_bones = pm.read_uint(target + m_dwBoneMatrix)

        enemy_pos_x = pm.read_float(entity_bones + 0x30 * index + 0xC)
        enemy_pos_y = pm.read_float(entity_bones + 0x30 * index + 0x1C)
        enemy_pos_z = pm.read_float(entity_bones + 0x30 * index + 0x2C)


        delta_vector_x = enemy_pos_x - my_pos_x
        delta_vector_y = enemy_pos_y - my_pos_y
        delta_vector_z = enemy_pos_z - my_pos_z
        delta_vector_len = sqrt(delta_vector_x ** 2 + delta_vector_y ** 2 + delta_vector_z ** 2)


        pitch = -asin(delta_vector_z / delta_vector_len) * 57.295779513082320876798154814105
        yaw = (atan2(delta_vector_y, delta_vector_x) * 57.295779513082320876798154814105)
        return pitch, yaw, delta_vector_len
    except:
        pass


def Zeusbotfunction(State, enemies, team, pm, client, engine_pointer):
    try:
        if State == True:
            id, dist = findclosestdistance(pm, client, enemies, team)
            if dist < 170:

                Yaw, Pitch, Distance = calculateangle(pm, client, id, 5)
                pm.write_float(engine_pointer + dwClientState_ViewAngles, Yaw)
                pm.write_float(engine_pointer + dwClientState_ViewAngles + 0x4, Pitch)
                pm.write_int(client + dwForceAttack, 5)
            else:
                pm.write_int(client + dwForceAttack, 4)
    except:
        pass

