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
with open("day21.txt") as input_file:
    lines = input_file.read().rstrip().split("\n")

# lines = [
# "root: pppw + sjmn",
# "dbpl: 5",
# "cczh: sllz + lgvd",
# "zczc: 2",
# "ptdq: humn - dvpt",
# "dvpt: 3",
# "lfqf: 4",
# "humn: 5",
# "ljgn: 2",
# "sjmn: drzm * dbpl",
# "sllz: 4",
# "pppw: cczh / lfqf",
# "lgvd: ljgn * ptdq",
# "drzm: hmdt - zczc",
# "hmdt: 32"
# ]

unknown_monkeys = {}
known_monkeys = {}

for line in lines:
    arr = re.match("(\w+): (?:(\d+)|(?:(\w+) ([+\-/\*]) (\w+)))", line)
    name, num, first_operand, operation, second_operand = arr[1], arr[2], arr[3], arr[4], arr[5]
    if num is not None:
        known_monkeys[name] = int(num)
    else:
        unknown_monkeys[name] = (first_operand, operation, second_operand)

known_monkeys_part1 = known_monkeys.copy()
def monkey_yelled(name):
    if name in known_monkeys_part1:
        return known_monkeys_part1[name]
    first_operand, operation, second_operand = unknown_monkeys[name]
    first_yelled = monkey_yelled(first_operand)
    second_yelled = monkey_yelled(second_operand)
    if operation == "+":
        result = first_yelled + second_yelled
        known_monkeys_part1[name] = result
        return result
    if operation == "-":
        result = first_yelled - second_yelled
        known_monkeys_part1[name] = result
        return result
    if operation == "*":
        result = first_yelled * second_yelled
        known_monkeys_part1[name] = result
        return result
    if operation == "/":
        result = first_yelled // second_yelled
        known_monkeys_part1[name] = result
        return result

print(monkey_yelled("root"))

tree = {}

class polynomial:
    def __init__(self, coefficients):
        # backwards order - [1] = num, [0, 1] = humn
        self.coefficients = coefficients
        self.len = len(coefficients)
    def minimize(self):
        for i in range(self.len - 1, -1, -1):
            if self.coefficients[i] != 0:
                self.len = i + 1
                self.coefficients = self.coefficients[:self.len]
                return
        self.coefficients = [0]
        self.len = 1
    def __getitem__(self, key):
        return self.coefficients[key]
    def __add__(self, other):
        max_len = max(self.len, other.len)
        coefficients = []
        for i in range(max_len):
            a = self[i] if i < self.len else 0
            b = other[i] if i < other.len else 0
            coefficients.append(a + b)
        result = polynomial(coefficients)
        result.minimize()
        return result
    def __sub__(self, other):
        max_len = max(self.len, other.len)
        coefficients = []
        for i in range(max_len):
            a = self[i] if i < self.len else 0
            b = other[i] if i < other.len else 0
            coefficients.append(a - b)
        result = polynomial(coefficients)
        result.minimize()
        return result
    def __mul__(self, other):
        new_len = self.len * other.len
        coefficients = [0] * new_len
        for i in range(self.len):
            for j in range(other.len):
                coefficients[i+j] += self[i] * other[j]
        result = polynomial(coefficients)
        result.minimize()
        return result
    def __truediv__(self, other):
        # Polynomial long division algorithm from wikipedia
        if other.len == 1 and other[0] == 0:
            print("uhoh divide by 0")
            exit(0)
        q = polynomial([0] * self.len)
        r = polynomial(self.coefficients.copy())
        while not (r.len == 1 and r[0] == 0) and r.len >= other.len:
            lead_r = r.coefficients[-1]
            lead_other = other.coefficients[-1]
            degree = r.len - other.len
            t = polynomial([0] * degree + [lead_r / lead_other])
            t.minimize()
            q = q + t
            r = r - (t * other)
            r.minimize()
        if other.len == 1 and other[0] == 0:
            print("uhoh gotta keep track of remainder")
            exit(0)
        q.minimize()
        return q

known_monkeys_part2 = {}

def monkey_yelled_part2(name):
    if name in known_monkeys_part2:
        return known_monkeys_part2[name]
    if name == "humn":
        known_monkeys_part2[name] = polynomial([0, 1])
        return known_monkeys_part2[name]
    if name in known_monkeys:
        known_monkeys_part2[name] = polynomial([known_monkeys[name]])
        return known_monkeys_part2[name]

    first_operand, operation, second_operand = unknown_monkeys[name]
    first_yelled = monkey_yelled_part2(first_operand)
    second_yelled = monkey_yelled_part2(second_operand)
    # print(first_yelled.coefficients, operation, second_yelled.coefficients)
    if operation == "+":
        result = first_yelled + second_yelled
    if operation == "-":
        result = first_yelled - second_yelled
    if operation == "*":
        result = first_yelled * second_yelled
    if operation == "/":
        result = first_yelled / second_yelled
    known_monkeys_part2[name] = result
    # print("=", result.coefficients)
    return result

root_a, _, root_b = unknown_monkeys["root"]
zero = monkey_yelled_part2(root_a) - monkey_yelled_part2(root_b)

# Assume the answer is linear
humn = -zero[0]/zero[1]
print(int(humn))