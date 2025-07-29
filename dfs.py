import grid

# Depth-First Search Subroutine
# parameters adjacency list A, start node (tuple) and end node (tuple)
def DFS(A, start: tuple, end: tuple): # --> returns ordered discovered cells and path
    discovered = set()
    uiDiscovered = []
    stack = []
    stack.append((start, [start]))
    while len(stack) > 0:
        # unpack tuple directly
        node, path = stack.pop()
        if node == end:
            return uiDiscovered, path
        if node not in discovered:
            discovered.add(node)
            uiDiscovered.append(node)
            for neighbour in A[node]:
                stack.append((neighbour, path + [neighbour]))

    return uiDiscovered, []


