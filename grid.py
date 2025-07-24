import random

# backend grid class --iteration 1--
class Grid:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.weightChoices = [0, 2, 5, 10, 20, 50, "#"]
        # list comprehension creating gridArray with parameter dimensions
        self.gridArray = [[0 for col in range(columns)] for row in range(rows)]
        
        # place start and end cells in top left and bottom right cells respectively
        self.gridArray[0][0], self.gridArray[-1][-1] = "S", "E"
        
            
    # method to insert weight or obstacle into array
    def insertValue(self, cellValue, rowIndex, colIndex):
        if self.gridArray[rowIndex][colIndex] not in ["S", "E"] and cellValue in self.weightChoices:
            self.gridArray[rowIndex][colIndex] = cellValue
    
    # generate a randomly weighted grid
    def randomWeightedGrid(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.gridArray[i][j] not in ["S", "E"]:
                    self.gridArray[i][j] = random.choice(self.weightChoices)
    
    # output grid array on terminal
    def outputGrid(self):
        for i in self.gridArray:
            print(" ".join(str(j) for j in i))
    
    # currently only created a method for resetting grid.
    # option for resetting path will come after algorithm implementation
    def resetGrid(self):
        self.gridArray = [[0 for col in range(self.columns)] for row in range(self.rows)]
    
    # generate adjacency list
    def adjacencyList(self):
        
        def validEdges(neighbours):
            edges = {}
            for n in neighbours:
                val = self.gridArray[n[1]][n[0]]
                if val != "#":
                    edges[n] = val
            return edges
        
        adjacency = {}
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
                    
                    # left column - add above, right and below
                    elif x == 0:
                        neighbours = [(x, y-1), (x+1, y), (x, y+1)]
                    
                    # right column - add above, left and below
                    elif x == len(row) - 1:
                        neighbours = [(x, y-1), (x-1, y), (x, y+1)]
                    
                    # normal conditions - above, below, left, right
                    else:
                        neighbours = [(x, y-1), (x, y+1), (x-1, y), (x+1, y)]
                    
                    # add map of weighted neighbours to adjacency list
                    adjacency[(x, y)] = validEdges(neighbours)
        
        return adjacency
                    
test = Grid(5, 5)
test.adjacencyList()
#test.outputGrid()
