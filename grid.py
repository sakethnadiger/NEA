import random
import numpy as np
import time

# backend grid class --iteration 1--
class Grid:
    # format ROW, COL
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.weightChoices = [0, 2, 5, 10, 20, 50, "#"]
        # list comprehension creating gridArray with parameter dimensions
        self.gridArray = [[0 for col in range(self.columns)] for row in range(self.rows)]
        
        # place start and end cells in top left and bottom right cells respectively
        self.gridArray[0][0], self.gridArray[-1][-1] = "S", "E"
    
    
    def getStart(self):
        npArray = np.array(self.gridArray)
        startPos = tuple(np.argwhere(npArray == "S")[0])
        return (startPos[1], startPos[0])
    
    def getEnd(self):
        npArray = np.array(self.gridArray)
        endPos = tuple(np.argwhere(npArray == "E")[0])
        return (endPos[1], endPos[0])
    
    # method to insert weight or obstacle into array
    def insertValue(self, cellValue, x, y):
        if self.gridArray[y][x] not in ["S", "E"] and cellValue in self.weightChoices:
            self.gridArray[y][x] = cellValue
    
    def changeStart(self, x, y):
        curStart = self.getStart()
        self.gridArray[y][x] = "S"
        self.gridArray[curStart[1]][curStart[0]] = 0
        
    def changeEnd(self, x, y):
        curEnd = self.getEnd()
        self.gridArray[y][x] = "E"
        self.gridArray[curEnd[1]][curEnd[0]] = 0
    
    # generate a randomly weighted grid
    def randomWeightedGrid(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.gridArray[i][j] not in ["S", "E"]:
                    self.gridArray[i][j] = random.choice(self.weightChoices)

    
    def getArray(self):
        return self.gridArray
    
    # currently only created a method for resetting grid.
    # option for resetting path will come after algorithm implementation
    def resetGrid(self):
        self.gridArray = [[0 for col in range(self.columns)] for row in range(self.rows)]
        self.gridArray[0][0], self.gridArray[-1][-1] = "S", "E"
    
    # generate adjacency list - NEW: ADDED A NEW PARAMETER FOR A SPECIALISED MAZE GENERATION ADJACENCY LIST
    def adjacencyList(self, maze=False):
            
        def validEdges(neighbours):
            edges = {}
            for n in neighbours:
                val = self.gridArray[n[1]][n[0]]
                if val != "#":
                    if val == 0 or val == "S" or val == "E":
                        # weight should be 1, not 0 or "S" or "E"
                        edges[n] = 1
                    else:
                        edges[n] = val
            return edges
        
        adjacency = {}
        if maze:
            if self.columns % 2 == 0 or self.rows % 2 == 0: return False
            for y, row in enumerate(self.gridArray):
                for x, val in enumerate(row):
                    if val != "#":
                        # PRECONDITION - there will be an odd number of rows and columns only
                        # relative top left
                        if y == 1 and x == 1:
                            neighbours = [(x+2, y), (x, y+2)]
                        
                        # relative top right
                        elif y == 1 and x == self.columns - 2:
                            neighbours = [(x-2, y), (x, y+2)]
                        
                        # relative top row
                        elif y == 1:
                            neighbours = [(x-2, y), (x+2, y), (x, y+2)]
                        
                        # relative bottom left
                        elif y == self.rows - 2 and x == 1:
                            neighbours = [(x+2, y), (x, y-2)]
                        
                        # relative bottom right
                        elif y == self.rows - 2 and x == self.columns - 2:
                            neighbours = [(x-2, y), (x, y-2)]
                        
                        # relative bottom row
                        elif y == self.rows - 2:
                            neighbours = [(x-2, y), (x+2, y), (x, y-2)]
                        
                        # relative left column
                        elif x == 1:
                            neighbours = [(x+2, y), (x, y-2), (x, y+2)]
                        
                        # relative right column
                        elif x == self.columns - 2:
                            neighbours = [(x-2, y),(x, y-2), (x, y+2)]
                        
                        # everything else - don't need to check for odd or not because it will be an obstacle anyway
                        else:
                            neighbours = [(x-2, y), (x+2, y), (x, y-2), (x, y+2)]
                        
                        adjacency[(x, y)] = validEdges(neighbours)
                        
                        
        else:
            for y, row in enumerate(self.gridArray):
                for x, val in enumerate(row):
                    if val != "#":
                        # firstly check boundary conditions
                        # top left - add right and below
                        if x == 0 and y == 0:
                            neighbours = [(x+1, y), (x, y+1)]
                            
                        # top right - add left and below
                        elif x == len(row)-1 and y == 0:
                            neighbours = [(x-1, y), (x, y+1)]
                            
                        # top row - add left, right and below
                        elif y == 0:
                            neighbours = [(x-1, y), (x+1, y), (x, y+1)]
                            
                        # bottom left - add right and above
                        elif x == 0 and y == len(self.gridArray) - 1:
                            neighbours = [(x+1, y), (x, y-1)]
                        
                        # bottom right - add left and above
                        elif x == len(row) - 1 and y == len(self.gridArray) - 1:
                            neighbours = [(x-1, y), (x, y-1)]
                        
                        # bottom row - add left, right and above
                        elif y == len(self.gridArray) - 1:
                            neighbours = [(x-1, y), (x+1, y), (x, y-1)]
                        
                        # left column - add right, above and below
                        elif x == 0:
                            neighbours = [(x+1, y), (x, y-1), (x, y+1)]
                        
                        # right column - add left, above and below
                        elif x == len(row) - 1:
                            neighbours = [(x-1, y),(x, y-1), (x, y+1)]
                        
                        # normal conditions - left, right, above, below
                        else:
                            neighbours = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
                        
                        # add map of weighted neighbours to adjacency list
                        adjacency[(x, y)] = validEdges(neighbours)
        
        return adjacency
    
    # used for maze generation
    def createWalls(self):
        for y in range(self.rows):
            for x in range(self.columns):
                if y % 2 == 0 or x % 2 == 0:
                    self.insertValue("#", x, y)
        
        self.changeStart(1, 1)
        self.changeEnd(self.columns - 2, self.rows - 2)
        self.insertValue("#", 0, 0)
        self.insertValue("#", self.columns - 1, self.rows - 1)
        return self.adjacencyList(maze=True)
    
    # DFS for maze generation - CHANGE : ADDED RUNTIME MEASURING TO MAZE GENERATION
    def generateMaze(self):
        startTime = time.perf_counter()
        A = self.createWalls()
        start = self.getStart()
        
        def validNeighbours(A, node, visited):
            neighbours =  A[node]
            valids = []
            for n in neighbours:
                if n not in visited:
                    valids.append(n)
            
            return valids
        
        visited = set()
        visited.add(start)
        uiDiscovered = []
        stack = [start]
        while stack:
            cur = stack.pop()
            neighbours = validNeighbours(A, cur, visited)
            if len(neighbours) > 0:
                stack.append(cur)
                new = random.choice(neighbours)
                obstacle = ((cur[0] + new[0])//2, (cur[1] + new[1])//2)
                self.insertValue(0, obstacle[0], obstacle[1])
                uiDiscovered.append(obstacle)
                uiDiscovered.append(new)
                visited.add(new)
                stack.append(new)
        
        endTime = time.perf_counter()
        runtime = endTime - startTime
        return uiDiscovered, round(runtime, 4)
    
    # mainly to output a clearly contrasted grid for a generated maze
    def outputGrid(self):
        newArray = [[0 for col in range(self.columns)] for row in range(self.rows)]
        for y, row in enumerate(self.gridArray):
            for x, val in enumerate(row):
                if val == 0:
                    newArray[y][x] = "."
                else:
                    newArray[y][x] = val
        for i in newArray:
            print(" ".join(str(j) for j in i))
    
    # displays grid with path without amending gridArray
    def displayPath(self, path):
        tempArray = [x[:] for x in self.gridArray]
        for y, row in enumerate(self.gridArray):
            for x, val in enumerate(row):
                if val == 0:
                    tempArray[y][x] = "."
                else:
                    tempArray[y][x] = val
                if (x, y) in path and val not in ["S", "E"]:
                    tempArray[y][x] = "@"
                
        
        for i in tempArray:
            print(" ".join(str(j) for j in i))
    
    def getVariables(self):
        return self.adjacencyList(), self.getStart(), self.getEnd()
