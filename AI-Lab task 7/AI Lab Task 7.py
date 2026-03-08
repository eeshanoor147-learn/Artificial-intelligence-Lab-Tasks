class Graph:
    def __init__(self, graph):
        self.graph = graph
    def neighbors(self, node):
        return self.graph[node]
    def heuristic(self, node):
        h_value = {
            'A': 1,
            'B': 1,
            'C': 1,
            'D': 1
        }
        return h_value[node]
    def a_star(self, start, goal):
        open_set = [start]
        closed_set = []
        cost = {}
        cost[start] = 0
        parent = {}
        parent[start] = None
        while open_set:
            current = open_set[0]
            for node in open_set:
                if cost[node] + self.heuristic(node) < cost[current] + self.heuristic(current):
                    current = node
            if current == goal:
                path = []
                while current is not None:
                    path.append(current)
                    current = parent[current]
                path.reverse()
                print("Path:", path)
                return path
            open_set.remove(current)
            closed_set.append(current)
            for (neighbor, weight) in self.neighbors(current):
                new_cost = cost[current] + weight
                if neighbor not in open_set and neighbor not in closed_set:
                    open_set.append(neighbor)
                    parent[neighbor] = current
                    cost[neighbor] = new_cost
                elif new_cost < cost.get(neighbor, float('inf')):
                    cost[neighbor] = new_cost
                    parent[neighbor] = current
                    if neighbor in closed_set:
                        closed_set.remove(neighbor)
                        open_set.append(neighbor)

        print("No path found")
        return None
graph_data = {
    'A': [('B', 1), ('C', 3), ('D', 7)],
    'B': [('D', 5)],
    'C': [('D', 12)],
    'D': []
}

g = Graph(graph_data)
g.a_star('A', 'D')