import grid
import heapq
import math

# Dijkstra's Algorithm Subroutine
# parameters adjacency list A, start node (tuple) and end node (tuple)
def DIJKSTRA(A, start: tuple, end: tuple): # --> returns ordered discovered cells, path and distance
    
    def retrace(prev_node, start, end):
        path = [end]
        while path[-1] != start:
            path.append(prev_node[path[-1]])
        
        return path[::-1]
    
    dist = {}
    previous_node = {}
    queue = [(0, start)]
    uiDiscovered = []
    for node in A:
        dist[node] = math.inf
    dist[start] = 0
    
    while queue:
        cur_dist,  cur_node = heapq.heappop(queue)
        if cur_node not in uiDiscovered:
            uiDiscovered.append(cur_node)
        if cur_node == end:
            path = retrace(previous_node, start, end)
            
            return dist[end], path, uiDiscovered
        
        for neighbour in A[cur_node]:
            potential_dist = cur_dist + A[cur_node][neighbour]
            if potential_dist < dist[neighbour]:
                dist[neighbour] = potential_dist
                previous_node[neighbour] = cur_node
                heapq.heappush(queue, (potential_dist, neighbour))
        

    
    return 0, [], uiDiscovered

g = grid.Grid(5, 4)

a = g.adjacencyList()
distance, path, discovered = DIJKSTRA(a, g.getStart(), g.getEnd())

print(discovered)
print(path)