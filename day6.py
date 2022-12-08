import re

lines = []
with open("day6.txt") as input_file:
    lines = input_file.read().rstrip().split("\n")

line = lines[0]

# line = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"
# Part 1:
# num = 4
# Part 2:
num = 14

for i in range(num - 1, len(line)):
    check = line[(i - num + 1):i+1]
    if len(set(check)) == num:
        print(i+1)
        break