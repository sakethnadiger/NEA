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
            return dist[end], uiDiscovered, path, round(runtime, 4)
        
        for neighbour in A[cur_node]:
            potential_dist = dist[cur_node] + A[cur_node][neighbour]
            if potential_dist < dist[neighbour]:
                dist[neighbour] = potential_dist
                previous_node[neighbour] = cur_node
                heapq.heappush(queue, (dist[neighbour], neighbour))
        

    endTime = time.perf_counter()
    runtime = (endTime - startTime) * 10**3
    return 0, uiDiscovered, [], round(runtime, 4)

test = grid.Grid(10, 10)

test.randomWeightedGrid()

dist, cells, path, t = DIJKSTRA(test.adjacencyList(), test.getStart(), test.getEnd())

cur_alg = "Dijkstra's"

print(f"{cur_alg} completed in {t}, visited {len(cells)} cells, shortest path {len(path)} cells, with cost {dist}.")