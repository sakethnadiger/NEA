import grid

# Depth-First Search Subroutine
# parameters adjacency list A, start node (tuple) and end node (tuple)
def DFS(A, start: tuple, end: tuple): # --> returns ordered discovered cells and path
    
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
            return uiDiscovered, path
        if node not in discovered:
            discovered.add(node)
            uiDiscovered.append(node)
            for neighbour in A[node]:
                if neighbour not in discovered:
                    previous_node[neighbour] = node
                    stack.append(neighbour)
    

    return uiDiscovered, []

test = grid.Grid(4, 5)

A = test.adjacencyList()

uiDiscovered, p = DFS(A, test.getStart(), test.getEnd())

print(p)