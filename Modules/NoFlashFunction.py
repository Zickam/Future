from Offsets.offsets import m_flFlashMaxAlpha, m_flFlashDuration
def NoFlashFunction(localplayer, pm, client):

    is_flashed = pm.read_float(localplayer + m_flFlashDuration)
    if is_flashed != 0.0:
        try:
            pm.write_float(localplayer + m_flFlashMaxAlpha, float(0))
        except:
            pass
    else:
        try:
            pm.write_float(localplayer + m_flFlashMaxAlpha, float(255))
        except:
            pass