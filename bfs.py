import grid
from collections import deque
from runtime import runtime


# Breadth-First Search Subroutine
# parameters adjacency list A, start node (tuple) and end node (tuple)
def BFS(A, start: tuple, end: tuple): # --> returns ordered discovered cells and path
    discovered = set()
    uiDiscovered = []
    queue = deque()
    queue.append((start, [start]))
    while len(queue) > 0:
        node, path = queue.popleft()
        if node == end:
            return uiDiscovered, path
        if node not in discovered:
            discovered.add(node)
            uiDiscovered.append(node)
        for neighbour in A[node]:
            if neighbour not in discovered:
                queue.append((neighbour, path + [neighbour]))
                
    return uiDiscovered, []

test = grid.Grid(4, 4)

# obstacles = [(2, 0), (2, 1), (2, 2), (2, 3)]
# for o in obstacles:
#     test.insertValue("#", o[0], o[1])

A = test.adjacencyList()

uiDiscovered, path = BFS(A, test.getStart(), test.getEnd())

t = runtime(BFS, A, test.getStart(), test.getEnd())
print(t)