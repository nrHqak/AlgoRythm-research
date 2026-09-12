"""Synthetic graph-traversal fixture; never scientific data."""

from collections import deque


def build_graph(node_count, edges):
    graph = [[] for _ in range(node_count)]
    for left, right in edges:
        graph[left].append(right)
        graph[right].append(left)
    for neighbors in graph:
        neighbors.sort()
    return graph


def bfs_distances(graph, start):
    distance = [-1] * len(graph)
    distance[start] = 0
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if distance[neighbor] != -1:
                continue
            distance[neighbor] = distance[node] + 1
            queue.append(neighbor)
    return distance


def connected_components(graph):
    component = [-1] * len(graph)
    component_id = 0
    for start in range(len(graph)):
        if component[start] != -1:
            continue
        stack = [start]
        component[start] = component_id
        while stack:
            node = stack.pop()
            for neighbor in reversed(graph[node]):
                if component[neighbor] == -1:
                    component[neighbor] = component_id
                    stack.append(neighbor)
        component_id += 1
    return component


def eccentricity(graph, start):
    distances = bfs_distances(graph, start)
    reachable = [value for value in distances if value >= 0]
    return max(reachable, default=0)


def graph_summary(graph):
    components = connected_components(graph)
    sizes = {}
    for component in components:
        sizes[component] = sizes.get(component, 0) + 1
    return len(sizes), sorted(sizes.values(), reverse=True)


def parse(text):
    values = [int(token) for token in text.split()]
    if len(values) < 3:
        raise ValueError("expected graph header")
    node_count, edge_count, start = values[:3]
    payload = values[3:]
    if len(payload) != edge_count * 2:
        raise ValueError("edge count mismatch")
    edges = []
    for index in range(0, len(payload), 2):
        edges.append((payload[index], payload[index + 1]))
    return node_count, start, edges


def solve(text):
    node_count, start, edges = parse(text)
    graph = build_graph(node_count, edges)
    distances = bfs_distances(graph, start)
    component_count, sizes = graph_summary(graph)
    first = " ".join(map(str, distances))
    second = f"{component_count}:" + ",".join(map(str, sizes))
    return first + "\n" + second


if __name__ == "__main__":
    import sys

    print(solve(sys.stdin.read()))
