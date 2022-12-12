import re
import numpy as np
import math

lines = []
with open("day11.txt") as input_file:
    lines = input_file.read().rstrip().split("\n")

# lines = [
# "Monkey 0:",
# "  Starting items: 79, 98",
# "  Operation: new = old * 19",
# "  Test: divisible by 23",
# "    If true: throw to monkey 2",
# "    If false: throw to monkey 3",
# "",
# "Monkey 1:",
# "  Starting items: 54, 65, 75, 74",
# "  Operation: new = old + 6",
# "  Test: divisible by 19",
# "    If true: throw to monkey 2",
# "    If false: throw to monkey 0",
# "",
# "Monkey 2:",
# "  Starting items: 79, 60, 97",
# "  Operation: new = old * old",
# "  Test: divisible by 13",
# "    If true: throw to monkey 1",
# "    If false: throw to monkey 3",
# "",
# "Monkey 3:",
# "  Starting items: 74",
# "  Operation: new = old + 3",
# "  Test: divisible by 17",
# "    If true: throw to monkey 0",
# "    If false: throw to monkey 1",
# ]

class monkey:
    def __init__(self, items, operation_str, divisible_by, true_location, false_location):
        self.items = items
        self.operation_str = operation_str
        self.divisible_by = divisible_by
        self.true_location = true_location
        self.false_location = false_location
        self.inspected = 0
    def do_operation(self, old):
        # operation = re.match("new = (.+)", self.operation_str)[1]
        # return eval(operation)
        if "+" in self.operation_str:
            operand = self.operation_str.split("+")[1].strip()
            return old + int(operand)
        elif "*" in self.operation_str:
            operand = self.operation_str.split("*")[1].strip()
            if operand == "old":
                return old * old
            else:
                return old * int(operand)
    def do_test(self, worry):
        return worry % self.divisible_by == 0

line_groups = [lines[7 * i:7 * i+6] for i in range((len(lines) + 1 )// 7)]
monkeys = []
divisors = 1

for line_group in line_groups:
    starting_items = re.match("  Starting items: (.+)", line_group[1])[1]
    starting_items = [int(i) for i in starting_items.split(", ")]
    operation = re.match("  Operation: (.+)", line_group[2])[1]
    test = re.match("  Test: (.+)", line_group[3])[1]
    divisible_by = int(re.match("divisible by ([0-9]+)", test)[1])
    divisors *= divisible_by
    true_location = int(re.match("    If true: throw to monkey ([0-9]+)", line_group[4])[1])
    false_location = int(re.match("    If false: throw to monkey ([0-9]+)", line_group[5])[1])
    monkeys.append(monkey(starting_items, operation, divisible_by, true_location, false_location))

# part 2:
rounds = 10000
# part 1: uncomment
# rounds = 20
for round in range(rounds):
    for monk in monkeys:
        while len(monk.items) != 0:
            item = monk.items.pop(0)
            monk.inspected += 1
            item = monk.do_operation(item)

            # part 1: uncomment
            # item = item // 3

            # part 2
            item = item % divisors

            new_location = monk.true_location if monk.do_test(item) else monk.false_location
            monkeys[new_location].items.append(item)

sorted_inspected = sorted([m.inspected for m in monkeys])
monkey_business = sorted_inspected[-1] * sorted_inspected[-2]

print(monkey_business)