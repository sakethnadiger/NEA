import grid
import time

# Depth-First Search Subroutine
# parameters adjacency list A, start node (tuple) and end node (tuple)
def DFS(A, start: tuple, end: tuple): # --> returns ordered discovered cells and path
    startTime = time.perf_counter()
    
    def retrace(prev_node, start, end):
        path = [end]
        while path[-1] != start:
            path.append(prev_node[path[-1]])
        
        return path[::-1]
    
    previous_node = {}
    discovered = set()
    uiDiscovered = []
    stack = [start]
    while stack:
        node = stack.pop()
        if node == end:
            path = retrace(previous_node, start, end)
            endTime = time.perf_counter()
            runtime = (endTime - startTime)*10**3
            return uiDiscovered, path, round(runtime, 4)
        if node not in discovered:
            discovered.add(node)
            uiDiscovered.append(node)
            for neighbour in A[node]:
                if neighbour not in discovered:
                    previous_node[neighbour] = node
                    stack.append(neighbour)
    
    
    endTime = time.perf_counter()
    runtime = (endTime - startTime)*10**3
    return uiDiscovered, [], round(runtime, 4)

