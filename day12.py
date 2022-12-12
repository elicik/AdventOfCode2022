import re
import numpy as np
import math
import bisect

lines = []
with open("day12.txt") as input_file:
    lines = input_file.read().rstrip().split("\n")

# lines = [
# "Sabqponm",
# "abcryxxl",
# "accszExk",
# "acctuvwj",
# "abdefghi"
# ]

map = []

for line in lines:
    map_line = [ord(i) for i in line]
    map.append(map_line)

x_range = len(map)
y_range = len(map[0])

goal = ()
starts = []

for x in range(x_range):
    for y in range(y_range):
        # Comment out for part 1
        if map[x][y] == ord("a"):
            starts.append((x, y))
        if map[x][y] == ord("S"):
            map[x][y] = ord("a")
            starts.append((x, y))
        if map[x][y] == ord("E"):
            map[x][y] = ord("z")
            goal = (x, y)

def h(node):
    return abs(goal[0]-node[0]) + abs(goal[1] - node[1])

# A*

g = {}
f = {}

for start in starts:
    g[start] = 0
    f[start] = h(start)

open_set = sorted(starts, key=lambda i:f[i])

current = None

while len(open_set) != 0:
    current = open_set.pop(0)
    if current == goal:
        break
    neighbors = []
    x = current[0]
    y = current[1]
    if x != 0 and map[x-1][y] <= 1 + map[x][y]:
        neighbors.append((x-1, y))
    if x != x_range - 1 and map[x+1][y] <= 1 + map[x][y]:
        neighbors.append((x+1, y))
    if y != 0 and map[x][y-1] <= 1 + map[x][y]:
        neighbors.append((x, y-1))
    if y != y_range - 1 and map[x][y+1] <= 1 + map[x][y]:
        neighbors.append((x, y+1))
    for neighbor in neighbors:
        tentative_g = g[current] + 1
        if tentative_g < g.get(neighbor, math.inf):
            g[neighbor] = tentative_g
            f[neighbor] = tentative_g + h(neighbor)
            if neighbor not in open_set:
                bisect.insort(open_set, neighbor, key=lambda i: f[i])

print(g[goal])