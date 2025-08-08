import pygame
from ui import *
from grid import Grid
from enum import *

# Not resizable
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Screen(Enum):
    QUIT = auto()
    ENTRYSCREEN = auto()
    MAINSCREEN = auto()
    LEARNSCREEN = auto()
    
    
pygame.init()

# PRESETS
# Position (10, 170)
# SMALL : 27 rows, 63 columns, 20 px
# MEDIUM : 9 rows, 21 columns, 60 px
# LARGE : 3 rows, 7 columns, 180 px

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
    
    gridSizeVals = {
        
        gridSize.SMALL : (27, 63, 20), 
        gridSize.MEDIUM : (9, 21, 60),
        gridSize.LARGE : (3, 7, 180)
            
    }

    # Need to change these values
    speedVals = {
        
        Speed.SLOW : 1000, 
        Speed.MEDIUM : 100,
        Speed.FAST : 10
            
    }
    
    curGridSize = gridSize.SMALL
    curSpeed = Speed.FAST
    
    # Set a screen caption
    pygame.display.set_caption("Pathfinding Visualiser - Animate")
    
    # Initialise all elements here
    uiGrid = UIGrid(gridSizeVals[curGridSize][0], gridSizeVals[curGridSize][1], gridSizeVals[curGridSize][2])
    terminal = Label(1260, 70, BLACK, "", 10, WHITE)
    
    # top row button initialisation
    back = Button(70, 70, BLACK, "  BACK ", 20, WHITE, "back button")
    gridSizeCyclic = Cyclic(90, 70, BLUE, 15, BLACK, {gridSize.SMALL : "   GRID SIZE   \n      SMALL", gridSize.MEDIUM : "   GRID SIZE   \n    MEDIUM", gridSize.LARGE: "   GRID SIZE   \n      LARGE"}, "grid size")
    speedCyclic = Cyclic(90, 70, BLUE, 15, BLACK, {Speed.SLOW : " ANIMATION   \n      SLOW", Speed.MEDIUM : " ANIMATION   \n    MEDIUM", Speed.FAST: " ANIMATION   \n        FAST"}, "animation speed")
    dfsButton = Button(90, 70, BLUE, "      DEPTH\n       FIRST\n     SEARCH", 15, BLACK, "DFS button")
    bfsButton = Button(90, 70, BLUE, "   BREADTH\n       FIRST\n     SEARCH", 15, BLACK, "BFS button")
    dijkstraButton = Button(90, 70, BLUE, "  DIJKSTRA'S\n ALGORITHM", 15, BLACK, "dijkstra's button")
    astarCyclic = Cyclic(91, 70, BLUE, 15, BLACK, {"EUCLIDEAN" : "          A*\n  EUCLIDEAN", "MANHATTAN" : "          A*\nMANHATTAN"}, "a star button")
    mazeButton = Button(89, 70, BLUE, "  GENERATE\n      MAZE", 15, BLACK, "maze button")
    randomWeightButton = Button(85, 70, PURPLE, "RANDOMISE\n   WEIGHTS", 15, WHITE, "random weights")
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
    while running:

        # Draw elements here
        screen.fill((34, 40, 49))
        
        # Draw grid and colour in start and end cells which are top left and bottom right by default - CHANGE THIS CODE WHEN USING GRID CLASS FROM BACKEND
        uiGrid.draw(screen, 10, 170)
        uiGrid.changeColour(0, 0, GREEN)
        uiGrid.changeColour(gridSizeVals[curGridSize][1] - 1, gridSizeVals[curGridSize][0] - 1, RED)
        
        terminal.draw(screen, 10, 90, normalised=False)
        
        # top row button drawing
        back.draw(screen, 10, 10, normalised=False, offset=20)
        gridSizeCyclic.draw(screen, 90, 10, normalised=False, offset=15)
        speedCyclic.draw(screen, 190, 10, normalised=False, offset=15)
        dfsButton.draw(screen, 290, 10, normalised=False, offset=6)
        bfsButton.draw(screen, 390, 10, normalised=False, offset=6)
        dijkstraButton.draw(screen, 490, 10, normalised=False, offset=15)
        astarCyclic.draw(screen, 590, 10, normalised=False, offset=15)
        mazeButton.draw(screen, 691, 10, normalised=False, offset=15)
        randomWeightButton.draw(screen, 1090, 10, normalised=False, offset=15)
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
            
            if uiGrid.eventOccurence(event):
                print(f"{uiGrid.clickedCell()} was clicked.")
                uiGrid.reset()
            
            if back.eventOccurence(event):
                return Screen.ENTRYSCREEN
            
            if gridSizeCyclic.eventOccurence(event):
                gridSizeCyclic.reset()
                curGridSize = gridSizeCyclic.getState()
                uiGrid.changeDimensions(gridSizeVals[curGridSize][0], gridSizeVals[curGridSize][1], gridSizeVals[curGridSize][2])
            
            if speedCyclic.eventOccurence(event):
                speedCyclic.reset()
                curSpeed = speedCyclic.getState()
                print(speedVals[curSpeed])
            
            if dfsButton.eventOccurence(event):
                print("DFS will now be run.")
                dfsButton.reset()
            
            if bfsButton.eventOccurence(event):
                print("BFS will now be run.")
                bfsButton.reset()
            
            if dijkstraButton.eventOccurence(event):
                print("Dijkstra's algorithm will now be run.")
                dijkstraButton.reset()
            
            if astarCyclic.eventOccurence(event):
                astarCyclic.reset()
                print(f"A* {astarCyclic.getState()} algorithm will now be run.")
            
            if mazeButton.eventOccurence(event):
                print("The maze will now be generated.")
                mazeButton.reset()
            
            if obstacleButton.eventOccurence(event):
                print("An obstacle can now be placed.")
                obstacleButton.reset()
            
            if snowButton.eventOccurence(event):
                print("A snow can now be placed.")
                snowButton.reset()
                
            if grassButton.eventOccurence(event):
                print("A grass can now be placed.")
                grassButton.reset()
            
            if rockButton.eventOccurence(event):
                print("A rock can now be placed.")
                rockButton.reset()
            
            if waterButton.eventOccurence(event):
                print("A water can now be placed.")
                waterButton.reset()
            
            if lavaButton.eventOccurence(event):
                print("A lava can now be placed.")
                lavaButton.reset()
            
            if randomWeightButton.eventOccurence(event):
                print("A randomly weighted grid will now be generated.")
                randomWeightButton.reset()
            
            if resetGridButton.eventOccurence(event):
                print("The grid will now be reset.")
                resetGridButton.reset()
            
            if resetPathButton.eventOccurence(event):
                print("The path will now be reset.")
                resetPathButton.reset()
                
        pygame.display.update()
        
        clock.tick(60)
        
    return
    
