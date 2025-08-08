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