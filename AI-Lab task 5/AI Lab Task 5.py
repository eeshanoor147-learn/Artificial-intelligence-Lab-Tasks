# DFS using Stack
def dfs_stack(graph, start_node):
    visited = set()
    stack = [start_node]
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            print(vertex)
            for neighbour in graph[vertex] - visited:
                stack.append(neighbour)
    return visited
graph = {'0': set(['1', '2']),
         '1': set(['0', '3', '4']),
         '2': set(['0']),
         '3': set(['1']),
         '4': set(['2', '3'])
         }
dfs_stack(graph, '0')

