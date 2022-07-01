import pygame, pymem, pymem.process
from Offsets import *
import math
import json



# csgo read ram
pm = pymem.Pymem("csgo.exe")
client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
engine = pymem.process.module_from_name(pm.process_handle, "engine.dll").lpBaseOfDll
engine_pointer = pm.read_uint(engine + dwClientState)


# pygame stuff
screen = pygame.display.set_mode((1024, 1024))
Map = pygame.image.load("mirage.jpg")
pygame.font.init()
font = pygame.font.SysFont("Microsoft Sans Serif", 20, False, False)



Dists = []
def calcDist(Playerpos, Nodelist, array):
    array.clear()

    for Index in range(0, len(Nodelist)):
        Dist = math.hypot(Nodelist[Index][0] - Playerpos[0], Nodelist[Index][1] - Playerpos[1])
        array.append(Dist)

    mindist = min(array)

    for X in range(0, len(array)):
        if array[X] == mindist:
            return mindist, X

WALK = False
FINDPATH = True

# csgo values
localplayer = pm.read_uint(client + dwLocalPlayer)
ForceW = client + dwForceForward
ForceA = client + dwForceLeft
ForceS = client + dwForceBackward
ForceD = client + dwForceRight

PlayerAnim = 0

# pathfinder
NodeList = []
NextNodesAvailable = []
DistCompare = []
IndexList = []
TargetNode = 11
Pathfindernode = 0
SmallestIndex = 0
smallestdist = 0





while True:
    clock = pygame.time.Clock()
    clock.tick(60)
    PlayerAnim += 1

    screen.blit(Map, (0, 0))


    # get pos >> display pixel
    localplayerposX = pm.read_float(localplayer + m_vecOrigin)
    localplayerposY = pm.read_float(localplayer + m_vecOrigin + 0x4)
    localplayeryaw = pm.read_float(engine_pointer + dwClientState_ViewAngles + 0x4)
    lclx = localplayerposX/5+645
    lcly = -localplayerposY/5+340

    # draw nodes with index
    with open("NodesMirage.json") as file:
        options = json.load(file)
        for NodeIndex in range(0, len(options["Nodes"])):
            pygame.draw.circle(screen, (0, 255, 0), options["Nodes"][NodeIndex], 3+math.cos(PlayerAnim/3))
            screen.blit(font.render(str(NodeIndex), True, (0, 0, 0)), options["Nodes"][NodeIndex])


    # closest node with distance and index
    SmallestDist, Index = calcDist((lclx, lcly), options["Nodes"], Dists)
    pygame.draw.line(screen, (255, 255, 255), (lclx, lcly), options["Nodes"][Index])


    # draw next nodes possible
    for NextNodes in range(0, len(options["NextNode"])):

        if options["NextNode"][NextNodes][0] == Index:
            for nextoption in options["NextNode"][NextNodes]:
                pygame.draw.line(screen, (0, 255, 0), options["Nodes"][Index], options["Nodes"][nextoption])
                NextNodesAvailable = options["NextNode"][NextNodes]


    if FINDPATH == True:
        # pathfinder
        CurrentNode = NextNodesAvailable[0]
        CurrentDistToNode = SmallestDist
        NextNodes = NextNodesAvailable
        FullDist = math.hypot(options["Nodes"][CurrentNode][0] - options["Nodes"][TargetNode][0], options["Nodes"][CurrentNode][1] - options["Nodes"][TargetNode][0])

        # details
        pygame.draw.rect(screen, (55, 55, 55), (0, 0, 1024, 150))
        screen.blit(font.render("CurrentNode: " +  str(NextNodesAvailable[0]), True, (255, 255, 255)), (10, 10))
        screen.blit(font.render("CurrentDistToNode: " + str(round(SmallestDist)), True, (255, 255, 255)), (10, 40))
        screen.blit(font.render("NextNodes: " + str(NextNodesAvailable), True, (255, 255, 255)), (10, 70))
        screen.blit(font.render("Curr to Target dist: " + str(round(FullDist)), True, (255, 255, 255)), (10, 100))


        for X in range(0, len(options["NextNode"][Pathfindernode])):
            if X == len(options["NextNode"][Pathfindernode])-1:
                if len(DistCompare) > 1:
                    DistCompare.clear()
                    IndexList.clear()

            if options["NextNode"][Pathfindernode][X] == 22:
                CurrNodeX = options["Nodes"][20][0]
                CurrNodeY = options["Nodes"][20][1]
                DistNowToTar = math.hypot(CurrNodeX - options["Nodes"][TargetNode][0], CurrNodeY - options["Nodes"][TargetNode][1])
                DistCompare.append(round(DistNowToTar))
                IndexList.append(22)
                IndexList.append(21)
                IndexList.append(20)
            elif options["NextNode"][Pathfindernode][X] == 3:
                CurrNodeX = options["Nodes"][7][0]
                CurrNodeY = options["Nodes"][7][1]
                DistNowToTar = math.hypot(CurrNodeX - options["Nodes"][TargetNode][0], CurrNodeY - options["Nodes"][TargetNode][1])
                DistCompare.append(round(DistNowToTar))
                IndexList.append(2)
                IndexList.append(3)
                IndexList.append(4)
                IndexList.append(5)
                IndexList.append(6)
                IndexList.append(7)
            else:
                CurrNodeX = options["Nodes"][options["NextNode"][Pathfindernode][X]][0]
                CurrNodeY = options["Nodes"][options["NextNode"][Pathfindernode][X]][1]
                DistNowToTar = math.hypot(CurrNodeX - options["Nodes"][TargetNode][0], CurrNodeY - options["Nodes"][TargetNode][1])
                DistCompare.append(round(DistNowToTar))
                IndexList.append(options["NextNode"][Pathfindernode][X])

            if len(DistCompare) > len(options["NextNode"][Pathfindernode])-1:
                smallestdist = min(DistCompare)
                for Element in range(0, len(DistCompare)):
                    if smallestdist == DistCompare[Element]:
                        SmallestIndex = IndexList[Element]


        Pathfindernode = SmallestIndex
        if Pathfindernode not in NodeList:
            NodeList.append(Pathfindernode)

        for Node in range(0, len(NodeList)):
            try:
                pygame.draw.line(screen, (255, 255, 255), options["Nodes"][NodeList[Node]], options["Nodes"][NodeList[Node+1]])
            except:
                pass





    pygame.draw.circle(screen, (255, 0, 0), (lclx, lcly), 5+math.cos(PlayerAnim/4)*1.3)

    pygame.display.flip()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()