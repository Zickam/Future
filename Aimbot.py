import keyboard
import random
from offsets import *
import numpy as np
from math import *

Curryaw = 0
Currpitch = 0
SmoothedYaw = 0
SmoothedPitch = 0
randomyaw = 0
randompitch = 0

def calculateangle(pm, client, localplayer, player_origin_x, player_origin_y, player_origin_z, vec_x, vec_y, vec_z, target, target_props, index):
    try:

        velx = pm.read_float(target + m_vecVelocity)
        vely = pm.read_float(target + m_vecVelocity + 0x4)
        velz = pm.read_float(target + m_vecVelocity + 0x8)

        my_pos_x = player_origin_x - vec_x - velx / 120
        my_pos_y = player_origin_y - vec_y - vely / 120
        my_pos_z = player_origin_z + vec_z - velz / 120

        enemy_pos_x = target_props["entitypos_x"]
        enemy_pos_y = target_props["entitypos_y"]
        enemy_pos_z = target_props["entitypos_z"]

        delta_vector_x = enemy_pos_x - my_pos_x
        delta_vector_y = enemy_pos_y - my_pos_y
        delta_vector_z = enemy_pos_z - my_pos_z
        delta_vector_len = sqrt(delta_vector_x ** 2 + delta_vector_y ** 2 + delta_vector_z ** 2)

        pitch = -asin(delta_vector_z / delta_vector_len) * 57.295779513082320876798154814105
        yaw = (atan2(delta_vector_y, delta_vector_x) * 57.295779513082320876798154814105)
        return pitch, yaw, delta_vector_len
    except:
        pass

def markplayer(entities, entity, glow_manager, pm):

    try:
        entity_glow = entities[entity]["entity_glow"]

        pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(1))  # red
        pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(0))  # green
        pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(0))  # blue
        pm.write_float(glow_manager + entity_glow * 0x38 + 0x14, float(1))  # alpha
        pm.write_int(glow_manager + entity_glow * 0x38 + 0x28, 1)  # Enabling

    except Exception as _ex:
        print(_ex)

def findclosestdistance(entities, pm, client, localplayer, enemies, team):
    localplayer_team = pm.read_uint(localplayer + m_iTeamNum)

    player_bones = pm.read_uint(localplayer + m_dwBoneMatrix)
    player_x = pm.read_float(player_bones + 0x30 * 8 + 0xC)
    player_y = pm.read_float(player_bones + 0x30 * 8 + 0x1C)
    player_z = pm.read_float(player_bones + 0x30 * 8 + 0x2C)
    player_head_pos = np.array([player_x, player_y, player_z])

    vectors = dict()

    for entity, entity_props in entities.items():
        try:
            entity_team = entity_props[0]
            if (entity_team != localplayer_team and enemies) or (entity_team == localplayer_team and team):
                entitypos_x = entity_props[6]
                entitypos_y = entity_props[7]
                entitypos_z = entity_props[8]
                entity_head_pos = np.array([entitypos_x, entitypos_y, entitypos_z])
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

    return closest_enemy

def findclosestcroshair(entities, pm, client, localplayer, engine_pointer, enemies, team, player_origin_x, player_origin_y, player_origin_z, vec_x, vec_y, vec_z):

    localplayer_team = pm.read_uint(localplayer + m_iTeamNum)
    yawlist = dict()
    deltas = []
    deltas_names = []

    for entity, entity_props in entities.items():
        try:
            entity_team = entity_props["entity_team"]
            if (entity_team != localplayer_team and enemies) or (entity_team == localplayer_team and team):
                pitch, yaw, dist = calculateangle(pm, client, localplayer, player_origin_x, player_origin_y, player_origin_z, vec_x, vec_y, vec_z, entity, entity_props, 8)
                yawlist[entity] = yaw
        except:
            pass

    localplayeryaw = pm.read_float(engine_pointer + dwClientState_ViewAngles + 0x4)

    for entity, yaw in yawlist.items():
        if yaw != None:
            deltayaw = yaw - localplayeryaw
            deltas.append(abs(deltayaw))
            deltas_names.append(entity)

    if deltas:
        closest_enemy_index = deltas.index(min(deltas))
        closest_enemy = deltas_names[closest_enemy_index]

        return closest_enemy


