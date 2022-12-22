import re
import numpy as np
import math
import bisect
import functools
import time
import itertools
import copy
import collections


lines = []
with open("day22.txt") as input_file:
    lines = input_file.read().rstrip().split("\n")

lines = [
"        ...#",
"        .#..",
"        #...",
"        ....",
"...#.......#",
"........#...",
"..#....#....",
"..........#.",
"        ...#....",
"        .....#..",
"        .#......",
"        ......#.",
"",
"10R5L5R10L4R5L5"
]

# assumes path starts with number
path = re.split("([LRUD])", lines[-1])
# path = [int(p) if i % 2 == 0 else p for i, p in enumerate(path)]
# print(path)


num_rows = len(lines) - 2
num_cols = max(len(line) for line in lines[:num_rows])

map = np.full((num_rows, num_cols), " ")
row_starts = np.zeros((num_rows), dtype=int)
row_ends = np.zeros((num_rows), dtype=int)
col_starts = np.zeros((num_cols), dtype=int)
col_ends = np.zeros((num_cols), dtype=int)
size_of_side = math.inf

for row, line in enumerate(lines[:num_rows]):
    start = None
    end = len(line)
    for col, character in enumerate(line):
        if start is None and character != " ":
            start = col
        map[row, col] = character
    
    row_starts[row] = start
    row_ends[row] = end
    if end - start < size_of_side:
        size_of_side = end - start

for col in range(num_cols):
    start = None
    end = num_rows
    for row, character in enumerate(map[:, col]):
        if start is None and character != " ":
            start = row
        if start is not None and character == " ":
            end = row
            break
    
    col_starts[col] = start
    col_ends[col] = end


def part1():
    # 0 is right, 1 is down, 2 is left, 3 is up
    direction = 0
    curr_row, curr_col = col_starts[0], row_starts[0]

    for instruction_index, instruction in enumerate(path):
        if instruction_index % 2 == 0:
            num = int(instruction)
            for n in range(num):
                next_row = curr_row
                next_col = curr_col
                if direction == 0:
                    next_col += 1
                    if next_col == row_ends[next_row]:
                        next_col = row_starts[next_row]
                if direction == 2:
                    next_col -= 1
                    if next_col == row_starts[next_row] - 1:
                        next_col = row_ends[next_row] - 1
                if direction == 1:
                    next_row += 1
                    if next_row == col_ends[next_col]:
                        next_row = col_starts[next_col]
                if direction == 3:
                    next_row -= 1
                    if next_row == col_starts[next_col] - 1:
                        next_row = col_ends[next_col] - 1
                if map[next_row, next_col] == "#":
                    break
                else:
                    curr_row, curr_col = next_row, next_col
        else:
            if instruction == "R":
                direction += 1
            else:
                direction -= 1
            direction %= 4

    # print(curr_row, curr_col, direction)
    print(1000 * (curr_row + 1) + 4 * (curr_col + 1) + direction)

# part1()
edges = [(None, None), (None, None), (None, None), (None, None)]
class cube_side:
    def __init__(self, row, col, label):
        self.row = row
        self.col = col
        # right, down, left, up
        # self.edges = [(None, None), (None, None), (None, None), (None, None)]
        self.edges = edges.copy()
        self.label = label
    def __str__(self):
        return f"{self.label}"
        # return f"{self.label} = ({self.row},{self.col})"
        # return f"({self.row},{self.col})"
    def print_edges(self):
        print(self)
        print("right", self.edges[0][0], self.edges[0][1])
        print("down", self.edges[1][0], self.edges[1][1])
        print("left", self.edges[2][0], self.edges[2][1])
        print("up", self.edges[3][0], self.edges[3][1])

sides = []
# make sides
i = ord("A")
for row in range(0, num_rows, size_of_side):
    for col in range(0, num_cols, size_of_side):
        if map[row, col] != " ":
            sides.append(cube_side(row, col, chr(i)))
            i += 1

# connect the direct sides
for side in sides:
    for connecting_side in sides:
        if side.row + size_of_side == connecting_side.row and side.col == connecting_side.col:
            side.edges[1] = (connecting_side, 0)
            connecting_side.edges[3] = (side, 0)
        if side.col + size_of_side == connecting_side.col and side.row == connecting_side.row:
            side.edges[0] = (connecting_side, 0)
            connecting_side.edges[2] = (side, 0)

# print(sides[3])
# print("left", sides[3].left[0])
# print("right", sides[3].right[0])
# print("up", sides[3].up[0])
# print("down", sides[3].down[0])

# d, e, f = sides[3:]
# d.print_edges()
# e.print_edges()
# f.print_edges()

# connect corners
all_connected = False
while not all_connected:
    for a, b, c in itertools.permutations(sides, 3):
        # if a.label == "D" and b.label == "E" and c.label == "F":
        #     d, e, f = a, b, c
        #     d.print_edges()
        #     e.print_edges()
        #     f.print_edges()
        if a.edges[1][0] == b and b.edges[(0 - a.edges[1][1]) % 4][0] == c and c.edges[(3 - b.edges[(0 - a.edges[1][1]) % 4][1]) % 4][0] is None:
            total_rotation = (b.edges[(0 + a.edges[1][1]) % 4][1] - 1) % 4
            a.edges[0] = (c, total_rotation)
            c.edges[3] = (a, -total_rotation)
        if a.edges[2][0] == b and b.edges[(1 - a.edges[2][1]) % 4][0] == c and c.edges[(0 - b.edges[(1 - a.edges[2][1]) % 4][1]) % 4][0] is None:
            total_rotation = (b.edges[(1 + a.edges[2][1]) % 4][1] - 1) % 4
            a.edges[1] = (c, total_rotation)
            c.edges[0] = (a, -total_rotation)
        if a.edges[3][0] == b and b.edges[(2 - a.edges[3][1]) % 4][0] == c and c.edges[(1 - b.edges[(2 - a.edges[3][1]) % 4][1]) % 4][0] is None:
            total_rotation = (b.edges[(2 + a.edges[3][1]) % 4][1] - 1) % 4
            a.edges[2] = (c, total_rotation)
            c.edges[1] = (a, -total_rotation)
        if a.edges[0][0] == b and b.edges[(3 - a.edges[0][1]) % 4][0] == c and c.edges[(2 - b.edges[(3 - a.edges[0][1]) % 4][1]) % 4][0] is None:
            total_rotation = (b.edges[(3 + a.edges[0][1]) % 4][1] - 1) % 4
            a.edges[3] = (c, total_rotation)
            c.edges[2] = (a, -total_rotation)
        # if a.label == "D" and b.label == "E" and c.label == "F":
        #     d, e, f = a, b, c
        #     d.print_edges()
        #     e.print_edges()
        #     f.print_edges()
        #     exit()
        # if c.label == "A" and b.label == "D" and a.label == "C":
        #     x, y, z = c, b, a
        #     print(x, y, z)
        #     print(x.edges[1][0])
        #     print(y.up[0])
        #     print(y.left[0])
        #     print(z.right[0])
        #     print(z.up[0])
        #     print(x.left[0])
        #     exit()
    all_connected = True
    for side in sides:
        if any(edge[0] is None for edge in side.edges):
            all_connected = False
            break
    print("Sides:")
    for side in sides:
        side.print_edges()

print(sides[0])