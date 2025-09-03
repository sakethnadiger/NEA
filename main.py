import pygame
import webbrowser
import os
from textwrap import fill
import datetime
from ui import *
from grid import Grid
from dfs import DFS
from bfs import BFS
from dijkstra import DIJKSTRA
from astar import *
from enum import *


def mainScreen():
    clock = pygame.time.Clock()
    
    class gridSize(Enum):
        SMALL = auto()
        MEDIUM = auto()
        LARGE = auto()
        
    class Speed(Enum):
        SLOW = auto()
        MEDIUM = auto()
        FAST = auto()
        
    class Insert(Enum):
        START = auto()
        END = auto()
        OBSTACLE = auto()
        GRASS = auto()
        WATER = auto()
        SNOW = auto()
        ROCK = auto()
        LAVA = auto()
        
    colourCodes = {
            Insert.GRASS : GRASSGREEN,
            Insert.WATER : WATERBLUE,
            Insert.SNOW : WHITE,
            Insert.ROCK : BROWN,
            Insert.LAVA : ORANGE,
            Insert.OBSTACLE : BLACK,
            Insert.START : GREEN,
            Insert.END : RED
    }
    
    insertCodes = {
            Insert.GRASS : 2,
            Insert.WATER : 5,
            Insert.SNOW : 10,
            Insert.ROCK : 20,
            Insert.LAVA : 50,
            Insert.OBSTACLE : "#",
    }
    
    gridSizeVals = {
        
        gridSize.SMALL : (27, 63, 20), 
        gridSize.MEDIUM : (9, 21, 60),
        gridSize.LARGE : (3, 7, 180)
            
    }

    # Need to change these values
    speedVals = {
        
        Speed.SLOW : 200, 
        Speed.MEDIUM : 30,
        Speed.FAST : 5
            
    }
    
    curGridSize = gridSize.SMALL
    curSpeed = Speed.FAST
    curInsert = Insert.OBSTACLE
    
    timeDelay = speedVals[curSpeed]
    
    # Initialise backend grid
    backendGrid = Grid(gridSizeVals[curGridSize][0], gridSizeVals[curGridSize][1])
    # Set a screen caption
    pygame.display.set_caption("Pathfinding Visualiser - Animate")
    
    # Initialise all elements here
    uiGrid = UIGrid(gridSizeVals[curGridSize][0], gridSizeVals[curGridSize][1], gridSizeVals[curGridSize][2])
    terminal = Label(1260, 70, BLACK, "", 15, WHITE)
    messageQueue = []
    headPointer = 0
    tailPointer = 0
    
    # top row button initialisation
    back = Button(70, 70, BLACK, "  BACK ", 20, WHITE, "back button")
    gridSizeCyclic = Cyclic(90, 70, PURPLE, 15, WHITE, {gridSize.SMALL : "   GRID SIZE   \n      SMALL", gridSize.MEDIUM : "   GRID SIZE   \n    MEDIUM", gridSize.LARGE: "   GRID SIZE   \n      LARGE"}, "grid size")
    speedCyclic = Cyclic(90, 70, PURPLE, 15, WHITE, {Speed.FAST: " ANIMATION   \n        FAST", Speed.SLOW : " ANIMATION   \n      SLOW", Speed.MEDIUM : " ANIMATION   \n    MEDIUM"}, "animation speed")
    dfsButton = Button(90, 70, BLUE, "      DEPTH\n       FIRST\n     SEARCH", 15, BLACK, "DFS button")
    bfsButton = Button(90, 70, BLUE, "   BREADTH\n       FIRST\n     SEARCH", 15, BLACK, "BFS button")
    dijkstraButton = Button(90, 70, BLUE, "  DIJKSTRA'S\n ALGORITHM", 15, BLACK, "dijkstra's button")
    astarCyclic = Cyclic(91, 30, BLUE, 13, BLACK, {"MANHATTAN" : "  MANHATTAN", "EUCLIDEAN" : "    EUCLIDEAN"}, "a star button")
    astarRun = Button(91, 30, BLUE, "      Run A*", 15, BLACK, "run a star button")
    mazeButton = Button(89, 70, BLUE, "  GENERATE\n      MAZE", 15, BLACK, "maze button")
    randomWeightButton = Button(85, 70, PURPLE, " RANDOMISE\n   WEIGHTS", 14, WHITE, "random weights")
    resetGridButton = Button(85, 30, RED, " RESET GRID", 15, BLACK, "reset grid")
    resetPathButton = Button(85, 30, RED, " RESET PATH", 15, BLACK, "reset path")
    
    
    # Weight buttons
    obstacleButton = Button(90, 30, BLACK, "   OBSTACLE", 15, WHITE, "obstacle")
    snowButton = Button(90, 30, WHITE, "  SNOW (10)", 15, BLACK, "snow")
    grassButton = Button(90, 30, GRASSGREEN, "   GRASS (2)", 15, WHITE, "green")
    rockButton = Button(90, 30, BROWN, "   ROCK (20)", 15, WHITE, "rock")
    waterButton = Button(90, 30, WATERBLUE, "   WATER (5)", 15, BLACK, "water")
    lavaButton = Button(90, 30, ORANGE, "    LAVA (50)", 15, BLACK, "lava")

    running = True
    frame_counter = 0
    while running:
        # Draw elements here
        screen.fill(GREY)
        
        # Draw grid and colour in start and end cells which are top left and bottom right by default - CHANGE THIS CODE WHEN USING GRID CLASS FROM BACKEND
        uiGrid.draw(screen, 10, 170)
        uiGrid.changeColour(backendGrid.getStart()[0], backendGrid.getStart()[1], GREEN)
        uiGrid.changeColour(backendGrid.getEnd()[0], backendGrid.getEnd()[1], RED)
        
        terminal.draw(screen, 10, 90, normalised=False)
        
        # The message string to be used in the terminal is constantly updated according to the message queue
        messageString = " "
        if messageQueue:
            for index in range(headPointer, tailPointer):
                messageString += f" [{index + 1}] " + messageQueue[index] + "\n"
            terminal.updateText(" " + messageString.strip())
        else:
            terminal.updateText(" Welcome to the animation screen.\n Add obstacles and weights by left clicking on the grid and remove them by right clicking. (Note: the last weight/obstacle you clicked will be the one added)\n View algorithm traversal in real time (Note: avoid clicking other buttons during animation as this will cause unresponsiveness) and see their associated metrics here.")
        
        # top row button drawing
        back.draw(screen, 10, 10, normalised=False, offset=20)
        gridSizeCyclic.draw(screen, 90, 10, normalised=False, offset=15)
        speedCyclic.draw(screen, 190, 10, normalised=False, offset=15)
        dfsButton.draw(screen, 290, 10, normalised=False, offset=6)
        bfsButton.draw(screen, 390, 10, normalised=False, offset=6)
        dijkstraButton.draw(screen, 490, 10, normalised=False, offset=15)
        astarCyclic.draw(screen, 590, 50, normalised=False, offset=6)
        astarRun.draw(screen, 590, 10, normalised=False, offset=5)
        mazeButton.draw(screen, 691, 10, normalised=False, offset=15)
        randomWeightButton.draw(screen, 1090, 10, normalised=False, offset=17)
        resetGridButton.draw(screen, 1185, 10, normalised=False, offset=5)
        resetPathButton.draw(screen, 1185, 50, normalised=False, offset=5)
        
        # Weight buttons
        obstacleButton.draw(screen, 790, 10, normalised=False, offset=5)
        snowButton.draw(screen, 790, 50, normalised=False, offset=5)
        grassButton.draw(screen, 890, 10, normalised=False, offset=5)
        rockButton.draw(screen, 890, 50, normalised=False, offset=5)
        waterButton.draw(screen, 990, 10, normalised=False, offset=5)
        lavaButton.draw(screen, 990, 50, normalised=False, offset=5)
        
        # Event handling
        for event in pygame.event.get():
            # Check for quit button clicked
            if event.type == pygame.QUIT:
                running = False
                return Screen.QUIT
            
            if uiGrid.eventOccurence(event)[0] and frame_counter > 10:
                clicked, button = uiGrid.eventOccurence(event)[1], uiGrid.eventOccurence(event)[2]
                if button == 3 and clicked != backendGrid.getStart() and clicked != backendGrid.getEnd():
                    uiGrid.changeColour(clicked[0], clicked[1], GREY)
                    backendGrid.insertValue(0, clicked[0], clicked[1])
                else:
                    
                    if clicked == backendGrid.getStart():
                        curInsert = Insert.START
                        continue
                    if clicked == backendGrid.getEnd():
                        curInsert = Insert.END
                        continue
                
                    if curInsert != Insert.START and curInsert != Insert.END:
                        uiGrid.changeColour(clicked[0], clicked[1], colourCodes[curInsert])
                        backendGrid.insertValue(insertCodes[curInsert], clicked[0], clicked[1])
                    else:
                        if curInsert == Insert.START:
                            # If a start changes position the original position needs to be made empty. The backend grid needs to be updated
                            currentStart = backendGrid.getStart()
                            uiGrid.changeColour(currentStart[0], currentStart[1], GREY)
                            backendGrid.changeStart(clicked[0], clicked[1])
                        
                        elif curInsert == Insert.END:
                            # If an end changes position the original position needs to be made empty. The backend grid needs to be updated
                            currentEnd = backendGrid.getEnd()
                            uiGrid.changeColour(currentEnd[0], currentEnd[1], GREY)
                            backendGrid.changeEnd(clicked[0], clicked[1])
                
            
            if back.eventOccurence(event):
                return Screen.ENTRYSCREEN
            
            if gridSizeCyclic.eventOccurence(event):
                gridSizeCyclic.reset()
                curGridSize = gridSizeCyclic.getState()
                uiGrid.changeDimensions(gridSizeVals[curGridSize][0], gridSizeVals[curGridSize][1], gridSizeVals[curGridSize][2])
                backendGrid = Grid(gridSizeVals[curGridSize][0], gridSizeVals[curGridSize][1])
            
            if speedCyclic.eventOccurence(event):
                speedCyclic.reset()
                curSpeed = speedCyclic.getState()
                timeDelay = speedVals[curSpeed]
                
            
            if dfsButton.eventOccurence(event):
                # Need to reset grid to only obstacles and weights
                uiGrid.backendToFrontendColour(backendGrid.getArray())
                print("DFS will now run.")
                dfsButton.reset()
                adjacencyList, start, end = backendGrid.getVariables()
                discovered, path, time = DFS(adjacencyList, start, end)
                if not path:
                    message = f"There is no possible path from the start cell to the end cell."
                    print(message)
                    if len(messageQueue) >= 3:
                        messageQueue.append(message)
                        headPointer += 1
                        tailPointer += 1
                    else:
                        messageQueue.append(message)
                        tailPointer += 1
                else:
                    startAnimation = datetime.datetime.now()
                    uiGrid.displayCells(discovered, path, timeDelay, start, end)
                    endAnimation = datetime.datetime.now()
                    timeDelta = endAnimation - startAnimation
                    message = f"DFS ran on computer in {time}ms and animated in {timeDelta.seconds}s, visited {len(discovered)} cells, shortest path {len(path)} cells."
                    print(message)
                    if len(messageQueue) >= 3:
                        messageQueue.append(message)
                        headPointer += 1
                        tailPointer += 1
                    else:
                        messageQueue.append(message)
                        tailPointer += 1
                    
            
            if bfsButton.eventOccurence(event):
                # Need to reset grid to only obstacles and weights
                uiGrid.backendToFrontendColour(backendGrid.getArray())
                print("BFS will now run.")
                bfsButton.reset()
                adjacencyList, start, end = backendGrid.getVariables()
                discovered, path, time = BFS(adjacencyList, start, end)
                if not path:
                    message = f"There is no possible path from the start cell to the end cell."
                    print(message)
                    if len(messageQueue) >= 3:
                        messageQueue.append(message)
                        headPointer += 1
                        tailPointer += 1
                    else:
                        messageQueue.append(message)
                        tailPointer += 1
                else:
                    startAnimation = datetime.datetime.now()
                    uiGrid.displayCells(discovered, path, timeDelay, start, end)
                    endAnimation = datetime.datetime.now()
                    timeDelta = endAnimation - startAnimation
                    message = f"BFS ran on computer in {time}ms and animated in {timeDelta.seconds}s, visited {len(discovered)} cells, shortest path {len(path)} cells."
                    print(message)
                    if len(messageQueue) >= 3:
                        messageQueue.append(message)
                        headPointer += 1
                        tailPointer += 1
                    else:
                        messageQueue.append(message)
                        tailPointer += 1
            
            if dijkstraButton.eventOccurence(event):
                # Need to reset grid to only obstacles and weights
                uiGrid.backendToFrontendColour(backendGrid.getArray())
                print("Dijkstra's algorithm will now run.")
                dijkstraButton.reset()
                adjacencyList, start, end = backendGrid.getVariables()
                cost, discovered, path, time = DIJKSTRA(adjacencyList, start, end)
                if not path:
                    message = f"There is no possible path from the start cell to the end cell."
                    print(message)
                    if len(messageQueue) >= 3:
                        messageQueue.append(message)
                        headPointer += 1
                        tailPointer += 1
                    else:
                        messageQueue.append(message)
                        tailPointer += 1
                else:
                    startAnimation = datetime.datetime.now()
                    uiGrid.displayCells(discovered, path, timeDelay, start, end)
                    endAnimation = datetime.datetime.now()
                    timeDelta = endAnimation - startAnimation
                    message = f"Dijkstra's algorithm ran on computer in {time}ms and animated in {timeDelta.seconds}s, visited {len(discovered)} cells, shortest path {len(path)} cells, with cost {cost}."
                    print(message)
                    if len(messageQueue) >= 3:
                        messageQueue.append(message)
                        headPointer += 1
                        tailPointer += 1
                    else:
                        messageQueue.append(message)
                        tailPointer += 1
            
            if astarCyclic.eventOccurence(event):
                astarCyclic.reset()
            
            if astarRun.eventOccurence(event):
                astarRun.reset()
                heuristic = astarCyclic.getState()
                print(f"A* {heuristic} algorithm will now run.")
                if heuristic == "EUCLIDEAN":
                    # Need to reset grid to only obstacles and weights
                    uiGrid.backendToFrontendColour(backendGrid.getArray())
                    adjacencyList, start, end = backendGrid.getVariables()
                    cost, discovered, path, time = ASTAR(adjacencyList, start, end, EUCLIDEAN)
                    if not path:
                        message = f"There is no possible path from the start cell to the end cell."
                        print(message)
                        if len(messageQueue) >= 3:
                            messageQueue.append(message)
                            headPointer += 1
                            tailPointer += 1
                        else:
                            messageQueue.append(message)
                            tailPointer += 1
                    else:
                        startAnimation = datetime.datetime.now()
                        uiGrid.displayCells(discovered, path, timeDelay, start, end)
                        endAnimation = datetime.datetime.now()
                        timeDelta = endAnimation - startAnimation
                        message = f"{heuristic} A* algorithm ran on computer in {time}ms and animated in {timeDelta.seconds}s, visited {len(discovered)} cells, shortest path {len(path)} cells, with cost {cost}."
                        print(message)
                        if len(messageQueue) >= 3:
                            messageQueue.append(message)
                            headPointer += 1
                            tailPointer += 1
                        else:
                            messageQueue.append(message)
                            tailPointer += 1
                        
                else:
                    # Need to reset grid to only obstacles and weights
                    uiGrid.backendToFrontendColour(backendGrid.getArray())
                    adjacencyList, start, end = backendGrid.getVariables()
                    cost, discovered, path, time = ASTAR(adjacencyList, start, end, MANHATTAN)
                    if not path:
                        message = f"There is no possible path from the start cell to the end cell."
                        print(message)
                        if len(messageQueue) >= 3:
                            messageQueue.append(message)
                            headPointer += 1
                            tailPointer += 1
                        else:
                            messageQueue.append(message)
                            tailPointer += 1
                    else:
                        startAnimation = datetime.datetime.now()
                        uiGrid.displayCells(discovered, path, timeDelay, start, end)
                        endAnimation = datetime.datetime.now()
                        timeDelta = endAnimation - startAnimation
                        message = f"{heuristic} A* algorithm ran on computer in {time}ms and animated in {timeDelta.seconds}s, visited {len(discovered)} cells, shortest path {len(path)} cells, with cost {cost}."
                        print(message)
                        if len(messageQueue) >= 3:
                            messageQueue.append(message)
                            headPointer += 1
                            tailPointer += 1
                        else:
                            messageQueue.append(message)
                            tailPointer += 1
                
            
            if mazeButton.eventOccurence(event):
                print("The maze will now be generated.")
                mazeButton.reset()
                # ERROR FIX - maze can not be generated on large grid
                if curGridSize == gridSize.LARGE:
                    message = "Maze can not be generated on a large grid."
                    if len(messageQueue) >= 3:
                        messageQueue.append(message)
                        headPointer += 1
                        tailPointer += 1
                    else:
                        messageQueue.append(message)
                        tailPointer += 1
                    continue
                # Before carving maze clear the whole grid.
                uiGrid.clearGrid()
                backendGrid.resetGrid()
                # Set current start and end cells to obstacle as they will be moved
                currentStart = backendGrid.getStart()
                uiGrid.changeColour(currentStart[0], currentStart[1], BLACK)
                currentEnd = backendGrid.getEnd()
                uiGrid.changeColour(currentEnd[0], currentEnd[1], BLACK)
                # Fill grid with obstacles for visualisation
                uiGrid.fillGrid()
                discovered, time = backendGrid.generateMaze()
                startAnimation = datetime.datetime.now()
                uiGrid.changeColour(backendGrid.getStart()[0], backendGrid.getStart()[1], GREEN)
                uiGrid.changeColour(backendGrid.getEnd()[0], backendGrid.getEnd()[1], RED)
                uiGrid.carveMaze(discovered, GREY, timeDelay, backendGrid.getStart(), backendGrid.getEnd())
                endAnimation = datetime.datetime.now()
                timeDelta = endAnimation - startAnimation
                message = f"DFS maze generated on computer in {time}ms and animated in {timeDelta.seconds}s, visited {len(discovered)} cells."
                if len(messageQueue) >= 3:
                    messageQueue.append(message)
                    headPointer += 1
                    tailPointer += 1
                else:
                    messageQueue.append(message)
                    tailPointer += 1
            
            if obstacleButton.eventOccurence(event):
                print("An obstacle can now be placed.")
                obstacleButton.reset()
                curInsert = Insert.OBSTACLE
                uiGrid.backendToFrontendColour(backendGrid.getArray())
            
            if snowButton.eventOccurence(event):
                print("A snow can now be placed.")
                snowButton.reset()
                curInsert = Insert.SNOW
                uiGrid.backendToFrontendColour(backendGrid.getArray())
                
            if grassButton.eventOccurence(event):
                print("A grass can now be placed.")
                grassButton.reset()
                curInsert = Insert.GRASS
                uiGrid.backendToFrontendColour(backendGrid.getArray())
            
            if rockButton.eventOccurence(event):
                print("A rock can now be placed.")
                rockButton.reset()
                curInsert = Insert.ROCK
                uiGrid.backendToFrontendColour(backendGrid.getArray())
            
            if waterButton.eventOccurence(event):
                print("A water can now be placed.")
                waterButton.reset()
                curInsert = Insert.WATER
                uiGrid.backendToFrontendColour(backendGrid.getArray())
            
            if lavaButton.eventOccurence(event):
                print("A lava can now be placed.")
                lavaButton.reset()
                curInsert = Insert.LAVA
                uiGrid.backendToFrontendColour(backendGrid.getArray())
            
            if randomWeightButton.eventOccurence(event):
                print("A randomly weighted grid will now be generated.")
                randomWeightButton.reset()
                backendGrid.randomWeightedGrid()
                uiGrid.backendToFrontendColour(backendGrid.getArray())
            
            if resetGridButton.eventOccurence(event):
                print("The grid will now be reset.")
                resetGridButton.reset()
                uiGrid.clearGrid()
                backendGrid.resetGrid()
            
            if resetPathButton.eventOccurence(event):
                print("The path will now be reset.")
                resetPathButton.reset()
                uiGrid.backendToFrontendColour(backendGrid.getArray())
                
        pygame.display.update()
        
        clock.tick(60)
        frame_counter += 1
        
        
    return

