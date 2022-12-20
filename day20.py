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
with open("day20.txt") as input_file:
    lines = input_file.read().rstrip().split("\n")

# lines = [
# "1",
# "2",
# "-3",
# "3",
# "-2",
# "0",
# "4"
# ]

length = len(lines)

class wrapped_int():
    def __init__(self, num):
        self.num = int(num)
        self.prev = None
        self.next = None

original_order = [wrapped_int(line) for line in lines]

zero = original_order[length - 1]
for i in range(length - 1):
    if original_order[i].num == 0:
        zero = original_order[i]
    original_order[i].next = original_order[i+1]
    original_order[i+1].prev = original_order[i]

original_order[length - 1].next = original_order[0]
original_order[0].prev = original_order[length - 1]

def print_arr_forwards(multiplier=1):
    curr = zero
    resulting_nums = []
    for i in range(length):
        resulting_nums.append(curr.num * multiplier)
        curr = curr.next
    print(resulting_nums)

decryption_key = 1
mix = 1

# Comment out for part 1
decryption_key = 811589153
mix = 10

for m in range(mix):
    for line in original_order:
        old_prev = line.prev
        old_next = line.next

        old_prev.next = old_next
        old_next.prev = old_prev

        new_prev = line.prev
        if line.num > 0:
            for i in range((decryption_key * line.num) % (length-1)):
                new_prev = new_prev.next
        else:
            for i in range((-decryption_key * line.num) % (length-1)):
                new_prev = new_prev.prev
        new_next = new_prev.next

        new_prev.next = line
        new_next.prev = line
        line.next = new_next
        line.prev = new_prev

curr = zero
output = []
for i in range(length):
    output.append(curr.num)
    curr = curr.next

first = output[1000 % length] * decryption_key
second = output[2000 % length] * decryption_key
third = output[3000 % length] * decryption_key

print(first + second + third)