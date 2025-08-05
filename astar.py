import grid
import heapq
import math
import time

def MANHATTAN(node: tuple, end: tuple):
    D = 3
    dx = abs(node[0] - end[0])
    dy = abs(node[1] - end[1])
    return D * (dx + dy)

def EUCLIDEAN(node: tuple, end: tuple):
    D = 2
    dx = abs(node[0] - end[0])
    dy = abs(node[1] - end[1])
    return D * math.hypot(dx, dy)

# A* Algorithm Subroutine
# parameters adjacency list A, start node (tuple), end node (tuple) and heuristic
def ASTAR(A, start: tuple, end: tuple, heuristic): # --> returns ordered discovered cells, path and distance
    startTime = time.perf_counter()
    def retrace(prev_node, start, end):
        path = [end]
        while path[-1] != start:
            path.append(prev_node[path[-1]])
        
        return path[::-1]
    
    previous_node = {}
    visited = set()
    uiDiscovered = []
    # g(n) - represents the current known distance from start
    known_dist = {}
    for node in A:
        known_dist[node] = math.inf
    known_dist[start] = 0
    # f(n) - represents the total distance from start to end
    total_dist = {}
    for node in A:
        total_dist[node] = math.inf
    
    total_dist[start] = known_dist[start] + heuristic(start, end)
    
    queue = []
    heapq.heappush(queue, (total_dist[start], start))
    
    while queue:
        # we don't actually require the current best distance as a value, hence it is not accessed again.
        cur_best_dist, cur_node = heapq.heappop(queue)
        
        # add to visited set and ui list for animation purposes
        if cur_node not in visited:
            visited.add(cur_node)
            uiDiscovered.append(cur_node)
        
        # check for completed path
        if cur_node == end:
            endTime = time.perf_counter()
            runtime = (endTime - startTime) * 10**3
            return known_dist[cur_node], uiDiscovered, retrace(previous_node, start, end), round(runtime, 4)
        
        for neighbour in A[cur_node]:
            if neighbour in visited:
                continue
            potential_known_dist = known_dist[cur_node] + A[cur_node][neighbour]
            if potential_known_dist < known_dist[neighbour]:
                known_dist[neighbour] = potential_known_dist
                # f(n) = g(n) + h(n) --> A* minimises this
                total_dist[neighbour] = known_dist[neighbour] + heuristic(neighbour, end)
                previous_node[neighbour] = cur_node
                heapq.heappush(queue, (total_dist[neighbour], neighbour))
    
    endTime = time.perf_counter()
    runtime = (endTime - startTime) * 10**3
    return 0, uiDiscovered, [], round(runtime, 4)

test = grid.Grid(10, 10)

test.randomWeightedGrid()

dist, cells, path, t = ASTAR(test.adjacencyList(), test.getStart(), test.getEnd(), EUCLIDEAN)

cur_alg = "A*"

print(f"{cur_alg} completed in {t}ms, visited {len(cells)} cells, shortest path {len(path)} cells, with cost {dist}.")