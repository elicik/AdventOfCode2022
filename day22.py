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

# lines = [
# "        ...#",
# "        .#..",
# "        #...",
# "        ....",
# "...#.......#",
# "........#...",
# "..#....#....",
# "..........#.",
# "        ...#....",
# "        .....#..",
# "        .#......",
# "        ......#.",
# "",
# "10R5L5R10L4R5L5"
# ]

# assumes path starts with number
path = re.split("([LRUD])", lines[-1])

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
    curr_row, curr_col = 0, row_starts[0]

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

def part2():
    class cube_side:
        def __init__(self, row, col, label):
            self.row = row
            self.col = col
            # right, down, left, up
            self.edges = [(None, None), (None, None), (None, None), (None, None)]
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

    # fold corners
    all_connected = False
    while not all_connected:
        for a, b, c in itertools.permutations(sides, 3):
            for i in range(4):
                a_down_side, a_down_rotation = a.edges[(i+1) % 4]
                if a_down_side is None:
                    continue
                total_rotation = a_down_rotation
                b_right_side, b_right_rotation = b.edges[(i-total_rotation) % 4]
                if b_right_side is None:
                    continue
                total_rotation += b_right_rotation
                c_up_side, c_up_rotation = c.edges[(i+3-total_rotation) % 4]
                if a_down_side == b and b_right_side == c and c_up_side is None:
                    a.edges[i] = (c, (total_rotation-1) % 4)
                    c.edges[(i+3-total_rotation) % 4] = (a, -(total_rotation-1) % 4)
        all_connected = True
        for side in sides:
            if any(edge[0] is None for edge in side.edges):
                all_connected = False
                break

    # print("Sides:")
    # for side in sides:
    #     side.print_edges()

    # 0 is right, 1 is down, 2 is left, 3 is up
    direction = 0
    curr_row, curr_col = 0, row_starts[0]
    curr_side = sides[0]

    for instruction_index, instruction in enumerate(path):
        if instruction_index % 2 == 0:
            num = int(instruction)
            for n in range(num):
                next_row = curr_row
                next_col = curr_col
                next_side = curr_side
                next_direction = direction
                if direction == 0:
                    next_col += 1
                    if next_col % size_of_side == 0:
                        next_side, next_side_rotation = curr_side.edges[direction]
                        next_direction = (direction - next_side_rotation) % 4

                        next_row %= size_of_side
                        next_col %= size_of_side
                        for i in range((next_side_rotation)%4):
                            next_row, next_col = size_of_side - 1 - next_col, next_row
                        next_row += next_side.row
                        next_col += next_side.col
                if direction == 2:
                    next_col -= 1
                    if (next_col + 1) % size_of_side == 0:
                        next_side, next_side_rotation = curr_side.edges[direction]
                        next_direction = (direction - next_side_rotation) % 4

                        next_row %= size_of_side
                        next_col %= size_of_side
                        for i in range((next_side_rotation)%4):
                            next_row, next_col = size_of_side - 1 - next_col, next_row
                        next_row += next_side.row
                        next_col += next_side.col
                if direction == 1:
                    next_row += 1
                    if next_row % size_of_side == 0:
                        next_side, next_side_rotation = curr_side.edges[direction]
                        next_direction = (direction - next_side_rotation) % 4

                        next_row %= size_of_side
                        next_col %= size_of_side
                        for i in range((next_side_rotation)%4):
                            next_row, next_col = size_of_side - 1 - next_col, next_row
                        next_row += next_side.row
                        next_col += next_side.col
                if direction == 3:
                    next_row -= 1
                    if (next_row + 1) % size_of_side == 0:
                        next_side, next_side_rotation = curr_side.edges[direction]
                        next_direction = (direction - next_side_rotation) % 4

                        next_row %= size_of_side
                        next_col %= size_of_side
                        for i in range((next_side_rotation)%4):
                            next_row, next_col = size_of_side - 1 - next_col, next_row
                        next_row += next_side.row
                        next_col += next_side.col
                if map[next_row, next_col] == "#":
                    break
                else:
                    curr_row, curr_col, curr_side, direction = next_row, next_col, next_side, next_direction
        else:
            if instruction == "R":
                direction += 1
            else:
                direction -= 1
            direction %= 4
    print(1000 * (curr_row + 1) + 4 * (curr_col + 1) + direction)

part2()