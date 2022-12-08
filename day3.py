lines = []
with open("day3.txt") as input_file:
    lines = input_file.read().strip().split("\n")
# lines = ["vJrwpWtwJgWrhcsFMMfFFhFp", "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL", "PmmdzqPrVvPwwTWBwg", "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn", "ttgJtRGJQctTZtZT", "CrZsJsPPZsGzwwsLwLmpwMDw"]

def priority(letter):
    conv = ord(letter)
    if conv >= 97:
        return conv - 96
    else:
        return conv - 38

total = 0
for line in lines:
    first = line[:len(line)//2]
    second = line[len(line)//2:]
    common = set(first).intersection(second).pop()
    total += priority(common)

print(total)

total = 0
for i in range(len(lines)//3):
    first = lines[3 * i]
    second = lines[3 * i + 1]
    third = lines[3 * i + 2]
    common = set(first).intersection(second).intersection(third).pop()
    total += priority(common)

print(total)