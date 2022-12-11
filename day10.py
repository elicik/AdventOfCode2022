import re
import numpy as np
import math

lines = []
with open("day10.txt") as input_file:
    lines = input_file.read().rstrip().split("\n")

# lines = [
# "addx 15",
# "addx -11",
# "addx 6",
# "addx -3",
# "addx 5",
# "addx -1",
# "addx -8",
# "addx 13",
# "addx 4",
# "noop",
# "addx -1",
# "addx 5",
# "addx -1",
# "addx 5",
# "addx -1",
# "addx 5",
# "addx -1",
# "addx 5",
# "addx -1",
# "addx -35",
# "addx 1",
# "addx 24",
# "addx -19",
# "addx 1",
# "addx 16",
# "addx -11",
# "noop",
# "noop",
# "addx 21",
# "addx -15",
# "noop",
# "noop",
# "addx -3",
# "addx 9",
# "addx 1",
# "addx -3",
# "addx 8",
# "addx 1",
# "addx 5",
# "noop",
# "noop",
# "noop",
# "noop",
# "noop",
# "addx -36",
# "noop",
# "addx 1",
# "addx 7",
# "noop",
# "noop",
# "noop",
# "addx 2",
# "addx 6",
# "noop",
# "noop",
# "noop",
# "noop",
# "noop",
# "addx 1",
# "noop",
# "noop",
# "addx 7",
# "addx 1",
# "noop",
# "addx -13",
# "addx 13",
# "addx 7",
# "noop",
# "addx 1",
# "addx -33",
# "noop",
# "noop",
# "noop",
# "addx 2",
# "noop",
# "noop",
# "noop",
# "addx 8",
# "noop",
# "addx -1",
# "addx 2",
# "addx 1",
# "noop",
# "addx 17",
# "addx -9",
# "addx 1",
# "addx 1",
# "addx -3",
# "addx 11",
# "noop",
# "noop",
# "addx 1",
# "noop",
# "addx 1",
# "noop",
# "noop",
# "addx -13",
# "addx -19",
# "addx 1",
# "addx 3",
# "addx 26",
# "addx -30",
# "addx 12",
# "addx -1",
# "addx 3",
# "addx 1",
# "noop",
# "noop",
# "noop",
# "addx -9",
# "addx 18",
# "addx 1",
# "addx 2",
# "noop",
# "noop",
# "addx 9",
# "noop",
# "noop",
# "noop",
# "addx -1",
# "addx 2",
# "addx -37",
# "addx 1",
# "addx 3",
# "noop",
# "addx 15",
# "addx -21",
# "addx 22",
# "addx -6",
# "addx 1",
# "noop",
# "addx 2",
# "addx 1",
# "noop",
# "addx -10",
# "noop",
# "noop",
# "addx 20",
# "addx 1",
# "addx 2",
# "addx 2",
# "addx -6",
# "addx -11",
# "noop",
# "noop",
# "noop"
# ]

x = 1
total = 0
cycle = 0

crt = ["."] * 240

for line in lines:
    if line == "noop":
        cycle += 1
        if (cycle + 20) % 40 == 0:
            total += cycle * x
        if abs(x - cycle % 40 + 1) <= 1:
            crt[cycle - 1] = "#"
        else:
            crt[cycle - 1] = "."
    else:
        v = int(line[5:])
        for i in range(2):
            cycle += 1
            if (cycle + 20) % 40 == 0:
                total += cycle * x
            if abs(x - cycle % 40 + 1) <= 1:
                crt[cycle - 1] = "#"
            else:
                crt[cycle - 1] = "."
        x += v

# part 1:
print(total)

# part 2:
crt_lines = ["".join(crt[40 * i:40 * i+40]) for i in range(len(crt) // 40)]
for line in crt_lines:
    print(line)