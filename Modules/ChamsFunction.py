import time

from offsets import m_iTeamNum, dwEntityList, m_clrRender, model_ambient_min

time_updated = time.time()

def ChamsFunction(entities, TeamColor, EnemyColor, Glow, localplayer, localteam, pm, client, engine):
    global time_updated

    try:
        if time_updated + 0.1 < time.time():
            if Glow == True:
                buf = 1084227584
                point = pm.read_int(engine + model_ambient_min - 44)
                xored = buf ^ point
                pm.write_int(engine + model_ambient_min, xored)
            else:
                b = 0
                pointer = pm.read_int(engine + model_ambient_min - 44)
                xo = b ^ pointer
                pm.write_int(engine + model_ambient_min, xo)

            for entity, entity_props in entities.items():
                entity_team_id = entity_props["entity_team"]
                if entity_team_id != localteam:  # T
                    pm.write_int(entity + m_clrRender, (EnemyColor[0]))  # red
                    pm.write_int(entity + m_clrRender + 0x1, (EnemyColor[1]))  # green
                    pm.write_int(entity + m_clrRender + 0x2, (EnemyColor[2]))  # blue

                elif entity_team_id == localteam:  # CT
                    pm.write_int(entity + m_clrRender, (TeamColor[0]))  # red
                    pm.write_int(entity + m_clrRender + 0x1, (TeamColor[1]))  # green
                    pm.write_int(entity + m_clrRender + 0x2, (TeamColor[2]))  # blue

            time_updated = time.time()

    except Exception as _ex:
        pass

def RESET(entities, pm, client, engine):
    global time_updated

    try:
        if time_updated + 1 < time.time():
            for entity in entities.keys():
                pm.write_uchar(entity + 112, 255)
                pm.write_uchar(entity + 113, 255)
                pm.write_uchar(entity + 114, 255)

                b = 0
                pointer = pm.read_int(engine + model_ambient_min - 44)
                xo = b ^ pointer
                pm.write_int(engine + model_ambient_min, xo)

            time_updated = time.time()

    except:
        pass