from offsets import m_bIsScoped, m_iFOV, m_iFOVStart

def FOVFunction(FOV_reset, FOV_hands, FOV, localplayer, pm, client):

    try:

        m_iDefaultFOV = 0x333C

        if FOV_reset:
            pm.write_int(localplayer + m_iDefaultFOV, 90)
            pm.write_int(localplayer + m_iFOV, 90)
            pm.write_int(localplayer + m_iFOVStart, 90)

        Isscoped = pm.read_uint(localplayer + m_bIsScoped)
        if Isscoped == False:
            pm.write_int(localplayer + m_iDefaultFOV, round(FOV_hands))
            pm.write_int(localplayer + m_iFOV, round(FOV))
            pm.write_int(localplayer + m_iFOVStart, round(FOV))
    except:
        pass