import re

lines = []
with open("day5.txt") as input_file:
    lines = input_file.read().rstrip().split("\n")

# lines = [
# "    [D]    ",
# "[N] [C]    ",
# "[Z] [M] [P]",
# " 1   2   3 ",
# "",
# "move 1 from 2 to 1",
# "move 3 from 1 to 3",
# "move 2 from 2 to 1",
# "move 1 from 1 to 2"
# ]

stack_len = (len(lines[0]) + 1) // 4
stacks = [[] for i in range(stack_len)]

setting_up = True
for line in lines:
    if line == "":
        setting_up = False
        # remove number at end
        for stack in stacks:
            stack.pop()
        continue
    if setting_up:
        for i in range(stack_len):
            letter = line[4 * i + 1]
            if letter != " ":
                stacks[i].append(letter)
    else:
        match = re.match('move ([0-9]+) from ([0-9]) to ([0-9])', line)
        move = int(match[1])
        frm = int(match[2]) - 1
        to = int(match[3]) - 1

        letters = stacks[frm][:move]
        # Part 1:
        # stacks[to] = letters[::-1] + stacks[to]
        # Part 2:
        stacks[to] = letters + stacks[to]
        del stacks[frm][:move]

final = "".join([stack[0] for stack in stacks])
print(final)