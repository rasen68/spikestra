import numpy as np

cost_map = np.loadtxt("cost_map_8x8.csv", delimiter=",")

rows, cols = cost_map.shape
start = (0,0)
goal = (7,7)

directions = [
    (-1,0),
    (1,0),
    (0,-1),
    (0,1)
]

dist = {}
prev = {}
Q = []

#initialize
for r in range(rows): 
    for c in range(cols):
        vertex = (r, c)

        dist[vertex] = float('inf')
        prev[vertex] = None
        Q.append(vertex)

dist[start] = 0

while Q: 
    u = min(Q, key=lambda vertex: dist[vertex])
    Q.remove(u)
    if u == goal: 
        break

    row, col = u

    for dr, dc in directions: 
        nr = row + dr
        nc = col + dc

        if 0 <= nr < rows and 0 <= nc < cols: 
            v = (nr, nc)

            if v not in Q: 
                continue

            alt = dist[u] + cost_map[nr, nc]

            if alt < dist[v]: 
                dist[v] = alt
                prev[v] = u

path = []
current = goal
while current is not None: 
    path.append(current)
    current = prev[current]
path.reverse()

print("Shortest path:", path)
print()
print("Total path cost:", dist[goal])
print()
print("Path length:", len(path))