def astarScreen():
    clock = pygame.time.Clock()
    
    
    # Set a screen caption
    pygame.display.set_caption("Pathfinding Visualiser - Learn")
    
    
    
    # Initialise elements
    learnTitle = Label(1000, 70, GREY, "  Learn more about how the algorithms work", 50, BLACK)
    back = Button(70, 70, BLACK, "  BACK ", 20, WHITE, "back button")
    
    
    astarParagraph = Label(620, 300, BLACK, fill(astarText, 65), 25, BLUE)
    astarLink = Link(600, 40, BLACK, "Learn more about A* algorithm by clicking on this link.", 25, BLUE, "a star link")
    
    dfsTab = Button(308, 70, BLUE, "    Depth-First Search", 30, BLACK, autoSize=False,identification="dfs tab")
    bfsTab = Button(308, 70, BLUE, "   Breadth-First Search", 30, BLACK, autoSize=False, identification="bfs tab")
    dijkstraTab = Button(307, 70, BLUE, "   Dijkstra's Algorithm", 30, BLACK, autoSize=False, identification="dijkstra tab")
    astarTab = Label(307, 70, BLACK, "        A* Algorithm", 30, BLUE, autoSize=False)
    
    
    running = True
    while running:
        
        # Draw elements
        screen.fill(GREY)
        back.draw(screen, 10, 10, normalised=False, offset=20)
        learnTitle.draw(screen, 140, 10, normalised=False)
        dfsTab.draw(screen, 10, 90, normalised=False, offset=14)
        bfsTab.draw(screen, 327, 90, normalised=False, offset=14)
        dijkstraTab.draw(screen, 645, 90, normalised=False, offset=14)
        astarTab.draw(screen, 964, 90, normalised=False, offset=14)
        # Backdrop
        pygame.draw.rect(screen, BLACK, (10, 170, 1260, 540), 0, 12)
        
        astarParagraph.draw(screen, 540, 190, normalised=False)
        astarLink.draw(screen, 540, 550, normalised=False)
        
        screen.blit(pygame.transform.scale(astarImage, (500, 500)), (30, 190))
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return Screen.QUIT
            
            if back.eventOccurence(event):
                return Screen.ENTRYSCREEN
            
            if dfsTab.eventOccurence(event):
                return Screen.DFS_SCREEN
            
            if bfsTab.eventOccurence(event):
                return Screen.BFS_SCREEN
            
            if dijkstraTab.eventOccurence(event):
                return Screen.DIJKSTRA_SCREEN
            
            if astarLink.eventOccurence(event):
                webbrowser.open("https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#:~:text=Dijkstra's%20algorithm%20finds%20the%20shortest,path%20to%20the%20destination%20node.")
                astarLink.reset()
        
        
        pygame.display.update()
        clock.tick(60)
    
    return

