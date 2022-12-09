import re
import numpy as np
import math

lines = []
with open("day9.txt") as input_file:
    lines = input_file.read().rstrip().split("\n")

# lines = [
# "R 4",
# "U 4",
# "L 3",
# "D 1",
# "R 4",
# "D 1",
# "L 5",
# "R 2"
# ]

# Part 1:
# num_knots = 2
# Part 2:
num_knots = 10
tail_history = set()

rope = [[0,0] for i in range(num_knots)]
head = rope[0]
tail = rope[-1]

tail_history.add(tuple(tail))

for line in lines:
    arr = line.split(" ")
    direction = arr[0]
    steps = int(arr[1])
    for step in range(steps):
        if direction == "U":
            head[0] += 1
        if direction == "D":
            head[0] -= 1
        if direction == "R":
            head[1] += 1
        if direction == "L":
            head[1] -= 1
        
        for knot_i in range(1, num_knots):
            front = rope[knot_i - 1]
            curr = rope[knot_i]
            diff_x = abs(front[0] - curr[0])
            diff_y = abs(front[1] - curr[1])
            if diff_x > 1 or diff_y > 1:
                # diagonal
                if (diff_x == 2 and diff_y == 1) or (diff_x == 1 and diff_y == 2):
                    # move 1 x, 1 y
                    move_x = int(math.copysign(1, front[0] - curr[0]))
                    move_y = int(math.copysign(1, front[1] - curr[1]))
                else:
                    move_x = int(math.copysign(1, front[0] - curr[0])) if diff_x != 0 else 0
                    move_y = int(math.copysign(1, front[1] - curr[1])) if diff_y != 0 else 0
                curr[0] += move_x
                curr[1] += move_y
        tail_history.add(tuple(tail))

print(len(tail_history))