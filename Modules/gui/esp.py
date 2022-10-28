import pygame

import Modules.gui.gui
from Modules.EntitiesIterator import *
from Offsets.offsets import *


def read_matrix(pm, address):
    matrix = []
    for i in range(16):
        matrix.append(pm.read_float(address + 0x4 * i))
    return matrix

def world_to_screen(viewmatrix, vector, width, height):
    clip_x = vector[0] * viewmatrix[0] + vector[1] * viewmatrix[1] + vector[2] * viewmatrix[2] + viewmatrix[3]
    clip_y = vector[0] * viewmatrix[4] + vector[1] * viewmatrix[5] + vector[2] * viewmatrix[6] + viewmatrix[7]
    clip_w = vector[0] * viewmatrix[12] + vector[1] * viewmatrix[13] + vector[2] * viewmatrix[14] + viewmatrix[15]
    if clip_w < 0.1:
        return 200000, 200000
    ndc = (clip_x / clip_w, clip_y / clip_w)
    screenx = (width / 2 * ndc[0]) + (ndc[0] + width / 2)
    screeny = -(height / 2 * ndc[1]) + (ndc[1] + height / 2)
    return (screenx, screeny)



class ESP:
    def __init__(self):
        self.box = False

        self.draw_list = []

        self.screen_size = Modules.gui.gui.screen_size()



    def calculate(self, entities, pm, client):


        viewmatrix = read_matrix(pm, client + dwViewMatrix)


        for entity, values in entities.items():
            entitypos_x = entities[entity]["entitypos_x"]
            entitypos_y = entities[entity]["entitypos_y"]
            entitypos_z = entities[entity]["entitypos_z"]

            x1, y1 = world_to_screen(viewmatrix, (entitypos_x, entitypos_y, entitypos_z - 72), self.screen_size[0], self.screen_size[1])
            x2, y2 = world_to_screen(viewmatrix, (entitypos_x, entitypos_y, entitypos_z), self.screen_size[0], self.screen_size[1])

            if self.box:
                height = y2 - y1
                width = height / 4

                pos1 = x2 + width, y2
                pos2 = x1 + width, y1
                pos3 = x1 - width, y1
                pos4 = x2 - width, y2

                self.draw_list.append({"type": "polygon", "points": [pos1, pos2, pos3, pos4]})