def dijkstraScreen():
    clock = pygame.time.Clock()
    
    
    # Set a screen caption
    pygame.display.set_caption("Pathfinding Visualiser - Learn")
    
    
    
    # Initialise elements
    learnTitle = Label(1000, 70, GREY, "  Learn more about how the algorithms work", 50, BLACK)
    back = Button(70, 70, BLACK, "  BACK ", 20, WHITE, "back button")
    
    dijkstraParagraph = Label(620, 300, BLACK, fill(dijkstraText, 65), 25, BLUE)
    dijkstraLink = Link(680, 40, BLACK, "Learn more about Dijkstra's algorithm by clicking on this link.", 25, BLUE, "dijkstra link")
    
    dfsTab = Button(308, 70, BLUE, "    Depth-First Search", 30, BLACK, autoSize=False,identification="dfs tab")
    bfsTab = Button(308, 70, BLUE, "   Breadth-First Search", 30, BLACK, autoSize=False, identification="bfs tab")
    dijkstraTab = Label(307, 70, BLACK, "   Dijkstra's Algorithm", 30, BLUE, autoSize=False)
    astarTab = Button(307, 70, BLUE, "        A* Algorithm", 30, BLACK, autoSize=False, identification="a star tab")
    
    
    
    running = True
    while running:
        
        # Draw elements
        screen.fill(GREY)
        back.draw(screen, 10, 10, normalised=False, offset=20)
        learnTitle.draw(screen, 140, 10, normalised=False)
        dfsTab.draw(screen, 10, 90, normalised=False, offset=14)
        bfsTab.draw(screen, 327, 90, normalised=False, offset=14)
        dijkstraTab.draw(screen, 645, 90, normalised=False, offset=14)
        astarTab.draw(screen, 964, 90, normalised=False, offset=14)
        # Backdrop
        pygame.draw.rect(screen, BLACK, (10, 170, 1260, 540), 0, 12)
        
        dijkstraParagraph.draw(screen, 540, 190, normalised=False)
        dijkstraLink.draw(screen, 540, 520, normalised=False)
        
        screen.blit(pygame.transform.scale(dijkstraImage, (500, 500)), (30, 190))
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return Screen.QUIT
            
            if back.eventOccurence(event):
                return Screen.ENTRYSCREEN
            
            if dfsTab.eventOccurence(event):
                return Screen.DFS_SCREEN
            
            if bfsTab.eventOccurence(event):
                return Screen.BFS_SCREEN
            
            if astarTab.eventOccurence(event):
                return Screen.ASTAR_SCREEN
            
            if dijkstraLink.eventOccurence(event):
                webbrowser.open("https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#:~:text=Dijkstra's%20algorithm%20finds%20the%20shortest,path%20to%20the%20destination%20node.")
                dijkstraLink.reset()
        
        pygame.display.update()
        clock.tick(60)
    
    return

