import pygame

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Define colours - will add to this
BLACK = pygame.Color("#000000")
GREY = pygame.Color("#222831")
BLUE = pygame.Color("#00ADB5")
LIGHTBLUE = pygame.Color("#33C3CA")
WHITE = pygame.Color("#EEEEEE")
GREEN = pygame.Color("#06D001")
RED = pygame.Color("#F93827")
GRASSGREEN = pygame.Color("#386641")
BROWN = pygame.Color("#7B4019")
WATERBLUE = pygame.Color("#4DA8DA")
ORANGE = pygame.Color("#FF7601")
PURPLE = pygame.Color("#7E5CAD")

def normalisedToScreen(input_x, input_y, obj_width, obj_height):
    if input_x < -1: input_x = -1
    if input_y < -1: input_y = -1
    if input_x > 1: input_x = 1
    if input_y > 1: input_y = 1
    width, height = SCREEN_WIDTH, SCREEN_HEIGHT
    screen_centre_x = width // 2
    screen_centre_y = height // 2
    screen_x = int(screen_centre_x * (1 + input_x))
    screen_y = int(screen_centre_y * (1 - input_y))
    true_x = screen_x - obj_width // 2
    true_y = screen_y - obj_height // 2
    return true_x, true_y

class Label():
    def __init__(self, width, height, colour, text, textSize, textColour, autoSize=False):
        self.autoSize = autoSize
        self.width = width
        self.height = height
        self.colour = colour
        self.text = text
        self.textSize = textSize
        self.textColour = textColour
        self.font = pygame.font.SysFont("ebrima", self.textSize * 4)
    
    # (x, y) is the position that the user wants to place the CENTRE of the label
    def draw(self, surface, x, y, normalised=True, offset=0):
        lines = self.text.split("\n")
        textImgs = []
        imgWidths = []
        imgHeights = []
        for line in lines:
            render = self.font.render(line, True, self.textColour)
            scaled_render = pygame.transform.smoothscale(render, (render.get_width() // 4, render.get_height() // 4))
            textImgs.append(scaled_render)
            imgWidths.append(scaled_render.get_width())
            imgHeights.append(scaled_render.get_height())
        # Auto set the width and height of the box around the text. May need to add padding to this.
        if self.autoSize:
            self.width = max(imgWidths)
            self.height = sum(imgHeights)
        if normalised:
            true_x, true_y = normalisedToScreen(x, y, self.width, self.height)
        else:
            true_x, true_y = x, y
        self.box = pygame.Rect(true_x, true_y, self.width, self.height)
        pygame.draw.rect(surface, self.colour, self.box, 0, 12)
        
        heightCounter = true_y + offset
        for l, line in enumerate(textImgs):
            height = imgHeights[l]
            surface.blit(line, (true_x, heightCounter))
            heightCounter += height
    
    def updateText(self, newText):
        self.text = newText

class Button(Label):
    def __init__(self, width, height, colour, text, textSize, textColour, identification, autoSize=False):
        super().__init__(width, height, colour, text, textSize, textColour, autoSize=autoSize)
        self.identification = identification
        self.originalColour = colour
        self.pressed = False
        
    def getId(self):
        return self.identification
    
    def draw(self, surface, x, y, normalised=True, offset=0):
        lines = self.text.split("\n")
        textImgs = []
        imgWidths = []
        imgHeights = []
        for line in lines:
            render = self.font.render(line, True, self.textColour)
            scaled_render = pygame.transform.smoothscale(render, (render.get_width() // 4, render.get_height() // 4))
            textImgs.append(scaled_render)
            imgWidths.append(scaled_render.get_width())
            imgHeights.append(scaled_render.get_height())
        # Auto set the width and height of the box around the text. May need to add padding to this.
        if self.autoSize:
            self.width = max(imgWidths)
            self.height = sum(imgHeights)
        if normalised:
            true_x, true_y = normalisedToScreen(x, y, self.width, self.height)
        else:
            true_x, true_y = x, y
        self.box = pygame.Rect(true_x, true_y, self.width, self.height)
        pygame.draw.rect(surface, self.colour, self.box, 0, 12)
        heightCounter = true_y + offset
        for l, line in enumerate(textImgs):
            height = imgHeights[l]
            surface.blit(line, (true_x, heightCounter))
            heightCounter += height
    
    # handle a click and hover
    def eventOccurence(self, event):
        self.colour = self.originalColour
        mousePos = pygame.mouse.get_pos()
        if self.box.collidepoint(mousePos):
            self.colour = LIGHTBLUE
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.pressed:
                self.pressed = True
                return True
        
    # Call this right after checking for click
    def reset(self):
        self.pressed = False
    
    def updateText(self, newText):
        self.text = newText

class Cyclic():
    def __init__(self, width, height, colour, textSize, textColour, states: dict, identification, autoSize=False):
        self.autoSize = autoSize
        self.width = width
        self.height = height
        self.colour = colour
        self.textSize = textSize
        self.textColour = textColour
        self.identification = identification
        self.pressed = False
        self.originalColour = colour
        self.font = pygame.font.SysFont("ebrima", self.textSize * 4)

        self.states = states
        self.stateCounter = 0
        self.stateList = []
        for state in self.states:
            self.stateList.append(state)
            
    def getId(self):
        return self.identification
        
    # call this right after eventOccurence to obtain current state but before reset
    def getState(self):
        return self.stateList[self.stateCounter]
        
    def draw(self, surface, x, y, normalised=True, offset=0):
        
        curState = self.stateList[self.stateCounter]
        self.text = self.states[curState]
        # Render the text as an image
        lines = self.text.split("\n")
        textImgs = []
        imgWidths = []
        imgHeights = []
        for line in lines:
            render = self.font.render(line, True, self.textColour)
            scaled_render = pygame.transform.smoothscale(render, (render.get_width() // 4, render.get_height() // 4))
            textImgs.append(scaled_render)
            imgWidths.append(scaled_render.get_width())
            imgHeights.append(scaled_render.get_height())
        # Auto set the width and height of the box around the text. May need to add padding to this.
        if self.autoSize:
            self.width = max(imgWidths)
            self.height = sum(imgHeights)
        if normalised:
            true_x, true_y = normalisedToScreen(x, y, self.width, self.height)
        else:
            true_x, true_y = x, y
        self.box = pygame.Rect(true_x, true_y, self.width, self.height)
        pygame.draw.rect(surface, self.colour, self.box, 0, 12)
        heightCounter = true_y + offset
        for l, line in enumerate(textImgs):
            height = imgHeights[l]
            surface.blit(line, (true_x, heightCounter))
            heightCounter += height
            
    # handle a click and hover
    def eventOccurence(self, event):
        self.colour = self.originalColour
        mousePos = pygame.mouse.get_pos()
        if self.box.collidepoint(mousePos):
            self.colour = LIGHTBLUE
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.pressed:
                self.pressed = True
                return True
                
    # Call this right after checking for click
    def reset(self):
        self.stateCounter = (self.stateCounter + 1) % len(self.stateList)
        self.pressed = False
    
    def updateText(self, newText):
        self.text = newText        
                
                
            
class Cell():
    def __init__(self, sideLength, colour, identification):
        self.sideLength = sideLength
        self.colour = colour
        self.identification = identification
        self.pressed = False
    
    def draw(self, surface, x, y):
        self.surface = surface
        self.x = x
        self.y = y
        self.box = pygame.Rect(x, y, self.sideLength, self.sideLength)
        self.border = pygame.Rect(x, y, self.sideLength, self.sideLength)
        pygame.draw.rect(surface, self.colour, self.box)
        pygame.draw.rect(surface, BLUE, self.border, 1)
        
    
    # handle a click
    def eventOccurence(self, event):
        mousePos = pygame.mouse.get_pos()
        if self.box.collidepoint(mousePos):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.pressed:
                self.pressed = True
                return True
    
    def isClicked(self):
        if self.pressed:
            return True
        return False
    
    def getId(self):
        return self.identification
    
    # Call this right after checking for click
    def reset(self):
        self.pressed = False
    
    def changeColour(self, newColour):
        self.colour = newColour
        self.draw(self.surface, self.x, self.y)
        
class UIGrid():
    def __init__(self, rows, columns, cellSize):
        self.rows = rows
        self.columns = columns
        self.cellSize = cellSize
        # create an array of Cell objects
        self.grid = []
        for i in range(self.rows):
            row = []
            for j in range(self.columns):
                cell = Cell(cellSize, GREY, (j, i))
                row.append(cell)
            self.grid.append(row)
        
    def draw(self, surface, x, y):
        for i in range(self.rows):
            for j in range(self.columns):
                cell = self.grid[i][j]
                cell.draw(surface, x + self.cellSize*j, y + self.cellSize*i)
    
    def eventOccurence(self, event):
        for row in self.grid:
            for cell in row:
                if cell.eventOccurence(event):
                    return True
    
    def clickedCell(self):
        for row in self.grid:
            for cell in row:
                if cell.isClicked():
                    return cell.getId()
    
    def reset(self):
        for row in self.grid:
            for cell in row:
                cell.reset()
    
    def changeColour(self, x, y, colour):
        cell = self.grid[y][x]
        cell.changeColour(colour)
    
    def changeDimensions(self, newRows, newCols, newSize):
        self.rows = newRows
        self.columns = newCols
        self.cellSize = newSize
        self.grid = []
        for i in range(self.rows):
            row = []
            for j in range(self.columns):
                cell = Cell(self.cellSize, GREY, (j, i))
                row.append(cell)
            self.grid.append(row)
        
        
