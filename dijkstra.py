import grid
import heapq
import math
import time

# Dijkstra's Algorithm Subroutine
# parameters adjacency list A, start node (tuple) and end node (tuple)
def DIJKSTRA(A, start: tuple, end: tuple): # --> returns ordered discovered cells, path and distance
    startTime = time.perf_counter()
    def retrace(prev_node, start, end):
        path = [end]
        while path[-1] != start:
            path.append(prev_node[path[-1]])
        
        return path[::-1]
    
    dist = {}
    previous_node = {}
    queue = [(0, start)]
    uiDiscovered = []
    visited = set()
    for node in A:
        dist[node] = math.inf
    dist[start] = 0
    
    while queue:
        # we don't actually have to use cur_dist
        cur_dist,  cur_node = heapq.heappop(queue)
        if cur_node in visited:
            continue
        visited.add(cur_node)
        uiDiscovered.append(cur_node)
        if cur_node == end:
            path = retrace(previous_node, start, end)
            endTime = time.perf_counter()
            runtime = (endTime - startTime)*10**3
            return dist[end], path, uiDiscovered, runtime
        
        for neighbour in A[cur_node]:
            potential_dist = dist[cur_node] + A[cur_node][neighbour]
            if potential_dist < dist[neighbour]:
                dist[neighbour] = potential_dist
                previous_node[neighbour] = cur_node
                heapq.heappush(queue, (dist[neighbour], neighbour))
        

    endTime = time.perf_counter()
    runtime = (endTime - startTime) * 10**3
    return 0, [], uiDiscovered, runtime

dims = 50

g = grid.Grid(dims, dims)

start = g.getStart()
end = g.getEnd()


g.randomWeightedGrid()

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
    g.insertValue("#", i[0], i[1])



a = g.adjacencyList()
dist, path, cells, t = DIJKSTRA(a, start, end)

print(f"Runtime: {t:.4f}ms")
print(f"number of discovered cells: {len(cells)}")
print(f"length of shortest path: {len(path)} with cost {dist}")