import re
import numpy as np
import math
import bisect
import functools

lines = []
with open("day14.txt") as input_file:
    lines = input_file.read().rstrip().split("\n")

# lines = [
# "498,4 -> 498,6 -> 496,6",
# "503,4 -> 502,4 -> 502,9 -> 494,9"
# ]

rock = set()

for line in lines:
    points_str = line.split(" -> ")
    points = []
    for point in points_str:
        split_point = point.split(",")
        points.append((int(split_point[0]), int(split_point[1])))

    for i in range(1, len(points)):
        first = points[i-1]
        second = points[i]
        big_x = max(first[0], second[0])
        small_x = min(first[0], second[0])
        big_y = max(first[1], second[1])
        small_y = min(first[1], second[1])
        for x in range(small_x, big_x + 1):
            for y in range(small_y, big_y + 1):
                rock.add((x, y))

largest_y = max([r[1] for r in rock])
sand = set()

# Part 1
done = False
while not done:
    x = 500
    y = 0
    while True:
        if y >= largest_y:
            done = True
            break
        if (x, y + 1) not in rock and (x, y + 1) not in sand:
            y += 1
        elif (x - 1, y + 1) not in rock and (x - 1, y + 1) not in sand:
            x -= 1
            y += 1
        elif (x + 1, y + 1) not in rock and (x + 1, y + 1) not in sand:
            x += 1
            y += 1
        else:
            sand.add((x, y))
            break

print(len(sand))

# Part 2
sand = set()
floor = largest_y + 2
done = False
while not done:
    x = 500
    y = 0
    while True:
        if (x, y + 1) not in rock and (x, y + 1) not in sand and y + 1 != floor:
            y += 1
        elif (x - 1, y + 1) not in rock and (x - 1, y + 1) not in sand and y + 1 != floor:
            x -= 1
            y += 1
        elif (x + 1, y + 1) not in rock and (x + 1, y + 1) not in sand and y + 1 != floor:
            x += 1
            y += 1
        else:
            sand.add((x, y))
            if x == 500 and y == 0:
                done = True
            break

print(len(sand))