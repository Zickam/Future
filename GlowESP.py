from offsets import dwGlowObjectManager, m_iTeamNum, m_iGlowIndex, dwEntityList

def GlowESPFunction(entities, Teamred, Teamgreen, Teamblue, Enemyred, Enemygreen, Enemyblue, glow_manager, localplayer, localteam, pm, client):

    try:
        for entity, entity_props in entities.items():
            entity_team_id = entity_props["entity_team"]
            entity_glow = entity_props["entity_glow"]

            if localteam == entity_team_id:
                pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(Teamred))  # red
                pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(Teamgreen))  # green
                pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(Teamblue))  # blue
                pm.write_float(glow_manager + entity_glow * 0x38 + 0x14, float(1))  # alpha
                pm.write_int(glow_manager + entity_glow * 0x38 + 0x28, 1)  # Enabling

            else:
                pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(Enemyred))  # red
                pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(Enemygreen))  # green
                pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(Enemyblue))  # blue
                pm.write_float(glow_manager + entity_glow * 0x38 + 0x14, float(1))  # alpha
                pm.write_int(glow_manager + entity_glow * 0x38 + 0x28, 1)  # Enabling
    except:
        pass

