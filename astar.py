import grid
import heapq
import math

# Define heuristics

# Euclidean distance
def Euclidean(node: tuple, end: tuple):
    return int(math.sqrt((node[0] - end[0])**2 + (node[1] - end[1])**2))

# Manhattan distance
def Manhattan(node: tuple, end: tuple):
    return abs(node[0] - end[0]) + abs(node[0] - end[0])

# A* Algorithm Subroutine
# parameters adjacency list A, start node (tuple), end node (tuple), function passed in as a string and determined within the algorithm
def ASTAR(A, start: tuple, end: tuple, heuristic): # --> returns ordered discovered cells, path and distance
    
    def retrace(prev_node, start, end):
        path = [end]
        while path[-1] != start:
            path.append(prev_node[path[-1]])
        
        return path[::-1]
    
    dist = {}
    previous_node = {}
    queue = []
    uiDiscovered = []
    visited = set()
    estimated_dist = {}
    
    for node in A:
        dist[node] = math.inf
        estimated_dist[node] = math.inf
        previous_node[node] = None
    
    dist[start] = 0
    estimated_dist[start] = heuristic(start, end)
    heapq.heappush(queue, (estimated_dist[start], start))
    
    while queue:
        cur_dist, cur_node = heapq.heappop(queue)
        
        if cur_node not in visited:
            visited.add(cur_node)
            uiDiscovered.append(cur_node)
        
        if cur_node == end:
            path = retrace(previous_node, start, end)
            
            return dist[end], path, uiDiscovered
        
        for neighbour in A[cur_node]:
            potential_dist = cur_dist + A[cur_node][neighbour]
            if potential_dist < dist[neighbour]:
                previous_node[neighbour] = cur_node
                dist[neighbour] = potential_dist
                estimated_dist[neighbour] = potential_dist + heuristic(neighbour, end)
                if neighbour not in visited:
                    heapq.heappush(queue, (estimated_dist[neighbour], neighbour))
    
    return 0, [], uiDiscovered

test = grid.Grid(4, 4)

a = test.adjacencyList()

distance, path, discovered = ASTAR(a, test.getStart(), test.getEnd(), Manhattan)

print(len(discovered))
print(path)