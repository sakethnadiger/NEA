import grid
from collections import deque
import time

# Breadth-First Search Subroutine
# parameters adjacency list A, start node (tuple) and end node (tuple)
def BFS(A, start: tuple, end: tuple): # --> returns ordered discovered cells and path
    startTime = time.perf_counter()
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
            endTime = time.perf_counter()
            runtime = (endTime - startTime)*10**3
            return uiDiscovered, path, round(runtime, 4)
        for neighbour in A[node]:
            if neighbour not in discovered:
                discovered.add(neighbour)
                uiDiscovered.append(neighbour)
                previous_node[neighbour] = node
                queue.append(neighbour)
                
    endTime = time.perf_counter()
    runtime = (endTime - startTime)*10**3
    return uiDiscovered, [], round(runtime, 4)

test = grid.Grid(10, 10)
obstacles = [(1, 0), (5, 6), (3, 4), (4, 6), (5, 8), (9, 2), (6, 3)]

for o in obstacles:
    test.insertValue("#", o[0], o[1])

cells, path, t = BFS(test.adjacencyList(), test.getStart(), test.getEnd())

test.displayPath(path)