def bfsScreen():
    clock = pygame.time.Clock()
    
    
    # Set a screen caption
    pygame.display.set_caption("Pathfinding Visualiser - Learn")
    
    
    
    # Initialise elements
    learnTitle = Label(1000, 70, GREY, "  Learn more about how the algorithms work", 50, BLACK)
    back = Button(70, 70, BLACK, "  BACK ", 20, WHITE, "back button")
    bfsParagraph = Label(620, 300, BLACK, fill(bfsText, 65), 25, BLUE)
    dfsTab = Button(308, 70, BLUE, "    Depth-First Search", 30, BLACK, autoSize=False,identification="dfs tab")
    bfsTab = Label(308, 70, BLACK, "   Breadth-First Search", 30, BLUE, autoSize=False)
    dijkstraTab = Button(307, 70, BLUE, "   Dijkstra's Algorithm", 30, BLACK, autoSize=False, identification="dijkstra tab")
    astarTab = Button(307, 70, BLUE, "        A* Algorithm", 30, BLACK, autoSize=False, identification="a star tab")
    bfsLink = Link(530, 40, BLACK, "Learn more about BFS by clicking on this link.", 25, BLUE, "link for bfs", autoSize=False)
    
    
    
    running = True
    while running:
        
        # Draw elements
        screen.fill(GREY)
        back.draw(screen, 10, 10, normalised=False, offset=20)
        learnTitle.draw(screen, 140, 10, normalised=False)
        dfsTab.draw(screen, 10, 90, normalised=False, offset=14)
        bfsTab.draw(screen, 327, 90, normalised=False, offset=14)
        dijkstraTab.draw(screen, 645, 90, normalised=False, offset=14)
        astarTab.draw(screen, 964, 90, normalised=False, offset=14)
        # Backdrop
        pygame.draw.rect(screen, BLACK, (10, 170, 1260, 540), 0, 12)
        
        bfsParagraph.draw(screen, 540, 190, normalised=False)
        bfsLink.draw(screen, 540, 550, normalised=False)
        
        screen.blit(pygame.transform.scale(bfsImage, (500, 500)), (30, 190))
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return Screen.QUIT
            
            if back.eventOccurence(event):
                return Screen.ENTRYSCREEN
            
            if dfsTab.eventOccurence(event):
                return Screen.DFS_SCREEN
            
            if dijkstraTab.eventOccurence(event):
                return Screen.DIJKSTRA_SCREEN
            
            if astarTab.eventOccurence(event):
                return Screen.ASTAR_SCREEN
            
            if bfsLink.eventOccurence(event):
                webbrowser.open("https://en.wikipedia.org/wiki/Breadth-first_search")
                bfsLink.reset()
        
        pygame.display.update()
        clock.tick(60)
    
    return

