import pymem, keyboard, json


def changeskin(State, Skin, Weapon, pm, client, engine_pointer):
    from offsets import dwEntityList, m_hMyWeapons, m_iItemDefinitionIndex, m_OriginalOwnerXuidLow, m_nFallbackPaintKit, m_iItemIDHigh, m_iAccountID, m_nFallbackStatTrak, m_nFallbackSeed, m_flFallbackWear, dwLocalPlayer


    #for i in range(0, 8):
    #    try:
    #        my_weapons = pm.read_int(localplayer + m_hMyWeapons + (i - 1) * 0x4) & 0xFFF
    #        weapon_address = pm.read_int(client + dwEntityList + (my_weapons - 1) * 0x10)
    #        if weapon_address:
    #            weapon_id = pm.read_short(weapon_address + m_iItemDefinitionIndex)
    #
    #            weapon_owner = pm.read_int(weapon_address + m_OriginalOwnerXuidLow)
#
    #            pm.write_int(weapon_address + m_iItemIDHigh, -1)
    #            pm.write_int(weapon_address + m_nFallbackPaintKit, int(SkinID))
    #            pm.write_int(weapon_address + m_iAccountID, weapon_owner)
#
     #           pm.write_int(weapon_address + m_nFallbackSeed, int(Seed))
     #           pm.write_float(weapon_address + m_flFallbackWear, float(int(Wear) + .1))


def Update(pm, engine_pointer):
    pm.write_int(engine_pointer + 0x174, -1)

