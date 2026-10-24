
# Lab 4: A* Search and UCS
graph = {
    "S": [("A", 1), ("B", 4)],
    "A": [("C", 2)],
    "B": [("G", 5)],
    "C": [("G", 3)],
    "G": []
}

h = {
    "S": 5,
    "A": 4,
    "B": 4,
    "C": 2,
    "G": 0
}
def search(graph, h, start, goal):
    queue = [(h[start], 0, start, [start])]
    best = {start: 0}
    expanded = []

    while queue:
        queue.sort()
        f, cost, node, path = queue.pop(0)

        if cost != best[node]:
            continue

        if node == goal:
            return path, cost, expanded

        expanded.append(node)

        for child, weight in graph[node]:
            new_cost = cost + weight

            if new_cost < best.get(child, 999):
                best[child] = new_cost
                queue.append(
                    (new_cost + h[child], new_cost, child, path + [child])
                )

    return [], 0, expanded


# Task 1: A*
print("TASK 1: A* Search")
path, cost, expanded = search(graph, h, "S", "G")
print("Path:", path)
print("Cost:", cost)
print("Expanded:", expanded)


# Task 2: UCS (heuristic values are zero)
print("\nTASK 2: UCS")
zero_h = {"S": 0, "A": 0, "B": 0, "C": 0, "G": 0}

path, cost, expanded = search(graph, zero_h, "S", "G")
print("Path:", path)
print("Cost:", cost)
print("Expanded:", expanded)


# Task 3: Overestimate h(C)
print("\nTASK 3: Overestimate")
new_h = h.copy()
new_h["C"] = 10

path, cost, expanded = search(graph, new_h, "S", "G")
print("New h(C):", new_h["C"])
print("Path:", path)
print("Cost:", cost)
print("Expanded:", expanded)