def dfsScreen():
    clock = pygame.time.Clock()
    
    
    # Set a screen caption
    pygame.display.set_caption("Pathfinding Visualiser - Learn")
    
    
    
    # Initialise elements
    learnTitle = Label(1000, 70, GREY, "  Learn more about how the algorithms work", 50, BLACK)
    back = Button(70, 70, BLACK, "  BACK ", 20, WHITE, "back button")
    dfsParagraph = Label(1240, 300, BLACK, fill(dfsText, 100), 28, BLUE)
    dfsTab = Label(308, 70, BLACK, "    Depth-First Search", 30, BLUE, autoSize=False)
    bfsTab = Button(308, 70, BLUE, "   Breadth-First Search", 30, BLACK, autoSize=False, identification="bfs tab")
    dijkstraTab = Button(307, 70, BLUE, "   Dijkstra's Algorithm", 30, BLACK, autoSize=False, identification="dijkstra tab")
    astarTab = Button(307, 70, BLUE, "        A* Algorithm", 30, BLACK, autoSize=False, identification="a star tab")
    dfsLink = Link(530, 40, BLACK, "Learn more about DFS by clicking on this link.", 26, BLUE, "link for dfs", autoSize=False)
    
    
    
    running = True
    while running:
        
        # Draw elements
        screen.fill(GREY)
        back.draw(screen, 10, 10, normalised=False, offset=20)
        learnTitle.draw(screen, 140, 10, normalised=False)
        dfsTab.draw(screen, 10, 90, normalised=False, offset=14)
        bfsTab.draw(screen, 327, 90, normalised=False, offset=14)
        dijkstraTab.draw(screen, 645, 90, normalised=False, offset=14)
        astarTab.draw(screen, 964, 90, normalised=False, offset=14)
        # Backdrop
        pygame.draw.rect(screen, BLACK, (10, 170, 1260, 540), 0, 12)
        
        dfsParagraph.draw(screen, 15, 175, normalised=False)
        dfsLink.draw(screen, 722, 399, normalised=False)
        
        screen.blit(pygame.transform.scale(dfsImage, (400, 250)), (30, 450))
        screen.blit(pygame.transform.scale(mazeImage, (800, 250)), (460, 450))
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return Screen.QUIT
            
            if back.eventOccurence(event):
                return Screen.ENTRYSCREEN
            
            if bfsTab.eventOccurence(event):
                return Screen.BFS_SCREEN
            
            if dijkstraTab.eventOccurence(event):
                return Screen.DIJKSTRA_SCREEN
            
            if astarTab.eventOccurence(event):
                return Screen.ASTAR_SCREEN
            
            if dfsLink.eventOccurence(event):
                webbrowser.open("https://en.wikipedia.org/wiki/Depth-first_search")
                dfsLink.reset()
        
        pygame.display.update()
        clock.tick(60)
    
    return



