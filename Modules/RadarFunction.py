from Offsets.offsets import m_bSpotted
def RadarFunction(entities, pm, client):

    try:
        for entity in entities.keys():
            if entity:
                pm.write_uchar(entity + m_bSpotted, 1)
    except:
        pass