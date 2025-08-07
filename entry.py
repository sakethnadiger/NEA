import pygame
from ui import *
from grid import Grid

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

pygame.init()
clock = pygame.time.Clock()

# Not resizable
entryScreen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))



# Set a screen caption
pygame.display.set_caption("Pathfinding Visualiser")

# PRESETS
# SMALL : 27 rows, 63 columns, 20 px
# MEDIUM : 9 rows, 21 columns, 60 px
# LARGE : 3 rows, 7 columns, 180 px

testgrid = UIGrid(3, 7, 180)

running = True
while running:

    # Set background colour to grey
    entryScreen.fill((34, 40, 49))

    testgrid.draw(entryScreen, 10, 170)
    
    # Event handling
    for event in pygame.event.get():
        # Check for quit button clicked
        if event.type == pygame.QUIT:
            running = False
        
        
        if testgrid.eventOccurence(event):
            clickedCell = testgrid.clickedCell()
            print(f"{clickedCell} was clicked.")
            if clickedCell == (0,0):
                testgrid.changeColour(0,0, WHITE)
            testgrid.reset()
            
    pygame.display.update()
    
    clock.tick(FPS)
    
pygame.quit()