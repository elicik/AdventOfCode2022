import re
import numpy as np
import math
import bisect
import functools
import time
import itertools
import copy

lines = []
with open("day17.txt") as input_file:
    lines = input_file.read().rstrip().split("\n")

# lines = [">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"]

jets = lines[0]

shapes = [
    frozenset([(2, 0), (3, 0), (4, 0), (5, 0)]),
    frozenset([(2, 1), (3, 0), (3, 1), (3, 2), (4, 1)]),
    frozenset([(2, 0), (3, 0), (4, 0), (4, 1), (4, 2)]),
    frozenset([(2, 0), (2, 1), (2, 2), (2, 3)]),
    frozenset([(2, 0), (2, 1), (3, 0), (3, 1)])
]

all_rocks = frozenset((x, 0) for x in range(7))
top_border = 0
jet_iteration = 0
total_offset = 0
len_jets = len(jets)

def print_rocks(shapeset):
    top = max(r[1] for r in all_rocks.union(shapeset))
    output = np.full((9, top + 3), ".")
    output[0] = "|"
    output[8] = "|"
    for rock in all_rocks:
        x = rock[0]
        y = rock[1]
        output[x + 1,y] = "#"
    for s in shapeset:
        x = s[0]
        y = s[1]
        output[x + 1,y] = "@"
    output[:,0] = "+------+".split()
    for row in output.T[::-1]:
        print("".join(row))

# Clockwise directions
# directions = ['right', 'down-right', 'down', 'down-left', 'left', 'up-left', 'up', 'up-right']
directions = [(1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1)]

def find_border(curr, direction_i, path):    
    new_path = path.copy()
    new_path.add(curr)

    # down-left, left, up-left,up
    num_directions = 4 if curr[0] == 6 else 7

    for i in range(num_directions):
        # Can't go backwards
        # Start 5 forward from where u were
        potential_direction_i = (direction_i + i + 5) % 8
        potential_direction = directions[potential_direction_i]
        potential_rock = (curr[0] + potential_direction[0], curr[1] + potential_direction[1])
        if potential_rock in all_rocks:
            border = find_border(potential_rock, potential_direction_i, new_path)
            if border[1]:
                if potential_rock[0] == 6:
                    return (border[0], False)
                new_path.update(border[0])
            else:
                return (border[0], False)
    # Deadend - aka its a tail that will be part of the correct answer
    return (new_path, True)

def remove_rocks():
    # start with top-left, go around "left" - keep track of direction, go til right wall - this is our new floor
    top_left_rock_y = 0
    for x, y in all_rocks:
        if x == 0 and y > top_left_rock_y:
            top_left_rock_y = y
    
    curr = (0, top_left_rock_y)
    border = find_border(curr, 2, set())[0]
    return border

cache = {}

def move_shape(shape, jet_iteration, rocks, shape_iteration):
    # returns (new shape position, if move is over)

    jet = jets[jet_iteration]
    # We've found our pattern, go to the endgame
    if (shape, jet_iteration, rocks) in cache:
        return (None, cache[(shape, jet_iteration, rocks)])

    min_x = 6
    max_x = 0
    for rock in shape:
        x = rock[0]
        if x < min_x:
            min_x = x
        if x > max_x:
            max_x = x

    if jet == ">" and max_x != 6:
        shifted_right = frozenset((rock[0] + 1, rock[1]) for rock in shape)
        if rocks.isdisjoint(shifted_right):
            shape = shifted_right
    elif jet == "<" and min_x != 0:
        shifted_left = frozenset((rock[0] - 1, rock[1]) for rock in shape)
        if rocks.isdisjoint(shifted_left):
            shape = shifted_left

    shifted_down = frozenset((rock[0] , rock[1] - 1) for rock in shape)
    rock_can_move_down = rocks.isdisjoint(shifted_down)
    if rock_can_move_down:
        result = (shifted_down, False)
    else:
        result = (shape, True)
    
    cache[(shape, jet_iteration, rocks)] = shape_iteration
    return result


iterations = 1000000000000
# iterations = 2022

height_before_move = []

for shape_iteration in range(iterations):
    s = shapes[shape_iteration % len(shapes)]
    s = frozenset((rock[0], rock[1] + 4 + top_border) for rock in s)

    height_before_move.append(top_border + total_offset)

    move_is_over = False
    while not move_is_over:
        s, move_is_over = move_shape(s, jet_iteration, all_rocks, shape_iteration)
        if s is None:
            #  Just kidding! "move_is_over" is actually the OG shape_iteration - this is actually our end logic
            first_shape_iteration = move_is_over
            cycle_length = shape_iteration - first_shape_iteration
            cycle_height = height_before_move[shape_iteration] - height_before_move[first_shape_iteration]

            position_in_cycle = (iterations - first_shape_iteration) % cycle_length
            number_of_cycles = (iterations - first_shape_iteration) // cycle_length

            extra_height = height_before_move[first_shape_iteration + position_in_cycle]

            final_height = number_of_cycles * cycle_height + extra_height

            print(final_height)
            exit()
        jet_iteration = (jet_iteration + 1) % len_jets
        
    s_top = max(rock[1] for rock in s)
    if s_top > top_border:
        top_border = s_top
    all_rocks = all_rocks.union(s)


    # Get the border
    all_rocks = remove_rocks()

    # Move everything to the bottom
    offset = min(rock[1] for rock in all_rocks)
    all_rocks = frozenset((rock[0], rock[1] - offset) for rock in all_rocks)
    top_border -= offset
    total_offset += offset