def learnScreen():
    pass

def entryScreen():
    clock = pygame.time.Clock()

    # Set a screen caption
    pygame.display.set_caption("Pathfinding Visualiser - Welcome")
    
    # Initialise all elements here
    title = Label(0, 0, GREY, "PATHFINDING VISUALISER", 50, BLUE, autoSize=True)
    animate = Button(0, 0, BLUE, "                          ANIMATE\n Watch the algorithms in action on a grid ", 25, GREY, "animate", autoSize=True)
    learn = Button(0, 0, BLUE, "                          LEARN\n Learn about how the algorithms work ", 25, GREY, "animate", autoSize=True)
    
    running = True
    while running:

        # Draw elements here
        screen.fill((34, 40, 49))
        title.draw(screen, 0, 0.8)
        animate.draw(screen, 0, 0.1) 
        learn.draw(screen, 0, -0.1)
        
        # Event handling
        for event in pygame.event.get():
            # Check for quit button clicked
            if event.type == pygame.QUIT:
                running = False
                return Screen.QUIT
            
            if animate.eventOccurence(event):
                return Screen.MAINSCREEN
                
                
            if learn.eventOccurence(event):
                learnScreen()
                learn.reset()
        
                
        pygame.display.update()
        
        clock.tick(60)
        
    return
    
# Program starts with entry screen
currentScreen = Screen.ENTRYSCREEN
while currentScreen != Screen.QUIT:
    match currentScreen:
        case Screen.ENTRYSCREEN:
            currentScreen = entryScreen()
        case Screen.MAINSCREEN:
            currentScreen = mainScreen()
        case Screen.LEARNSCREEN:
            currentScreen = learnScreen()
        


pygame.quit()