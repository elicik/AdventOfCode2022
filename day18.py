import re
import numpy as np
import math
import bisect
import functools
import time
import itertools
import copy

lines = []
with open("day18.txt") as input_file:
    lines = input_file.read().rstrip().split("\n")

# lines = [
# "2,2,2",
# "1,2,2",
# "3,2,2",
# "2,1,2",
# "2,3,2",
# "2,2,1",
# "2,2,3",
# "2,2,4",
# "2,2,6",
# "1,2,5",
# "3,2,5",
# "2,1,5",
# "2,3,5"
# ]

cubes = []
for line in lines:
    cubes.append(tuple(int(i) for i in line.split(",")))

min_x = math.inf
min_y = math.inf
min_z = math.inf
max_x = -math.inf
max_y = -math.inf
max_z = -math.inf

for cube in cubes:
    if cube[0] > max_x:
        max_x = cube[0]
    if cube[0] < min_x:
        min_x = cube[0]
    if cube[1] > max_y:
        max_y = cube[1]
    if cube[1] < min_y:
        min_y = cube[1]
    if cube[2] > max_z:
        max_z = cube[2]
    if cube[2] < min_z:
        min_z = cube[2]

size = (max_x - min_x + 3, max_y - min_y + 3, max_z - min_z + 3)

# now we use a numpy 3d array
grid = np.full(size, False)
for cube in cubes:
    x, y, z = cube
    x = x - min_x + 1
    y = y - min_y + 1
    z = z - min_z + 1
    grid[x, y, z] = True

# part 1
total = 6 * len(cubes)
for cube in cubes:
    x, y, z = cube
    x = x - min_x + 1
    y = y - min_y + 1
    z = z - min_z + 1
    bordering_cubes = sum([grid[x, y, z+1], grid[x, y+1, z], grid[x+1, y, z], grid[x, y, z-1], grid[x, y-1, z], grid[x-1, y, z]])
    total -= bordering_cubes

print(total)
# part 2

# Find all the interior spaces (can't find a way out)
for x in range(1, size[0] - 1):
    for y in range(1, size[1] - 1):
        for z in range(1, size[2] - 1):
            # if it's a cube, it's not an interior space
            if grid[x, y, z]:
                continue
            # if we can go straight out in a direction, we're fine
            can_go_right = not np.any(grid[x+1:,y,z])
            if can_go_right:
                continue
            can_go_left = not np.any(grid[:x,y,z])
            if can_go_left:
                continue
            can_go_up = not np.any(grid[x,y+1:,z])
            if can_go_up:
                continue
            can_go_down = not np.any(grid[x,:y,z])
            if can_go_down:
                continue
            can_go_forward = not np.any(grid[x,y,z+1:])
            if can_go_forward:
                continue
            can_go_backward = not np.any(grid[x,y,:z])
            if can_go_backward:
                continue
            
            # BFS
            queue = [(x, y, z)]
            checked = set()
            trapped = True
            while len(queue) != 0:
                cube = queue.pop(0)

                left = (cube[0]-1, cube[1], cube[2])
                right = (cube[0]+1, cube[1], cube[2])
                down = (cube[0], cube[1]-1, cube[2])
                up = (cube[0], cube[1]+1, cube[2])
                backward = (cube[0], cube[1], cube[2]-1)
                forward = (cube[0], cube[1], cube[2]+1)

                if left[0] == 0 or right[0] == size[0] - 1 or down[1] == 0 or up[1] == size[1] - 1 or backward[2] == 0 or forward[2] == size[2] - 1:
                    trapped = False
                    break

                checked.add(cube)
                if not grid[left] and left not in checked and left not in queue:
                    queue.append(left)
                if not grid[right] and right not in checked and right not in queue:
                    queue.append(right)
                if not grid[down] and down not in checked and down not in queue:
                    queue.append(down)
                if not grid[up] and up not in checked and up not in queue:
                    queue.append(up)
                if not grid[backward] and backward not in checked and backward not in queue:
                    queue.append(backward)
                if not grid[forward] and forward not in checked and forward not in queue:
                    queue.append(forward)

            # if it's interior, just add it to the grid
            if trapped:
                for cube in checked:
                    grid[cube] = True

total = 6 * len(cubes)
for cube in cubes:
    x, y, z = cube
    x = x - min_x + 1
    y = y - min_y + 1
    z = z - min_z + 1
    bordering_cubes = sum([grid[x, y, z+1], grid[x, y+1, z], grid[x+1, y, z], grid[x, y, z-1], grid[x, y-1, z], grid[x-1, y, z]])
    total -= bordering_cubes

print(total)