def playersetangle(Yaw, Pitch, smooth, overunderaim, Distance, multip, pm, engine_pointer):
    global Curryaw, Currpitch, SmoothedYaw, SmoothedPitch, randomyaw, randompitch

    # current angles
    Curryaw = pm.read_float(engine_pointer + dwClientState_ViewAngles + 0x4)
    Currpitch = pm.read_float(engine_pointer + dwClientState_ViewAngles)

    # over aim
    if abs(round(SmoothedYaw) - round(Curryaw)) > 10:
        SmoothedYaw = Curryaw
        if Yaw < Curryaw and randomyaw == 0:
            randomyaw = random.randint(-overunderaim, 0)
        elif Yaw > Curryaw and randomyaw == 0:
            randomyaw = random.randint(-0, overunderaim)


    # if look away
    if round(SmoothedPitch) != round(SmoothedPitch):
        SmoothedPitch = Currpitch

    # smoother
    if smooth > 0 and smooth != 0:
        if Yaw > 0 and Yaw < 180:
            SmoothedYaw -= (SmoothedYaw - (Yaw + randomyaw)) / smooth
            SmoothedPitch -= (SmoothedPitch - (Pitch + randompitch)) / smooth
        else:
            SmoothedYaw += ((Yaw + randomyaw) - SmoothedYaw) / smooth
            SmoothedPitch += ((Pitch + randompitch) - SmoothedPitch) / smooth

        if abs((SmoothedYaw - (Yaw + randomyaw))) < 4:
            randomyaw = 0
    else:
        SmoothedYaw = Yaw
        SmoothedPitch = Pitch

    if multip == True:
        for I in range(-100, 100):
            pm.write_float(engine_pointer + dwClientState_ViewAngles, SmoothedPitch)
            pm.write_float(engine_pointer + dwClientState_ViewAngles + 0x4, SmoothedYaw + I*2.1 / Distance)

    else:
        pm.write_float(engine_pointer + dwClientState_ViewAngles, SmoothedPitch)
        pm.write_float(engine_pointer + dwClientState_ViewAngles + 0x4, SmoothedYaw)

def Aimbot(punch_x_ro_reduce, punch_y_to_reduce, entities, HotKey, distance, enemies, team, Markplayer, fov, target, smooth, overunderaim, Multipoint, pm, client, glow_manager, localplayer, localteam, engine_pointer):
    try:

        player_origin_x = pm.read_float(localplayer + m_vecOrigin)
        player_origin_y = pm.read_float(localplayer + m_vecOrigin + 0x4)
        player_origin_z = pm.read_float(localplayer + m_vecOrigin + 0x8)
        vec_x = pm.read_float(localplayer + m_vecViewOffset)
        vec_y = pm.read_float(localplayer + m_vecViewOffset + 0x4)
        vec_z = pm.read_float(localplayer + m_vecViewOffset + 0x8)

        if distance == "Distance":
            Target = findclosestdistance(entities, pm, client, localplayer, enemies, team)
        else:
            Target = findclosestcroshair(entities, pm, client, localplayer, engine_pointer, enemies, team, player_origin_x, player_origin_y, player_origin_z, vec_x, vec_y, vec_z)

        if Target:
            if Markplayer:
                markplayer(entities, Target, glow_manager, pm)

            if keyboard.is_pressed(str(HotKey)):
                if target == "Stomach":
                    Pitch, Yaw, Distance = calculateangle(pm, client, localplayer, player_origin_x, player_origin_y, player_origin_z, vec_x, vec_y, vec_z, Target, entities[Target], 3)
                elif target == "Chest":
                    Pitch, Yaw, Distance = calculateangle(pm, client, localplayer, player_origin_x, player_origin_y, player_origin_z, vec_x, vec_y, vec_z, Target, entities[Target], 5)
                else:
                    Pitch, Yaw, Distance = calculateangle(pm, client, localplayer, player_origin_x, player_origin_y, player_origin_z, vec_x, vec_y, vec_z, Target, entities[Target], 8)

                PlayerYaw = pm.read_float(engine_pointer + dwClientState_ViewAngles + 0x4)
                PlayerPitch = pm.read_float(engine_pointer + dwClientState_ViewAngles)
                DifferenceYaw = Yaw - PlayerYaw
                DifferencePitch = Pitch - PlayerPitch
                if abs(round(DifferenceYaw)) < fov and abs(round(DifferencePitch)) < fov:
                    Yaw -= punch_x_ro_reduce # match to recoil
                    Pitch -= punch_y_to_reduce #match to recoil
                    playersetangle(Yaw, Pitch, smooth, overunderaim, Distance, Multipoint, pm, engine_pointer)

    except Exception as _ex:
        print(_ex)
