import pygame, pymem, pymem.process, json, math, time
from Offsets import *
from fncs import *

NodeColor = (0, 255, 0)
SelecedNodeColor = (255, 0, 0)
LineColor = (255, 0, 0)
PlayerColor = (0, 255, 255)

DrawNodes = True
DrawConnections = False
DrawPathfinder = True


# csgo read ram
pm = pymem.Pymem("csgo.exe")
client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
engine = pymem.process.module_from_name(pm.process_handle, "engine.dll").lpBaseOfDll
engine_pointer = pm.read_uint(engine + dwClientState)
localplayer = pm.read_uint(client + dwLocalPlayer)
ForceW = client + dwForceForward
ForceA = client + dwForceLeft
ForceS = client + dwForceBackward
ForceD = client + dwForceRight

# pygame stuff
screen = pygame.display.set_mode((1024, 1024))
Map = pygame.image.load("mirage.jpg")
pygame.font.init()
font = pygame.font.SysFont("Microsoft Sans Serif", 20, False, False)

ButtonList = []
ButtonList.append(Button((10, 10), "Edit Nodes"))
ButtonList.append(Button((10, 37), "Connect Node"))


# constant values
CreateNode = False
CreatedNode = False
DeletedNode = False

ConnectNode = False
SelectedNode = 0
ConnectToNode = 0
ConnectedNode = False

# player
ClosestNode = 0
NodeToWalkto = 0
NodeChange = time.time()


# json file
with open("Nodes.json") as file:
    options = json.load(file)


PathFinder = True
Walk = True
# pathfinder
OrigStartnode = 1
OrigTargetNode = 11

StartNode = OrigStartnode
TargetNode = OrigTargetNode
NodeList = [StartNode]
Starttime = time.time()


