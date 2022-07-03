
def ThirdpersonFunction(State, pm, client):

    from Offsets.offsets import dwLocalPlayer, m_iObserverMode, m_iHealth
    localPlayer = pm.read_uint(client + dwLocalPlayer)
    health = pm.read_uint(localPlayer + m_iHealth)
    if State:
        try:
            if health > 0:
                pm.write_int(localPlayer + m_iObserverMode, 1)
        except:
            pass

    elif State == False and pm.read_int(localPlayer + m_iObserverMode) != 0:
        try:
            if health > 0:
                pm.write_int(localPlayer + m_iObserverMode, 0)
        except:
            pass
