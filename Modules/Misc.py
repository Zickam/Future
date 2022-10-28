import time
from Offsets.offsets import m_bIsScoped, m_bUseCustomAutoExposureMin, m_bUseCustomAutoExposureMax, m_flCustomAutoExposureMin, m_flCustomAutoExposureMax, \
    dwGlowObjectManager, m_vecOrigin
from Modules.configs import row_clanid
from Modules.ConsoleCommand import SendConsoleCommand
from pymem import process, pattern
from Offsets.offsets import dwEntityList

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






def get_sig(pm, modname, _pattern, extra = 0, offset = 0, relative = True, deref = False):
    module = process.module_from_name(pm.process_handle, modname)
    result = pattern.pattern_scan_module(pm.process_handle, module, _pattern)

    if relative == False and deref == True:
        result += extra - module.lpBaseOfDll
    elif relative == True and deref == False:
        result = pm.read_int(result + offset) + extra - module.lpBaseOfDll
    elif relative == False and deref == False:
        result = pm.read_int(result + offset) + extra

    return result

grenade_prediction = 0
showfps = 0
sky_name = 0

def class_id(entity, pm):
    client_networkable = pm.read_uint(entity + 0x8)
    dwGetClientClassFn = pm.read_uint(client_networkable + 0x8)
    entity_client_class = pm.read_uint(dwGetClientClassFn + 0x1)
    class_id = pm.read_uint(entity_client_class + 0x14)
    return class_id
def night_mode(brightness, pm, client):
    entity_list = []


    try:
        entity_list.clear()
        for i in range(0, 1024):
            entity = pm.read_uint(client + dwEntityList + i * 0x10)

            if entity != 0:
                if class_id(entity, pm) == None:
                    continue
                if [entity, class_id(entity, pm)] not in entity_list:
                    entity_list.append([i, entity, class_id(entity, pm)])
    except Exception as err:

        pass

    try:
        for entity in entity_list:
            if entity[2] == 69:
                pm.write_int(entity[1] + m_bUseCustomAutoExposureMin, 0)
                pm.write_int(entity[1] + m_bUseCustomAutoExposureMax, 2)
                pm.write_float(entity[1] + m_flCustomAutoExposureMin, brightness/100)
                pm.write_float(entity[1] + m_flCustomAutoExposureMax, brightness/100)


    except Exception as err:

        pass
def NoSmoke(pm, client):

    glow_objects_list = []

    try:
        glow_objects_list.clear()
        for i in range(1, 1024):
            glow_object = pm.read_uint(pm.read_uint(client + dwGlowObjectManager) + 0x38 * (i - 1) + 0x4)

            if glow_object != 0:
                if class_id(glow_object, pm) == None:
                    continue
                if glow_object not in glow_objects_list:
                    glow_objects_list.append({"objectid": glow_object, "id":class_id(glow_object, pm)})

    except Exception as err:
        pass

    for object in glow_objects_list:
        if object["id"] == 157:
            pm.write_float(object["objectid"] + m_vecOrigin, 0.0)
            pm.write_float(object["objectid"] + m_vecOrigin + 0x4, 0.0)
            pm.write_float(object["objectid"] + m_vecOrigin + 0x8, 0.0)

def GrenadePrediction(state, pm):
    global grenade_prediction
    if grenade_prediction == 0:
        grenade_prediction = ConVar("cl_grenadepreview", pm)
    if grenade_prediction.get_int() == 1 and state == False:
        grenade_prediction.set_int(0)
    if grenade_prediction.get_int() == 0 and state == True:
        grenade_prediction.set_int(1)

def ShowFPS(state, pm):
    global showfps
    if showfps == 0:
        showfps = ConVar("cl_showfps", pm)

    if state == False:
        showfps.set_int(0)
    elif state == True:
        showfps.set_int(1)
def ChangeSky(name, pm):
    global sky_name
    if sky_name == 0:
        sky_name = ConVar("sv_skyname", pm)

    sky_name.set_string(name)

class ConVar():
    def __init__(self, name, pm):
        try:
            self.pm = pm
            self.address = 0
            vstdlib = process.module_from_name(pm.process_handle, 'vstdlib.dll').lpBaseOfDll
            interface_engine_cvar = get_sig(pm, 'vstdlib.dll', rb'\x8B\x0D....\xC7\x05', 0, 2)
            v1 = pm.read_uint(vstdlib + interface_engine_cvar)
            v2 = pm.read_uint(pm.read_uint(pm.read_uint(v1 + 0x34)) + 0x4)
            while v2 != 0:
                if name == pm.read_string(pm.read_uint(v2 + 0x0C)):
                    self.address = v2
                    return
                # print(pm.read_string(pm.read_uint(a0 + 0x0C)))
                v2 = pm.read_uint(v2 + 0x4)
        except Exception as err:
            print(err)

    def get_int(self):
        return self.pm.read_uint(self.address + 0x30) ^ self.address

    def get_name(self):
        return self.pm.read_string(self.pm.read_uint(self.address + 0xC))

    def set_int(self, value: int):
        self.pm.write_int(self.address + 0x30, value ^ self.address)

    def set_string(self, value: str):
        self.pm.write_bytes(self.pm.read_uint(self.address + 0x24), value.encode('utf-8'), 128)


def devCommands():

    commands = ["sv_cheats 1",
                "mp_autokick 0",
                "mp_autoteambalance 0",
                "mp_limitteams 99",
                "mp_startmoney 999999",
                "mp_roundtime_defuse 999999",
                "mp_warmup_end",
                "bot_add",
                "bot_add",
                "bot_add",
                "bot_add",
                "bot_add",
                "bot_add",
                "bot_add",
                "bot_add",
                "bot_add",
                "bot_stop 1",
                "mp_freezetime 0",
                "mp_restartgame 1"]

    for command in commands:
        SendConsoleCommand(command)