# main loop
while True:
    clock = pygame.time.Clock()
    clock.tick(60)
    screen.blit(Map, (0, 0))
    mousepos = pygame.mouse.get_pos()

    # localplayer
    localplayerposX = pm.read_float(localplayer + m_vecOrigin)
    localplayerposY = pm.read_float(localplayer + m_vecOrigin + 0x4)
    localplayeryaw = pm.read_float(engine_pointer + dwClientState_ViewAngles + 0x4)
    lclx = localplayerposX / 5 + 645
    lcly = -localplayerposY / 5 + 340
    pygame.draw.circle(screen, PlayerColor, (lclx, lcly), 10)
    for Button in ButtonList:
        Button.Update(mousepos, screen)
        if Button.name == "Edit Nodes":
            CreateNode = Button.State

        if Button.name == "Connect Node":
            ConnectNode = Button.State



    if CreateNode == True:
        if mousepos[0] > 150 and mousepos[1] > 150:
            # add node
            if pygame.mouse.get_pressed()[0] == True and CreatedNode == False:
                with open("Nodes.json", "w") as file:
                    CreatedNode = True
                    options["Nodes"].append(mousepos)
                    json.dump(options, file)
            if pygame.mouse.get_pressed()[0] == False and CreatedNode == True:
                CreatedNode = False

            # delete node
            if pygame.mouse.get_pressed()[2] == True and DeletedNode == False:
                for Node in range(0, len(options["Nodes"])):
                    try:
                        DistanceToNode = math.hypot(mousepos[0] - options["Nodes"][Node][0], mousepos[1] - options["Nodes"][Node][1])
                        if DistanceToNode < 5 and DeletedNode == False:
                            with open("Nodes.json", "w") as file:
                                options["Nodes"].pop(Node)
                                json.dump(options, file)
                                DeletedNode = True
                    except:
                        pass

            if pygame.mouse.get_pressed()[2] == False and DeletedNode == True:
                DeletedNode = False

    if ConnectNode == True:
        if pygame.mouse.get_pressed()[0] == True or pygame.mouse.get_pressed()[2] == True:
            for Node in range(0, len(options["Nodes"])):
                DistanceToNode = math.hypot(mousepos[0] - options["Nodes"][Node][0], mousepos[1] - options["Nodes"][Node][1])

                if pygame.mouse.get_pressed()[0] == True:
                    if DistanceToNode < 5:
                        SelectedNode = Node
                elif pygame.mouse.get_pressed()[2] == True and ConnectedNode == False:
                    if DistanceToNode < 5:

                        with open("Nodes.json", "w") as file:
                            options["NextNode"][SelectedNode].append(Node)
                            print(SelectedNode)
                            json.dump(options, file)
                            ConnectedNode = True

        if pygame.mouse.get_pressed()[2] == False and ConnectedNode == True:
            ConnectedNode = False

    if PathFinder == True:
        # pathfinder
        DistanceList = []
        DistPlyList = []
        IndexPlyList = []
        IndexList = []
        for Node in range(0, len(options["Nodes"])):
            if Node == StartNode:
                for Connection in range(0, len(options["NextNode"][Node])):
                    if len(DistanceList) == len(options["NextNode"][Node]):
                        IndexList.clear()
                        DistanceList.clear()
                    DistanceToNode = math.hypot(options["Nodes"][TargetNode][0] - options["Nodes"][options["NextNode"][Node][Connection]][0], options["Nodes"][TargetNode][1] - options["Nodes"][options["NextNode"][Node][Connection]][1])

                    DistanceList.append(DistanceToNode)
                    IndexList.append(options["NextNode"][Node][Connection])

        # find index to distance
        LowestDist = min(DistanceList)
        for Index in range(0, len(DistanceList)):
            if LowestDist == DistanceList[Index]:
                Index = IndexList[Index]

                if Index not in NodeList:
                    NodeList.append(Index)
                    StartNode = Index

        if len(NodeList[-1:]) > 0:
            try:
                if time.time() > Starttime + 0.43 and int(NodeList[-1]) != OrigTargetNode:


                    TargetNode = TargetNode - 1
                    Starttime = time.time()
                    NodeList.clear()
                    IndexList.clear()
                    DistanceList.clear()
                    StartNode = OrigStartnode

                if int(NodeList[-1]) == TargetNode:
                    TargetNode = OrigTargetNode
            except:
                pass




        # walking code

        for Node in range(0, len(options["Nodes"])):
            if len(DistPlyList) == len(options["Nodes"]):
                DistPlyList.clear()
                IndexPlyList.clear()
            DistfrmNodeToPly = math.hypot(lclx - options["Nodes"][Node][0], lcly - options["Nodes"][Node][1])
            DistPlyList.append(DistfrmNodeToPly)
            IndexPlyList.append(Node)

        # find closest node index
        closestnodetoplayer = min(DistPlyList)
        for Element in range(0, len(DistPlyList)):
            if DistPlyList[Element] == closestnodetoplayer:
                ClosestNode = Element

        # player dist to next node
        if Walk == True:
            try:
                plydistnextnode = math.hypot(lclx - options["Nodes"][NodeList[NodeToWalkto]][0], lcly - options["Nodes"][NodeList[NodeToWalkto]][1])
                if (lclx - options["Nodes"][NodeList[NodeToWalkto]][0]) < 3:
                    pm.write_int(ForceS, 1)
                    pm.write_int(ForceW, 0)
                else:
                    pm.write_int(ForceS, 0)
                    pm.write_int(ForceW, 1)

                if (lcly - options["Nodes"][NodeList[NodeToWalkto]][1]) < 3:
                    pm.write_int(ForceA, 1)
                    pm.write_int(ForceD, 0)
                else:
                    pm.write_int(ForceA, 0)
                    pm.write_int(ForceD, 1)

                if plydistnextnode < 13 and NodeChange < time.time():
                    NodeChange = time.time() + 1
                    NodeToWalkto = NodeToWalkto + 1


            except:
                pass





    for Node in range(0, len(NodeList)):
        try:
            pygame.draw.line(screen, LineColor, options["Nodes"][NodeList[Node]], options["Nodes"][NodeList[Node+1]])
        except:
            pass

    if DrawNodes == True:
        for Node in range(0, len(options["Nodes"])):
            if Node == SelectedNode:
                pygame.draw.circle(screen, SelecedNodeColor, options["Nodes"][Node], 5)

            else:
                pygame.draw.circle(screen, NodeColor, options["Nodes"][Node], 5)
                screen.blit(font.render(str(Node), True, NodeColor), options["Nodes"][Node])
    if DrawConnections == True:
        for Connection in range(0, len(options["NextNode"])):
            for Invidual in range(0, (len(options["NextNode"][Connection]))):
                try:
                    pygame.draw.line(screen, LineColor, options["Nodes"][options["NextNode"][Connection][0]], options["Nodes"][options["NextNode"][Connection][Invidual]])
                except:
                    pass

    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()