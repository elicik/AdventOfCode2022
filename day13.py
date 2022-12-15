import re
import numpy as np
import math
import bisect
import functools

lines = []
with open("day13.txt") as input_file:
    lines = input_file.read().rstrip().split("\n")

# lines = [
# "[1,1,3,1,1]",
# "[1,1,5,1,1]",
# "",
# "[[1],[2,3,4]]",
# "[[1],4]",
# "",
# "[9]",
# "[[8,7,6]]",
# "",
# "[[4,4],4,4]",
# "[[4,4],4,4,4]",
# "",
# "[7,7,7,7]",
# "[7,7,7]",
# "",
# "[]",
# "[3]",
# "",
# "[[[]]]",
# "[[]]",
# "",
# "[1,[2,[3,[4,[5,6,7]]]],8,9]",
# "[1,[2,[3,[4,[5,6,0]]]],8,9]"
# ]

def compare(left, right):
    left_is_list = isinstance(left, list)
    right_is_list = isinstance(right, list)
    if not left_is_list and not right_is_list:
        if left < right:
            return True
        elif left > right:
            return False
        else:
            return None
    if left_is_list and right_is_list:
        i = 0
        while i < len(left) and i < len(right):
            result = compare(left[i], right[i])
            if result is not None:
                return result
            i += 1
        if len(left) < len(right):
            return True
        elif len(left) > len(right):
            return False
        else:
            return None
    if left_is_list and not right_is_list:
        return compare(left, [right])
    if not left_is_list and right_is_list:
        return compare([left], right)

line_groups = [lines[3*i:3*i+2] for i in range((len(lines) + 1 )// 3)]
lines = [[[2]], [[6]]]
indexes = []

for i in range(len(line_groups)):
    left = eval(line_groups[i][0])
    right = eval(line_groups[i][1])

    result = compare(left, right)
    if result:
        indexes.append(i+1)
    
    lines.append(left)
    lines.append(right)

print(sum(indexes))

lines.sort(key = functools.cmp_to_key(lambda a, b: -1 if compare(a, b) else 1))
divider_2 = lines.index([[2]]) + 1
divider_6 = lines.index([[6]]) + 1

print(divider_2 * divider_6)