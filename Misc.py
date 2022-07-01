import time
from offsets import m_bIsScoped
from Modules.configs import row_clanid
from Modules.ConsoleCommand import SendConsoleCommand

from offsets import dwEntityList, m_iHealth, m_lifeState

statichealth = dict()
EntityAdded = False
starttime = time.time()

def RoundStart(entities, pm, client):
    global statichealth, EntityAdded, starttime
    entityInfo = dict()


    for entity, entity_props in entities.items():
        if entity_props["entity_lifeint"] != 0:
            continue

        entityInfo[entity] = entity_props["entity_health"]
        for item in entityInfo.items():
            if item[0] not in statichealth:
                EntityAdded = True
                statichealth[item[0]] = entity_props["entity_health"]

    if EntityAdded == True and starttime + 0.1 < time.time():
        EntityAdded = False

    for item in entityInfo.items():
        if statichealth[item[0]] != item[1]:

            if statichealth[item[0]] > item[1]:
                statichealth[item[0]] = item[1]

            elif statichealth[item[0]] < item[1]:
                statichealth[item[0]] = item[1]
                if EntityAdded == True:
                    EntityAdded = False
                if EntityAdded == False:
                    print("SOMEOME HEALED / ROUNDSTART")
                    return True

import pygame, win32con, win32gui, win32api

crosshair_inited = False
crosshair = -1

def CrosshairOnAWP(localplayer, pm, client, engine, engine_pointer):

    global crosshair_inited

    is_scoped = pm.read_bool(localplayer + m_bIsScoped)

    if is_scoped:
        pm.write_bool(localplayer + m_bIsScoped, False)

tag_changed = time.time()
position_in_row = 0

def ChangeClanTag(localplayer, pm, engine, engine_pointer, client):

    global position_in_row, tag_changed
    try:

        if tag_changed + 1 < time.time():
            if position_in_row == 0:
                SendConsoleCommand(f"cl_clanid {row_clanid[0]}")
                position_in_row = 1

            elif position_in_row == 1:
                SendConsoleCommand(f"cl_clanid {row_clanid[1]}")
                position_in_row = 0

            tag_changed = time.time()

    except Exception as _ex:
        print("Error in ChangeClanTag: ", _ex)
