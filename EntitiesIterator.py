from offsets import dwEntityList, m_iTeamNum, m_iHealth, m_lifeState, m_iGlowIndex, m_dwBoneMatrix

Index = 0

def Entities(ESP_state, Aimbot_states, pm, client):
    global Index
    entities = {}

    if Aimbot_states[1][0] == "Head":
        Index = 8
    elif Aimbot_states[1][0] == "Chest":
        Index = 5
    elif Aimbot_states[1][0] == "Stomach":
        Index = 3

    for i in range(1, 32):
        entity = pm.read_uint(client + dwEntityList + i * 0x10)
        if entity:

            entity_lifeint = pm.read_int(entity + m_lifeState)
            if entity_lifeint != 0:
                continue
            entities[entity] = {}
            entities[entity]["entity_lifeint"] = entity_lifeint

            entity_lifebool = pm.read_bool(entity + m_lifeState)
            if entity_lifebool != False:
                continue
            entities[entity]["entity_lifebool"] = entity_lifebool

            entity_health = pm.read_int(entity + m_iHealth)
            if entity_health <= 0:
                continue

            entities[entity]["entity_health"] = entity_health

            if ESP_state or Aimbot_states[0]:
                entity_glow = pm.read_uint(entity + m_iGlowIndex)
                entities[entity]["entity_glow"] = entity_glow

            entity_team = pm.read_uint(entity + m_iTeamNum)
            entities[entity]["entity_team"] = entity_team

            if Aimbot_states[0]:
                entity_bones = pm.read_uint(entity + m_dwBoneMatrix)
                entitypos_x = pm.read_float(entity_bones + 0x30 * Index + 0xC)
                entitypos_y = pm.read_float(entity_bones + 0x30 * Index + 0x1C)
                entitypos_z = pm.read_float(entity_bones + 0x30 * Index + 0x2C)
                entities[entity]["entitypos_x"] = entitypos_x
                entities[entity]["entitypos_y"] = entitypos_y
                entities[entity]["entitypos_z"] = entitypos_z

            entities[entity]["i"] = i

    return entities