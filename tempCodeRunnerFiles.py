import grid
import heapq
import math

# Dijkstra's Algorithm Subroutine
# parameters adjacency list A, start node (tuple) and end node (tuple)
def DIJKSTRA(A, start: tuple, end: tuple): # --> returns ordered discovered cells and path
    dist = {}
    previous_node = {}
    queue = [(0, start)]
    uiDiscovered = []
    for node in A:
        dist[node] = math.inf
        previous_node[node] = None
    dist[start] = 0
    
    while len(queue) > 0:
        cur_dist,  cur_node = heapq.heappop(queue)
        if cur_node not in uiDiscovered:
            uiDiscovered.append(cur_node)
        if cur_node == end:
            path = []
            cur_node = end
            if previous_node[cur_node] or cur_node == start:
                while cur_node:
                    path.append(cur_node)
                    cur_node = previous_node[cur_node]
            
            return dist[end], path[::-1], uiDiscovered
        
        for neighbour in A[cur_node]:
            potential_dist = cur_dist + A[cur_node][neighbour]
            if potential_dist < dist[neighbour]:
                dist[neighbour] = potential_dist
                previous_node[neighbour] = cur_node
                heapq.heappush(queue, (potential_dist, neighbour))
        

    
    return dist[end], [], uiDiscovered

g = grid.Grid(4, 4)

# obstacles = [(1, 0), (2, 2), (1, 3)]

# for o in obstacles:
#     g.insertValue("#", o[0], o[1])

g.randomWeightedGrid()

g.outputGrid()

a = g.adjacencyList()
distance, path, discovered = DIJKSTRA(a, g.getStart(), g.getEnd())

print(path)