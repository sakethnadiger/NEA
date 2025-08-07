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

#testgrid = UIGrid(3, 7, 180)

s = {"small": "GRID SIZE\nSMALL", "medium": "GRID SIZE\nMEDIUM", "large": "GRID SIZE\nLARGE"}

c = Cyclic(200, 100, BLUE, 30, WHITE, s, "Cyclic test button", autoSize=True)

running = True
while running:

    # Set background colour to grey
    entryScreen.fill((34, 40, 49))
    
    c.draw(entryScreen, 0, 0)
    
    #testgrid.draw(entryScreen, 10, 170)
    
    # Event handling
    for event in pygame.event.get():
        # Check for quit button clicked
        if event.type == pygame.QUIT:
            running = False
        
        if c.eventOccurence(event):
            cur_state = c.getState()
            print(f"Current state of {c.getId()} is {c.getState()}")
            c.reset()
        
        # if testgrid.eventOccurence(event):
        #     clickedCell = testgrid.clickedCell()
        #     print(f"{clickedCell} was clicked.")
        #     if clickedCell == (0,0):
        #         testgrid.changeColour(0,0, WHITE)
        #     testgrid.reset()
            
    pygame.display.update()
    
    clock.tick(FPS)
    
pygame.quit()