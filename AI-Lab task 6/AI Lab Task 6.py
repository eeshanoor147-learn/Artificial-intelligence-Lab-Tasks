import collections
# BFS algorithm using queue
def bfs_with_queue(graph, root):
    visited, queue = set(), collections.deque([root])
    visited.add(root)
    while queue:
        # Dequeue a vertex from queue
        vertex = queue.popleft()
        print(str(vertex) + " ", end="")
        # Check neighbours
        for neighbour in graph[vertex]:
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)
if __name__ == '__main__':
    graph = {0: [1, 2], 1: [2], 2: [3], 3: [1, 2]}
    print("Following is Breadth First Traversal with queue:")
    bfs_with_queue(graph, 0)

    # BFS algorithm without using queue
def bfs_without_queue(graph, root):
    visited = set()
    queue = [root]
    visited.add(root)
    while queue:
        # Remove first element
        vertex = queue.pop(0)
        print(str(vertex) + " ", end="")
        # Check neighbours
        for neighbour in graph[vertex]:
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)
if __name__ == '__main__':
    graph = {0: [1, 2], 1: [2], 2: [3], 3: [1, 2]}
    print("Following is Breadth First Traversal without queue:")
    bfs_without_queue(graph, 0)