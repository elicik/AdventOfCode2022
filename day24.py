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
with open("day24.txt") as input_file:
    lines = input_file.read().rstrip().split("\n")

# lines = [
# "#.######",
# "#>>.<^<#",
# "#.<..<<#",
# "#>v.><>#",
# "#<^v^^>#",
# "######.#"
# ]

len_rows = len(lines)
len_cols = len(lines[0])

blizzards = [{}]

for row in range(1, len_rows - 1):
    for col in range(1, len_cols - 1):
        char = lines[row][col]
        if char in "><v^":
            if (row, col) not in blizzards[0]:
                blizzards[0][(row, col)] = []
            blizzards[0][(row, col)].append(char)

cycle_length = math.lcm(len_rows - 2, len_cols - 2)

def find_min_steps(start, goal, existing_steps, forwards):
    queue = collections.deque([(start[0], start[1], existing_steps)])
    goal_row, goal_col = goal
    min_steps = math.inf

    visited = {}
    while queue:
        row, col, steps = queue.pop()
        if steps > min_steps:
            continue
        if (row, col) == (goal_row, goal_col):
            min_steps = steps
            continue

        if (row, col, steps % cycle_length) in visited.keys():
            existing_steps = visited[row, col, steps % cycle_length]
            if steps < existing_steps:
                visited[row, col, steps % cycle_length] = steps
            else:
                continue
        visited[row, col, steps % cycle_length] = steps

        if steps % cycle_length == len(blizzards):
            old_blizzards = blizzards[steps-1]
            new_blizzards = {}
            for location in old_blizzards:
                for direction in old_blizzards[location]:
                    if direction == ">":
                        new_location = (location[0], (location[1] - 1 + 1) % (len_cols - 2) + 1)
                    if direction == "<":
                        new_location = (location[0], (location[1] - 1 - 1) % (len_cols - 2) + 1)
                    if direction == "v":
                        new_location = ((location[0] - 1 + 1) % (len_rows - 2) + 1, location[1])
                    if direction == "^":
                        new_location = ((location[0] - 1 - 1) % (len_rows - 2) + 1, location[1])
                    if new_location not in new_blizzards:
                        new_blizzards[new_location] = []
                    new_blizzards[new_location].append(direction)
            blizzards.append(new_blizzards)
        if (row, col) not in blizzards[steps % cycle_length]:
            queue.append((row, col, steps + 1))
        if forwards:
            directions = "^<v>"
        else:
            directions = ">v<^"
        for direction in directions:
            if direction == ">":
                new_row, new_col = row, col + 1
            if direction == "<":
                new_row, new_col = row, col - 1
            if direction == "v":
                new_row, new_col = row + 1, col
            if direction == "^":
                new_row, new_col = row - 1, col
            if (new_row, new_col) == (goal_row, goal_col) or (0 < new_row < len_rows - 1 and 0 < new_col < len_cols - 1 and (new_row, new_col) not in blizzards[steps % cycle_length].keys()):
                queue.append((new_row, new_col, steps + 1))
    return min_steps

start = (0, 1)
goal = (len_rows - 1, len_cols - 2)
existing_steps = 0
existing_steps = find_min_steps(start, goal, existing_steps, True)
print(existing_steps - 1)
existing_steps = find_min_steps(goal, start, existing_steps, False)
existing_steps = find_min_steps(start, goal, existing_steps, True)
print(existing_steps - 1)