def entryScreen():
    clock = pygame.time.Clock()
    
    # Set a screen caption
    pygame.display.set_caption("Pathfinding Visualiser - Welcome")
    
    # Initialise all elements here
    title = Label(0, 0, GREY, "PATHFINDING VISUALISER", 50, BLUE, autoSize=True)
    animate = Button(500, 70, BLUE, "                              ANIMATE\n     Watch the algorithms in action on a grid ", 25, BLACK, "animate")
    learn = Button(500, 70, BLUE, "                                LEARN\n      Learn about how the algorithms work ", 25, BLACK, "learn")
    
    
    running = True
    while running:

        # Draw elements here
        screen.fill(GREY)
        title.draw(screen, 0, 0.8)
        animate.draw(screen, 0, 0.12) 
        learn.draw(screen, 0, -0.12)
        
        # Event handling
        for event in pygame.event.get():
            # Check for quit button clicked
            if event.type == pygame.QUIT:
                running = False
                return Screen.QUIT
            
            if animate.eventOccurence(event):
                return Screen.MAINSCREEN
                
                
            if learn.eventOccurence(event):
                return Screen.DFS_SCREEN
        
                
        pygame.display.update()
        
        clock.tick(60)
        
    return

if __name__ == "__main__":
    
    # Unresizable screen dimensions
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Initialise images
    
    base = os.path.dirname(os.path.abspath(__file__))
    dfsImage = pygame.image.load(os.path.join(base, "assets", "dfs.png")).convert_alpha()
    mazeImage = pygame.image.load(os.path.join(base, "assets", "maze.png")).convert_alpha()
    bfsImage = pygame.image.load(os.path.join(base, "assets", "bfs.png")).convert_alpha()
    dijkstraImage = pygame.image.load(os.path.join(base, "assets", "dijkstra.png")).convert_alpha()
    astarImage = pygame.image.load(os.path.join(base, "assets", "astar.png")).convert_alpha()
    
    # get text from .txt files for each algorithm
    
    dfsText = open(os.path.join(base, "algorithmtext", "dfs.txt"), "r", encoding="utf-8").readline()
    bfsText = open(os.path.join(base, "algorithmtext", "bfs.txt"), "r", encoding="utf-8").readline()
    dijkstraText = open(os.path.join(base, "algorithmtext", "dijkstra.txt"), "r", encoding="utf-8").readline()
    astarText = open(os.path.join(base, "algorithmtext", "astar.txt"), "r", encoding="utf-8").readline()

    # Screen states
    class Screen(Enum):
        QUIT = auto()
        ENTRYSCREEN = auto()
        MAINSCREEN = auto()
        DFS_SCREEN = auto()
        BFS_SCREEN = auto()
        DIJKSTRA_SCREEN = auto()
        ASTAR_SCREEN = auto()
        
    pygame.init()
    
    
    # Program starts with entry screen
    currentScreen = Screen.ENTRYSCREEN
    while currentScreen != Screen.QUIT:
        match currentScreen:
            case Screen.ENTRYSCREEN:
                currentScreen = entryScreen()
            case Screen.MAINSCREEN:
                currentScreen = mainScreen()
            case Screen.DFS_SCREEN:
                currentScreen = dfsScreen()
            case Screen.BFS_SCREEN:
                currentScreen = bfsScreen()
            case Screen.DIJKSTRA_SCREEN:
                currentScreen = dijkstraScreen()
            case Screen.ASTAR_SCREEN:
                currentScreen = astarScreen()
                
        

    # Quit Pygame if user ever presses quit button     
    pygame.quit()