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
    return D * int(math.sqrt((dx)**2 + (dy)**2))

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
            return known_dist[cur_node], retrace(previous_node, start, end), uiDiscovered, runtime
        
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
    return 0, [], uiDiscovered, runtime

dims = 50

test = grid.Grid(dims, dims)

start = test.getStart()
end = test.getEnd()

test.randomWeightedGrid()

obstacles = [
    (0, 3), (1, 0), (39, 2), (44, 5), (15, 20), (7, 29), (20, 48), (22, 43),
    (34, 26), (12, 10), (17, 39), (48, 30), (6, 12), (38, 1), (3, 36), (41, 23),
    (8, 44), (30, 21), (16, 5), (25, 36), (27, 12), (5, 0), (35, 9), (42, 13),
    (33, 44), (36, 29), (46, 35), (19, 10), (28, 7), (9, 19), (18, 22), (47, 14),
    (2, 32), (32, 48), (0, 20), (23, 9), (14, 13), (13, 33), (37, 46), (4, 4),
    (40, 6), (31, 1), (29, 0), (1, 16), (45, 24), (24, 18), (11, 11), (26, 45),
    (43, 0), (49, 12), (19, 28), (17, 6), (10, 3), (27, 37), (6, 41), (38, 20),
    (22, 22), (12, 38), (35, 5), (46, 48), (34, 0), (48, 4), (9, 32), (36, 17),
    (5, 24), (44, 16), (0, 35), (39, 45), (31, 26), (20, 19), (2, 6), (15, 3),
    (18, 11), (41, 34), (4, 48), (29, 2), (13, 20), (33, 7), (42, 28), (40, 42),
    (16, 40), (8, 2), (14, 48), (25, 17), (7, 47), (3, 9), (11, 27), (1, 30),
    (43, 6), (21, 35), (32, 4), (45, 41), (24, 40), (30, 13), (28, 24), (26, 3)
]

for i in obstacles:
    test.insertValue("#", i[0], i[1])



A = test.adjacencyList()

dist, path, cells, t = ASTAR(A, start, end, EUCLIDEAN)


print(f"Runtime: {t:.4f}ms")
print(f"number of discovered cells: {len(cells)}")
print(f"length of shortest path: {len(path)} with cost {dist}")