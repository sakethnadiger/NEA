import grid
from collections import deque


# Breadth-First Search Subroutine
# parameters adjacency list A, start node (tuple) and end node (tuple)
def BFS(A, start: tuple, end: tuple): # --> returns ordered discovered cells and path
    
    def retrace(prev_node, start, end):
        path = [end]
        while path[-1] != start:
            path.append(prev_node[path[-1]])
        
        return path[::-1]
    
    discovered = set()
    previous_node = {}
    uiDiscovered = []
    queue = deque()
    
    queue.append(start)
    while queue:
        node = queue.popleft()
        if node == end:
            path = retrace(previous_node, start, end)
            return uiDiscovered, path
        for neighbour in A[node]:
            if neighbour not in discovered:
                discovered.add(neighbour)
                uiDiscovered.append(neighbour)
                previous_node[neighbour] = node
                queue.append(neighbour)
    return uiDiscovered, []

test = grid.Grid(5, 4)

test.outputGrid()

A = test.adjacencyList()

print(test.getStart(), test.getEnd())

uiDiscovered, path = BFS(A, test.getStart(), test.getEnd())

print(len(uiDiscovered))
print(path)
