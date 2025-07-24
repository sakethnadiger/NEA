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
    def adjacencyList():
        adjacency = {}

test = Grid(5, 5)

test.insertValue(8, 0, 0)
test.outputGrid()
