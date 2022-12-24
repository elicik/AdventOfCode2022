import numpy as np

lines = []
with open("day23.txt") as input_file:
    lines = input_file.read().rstrip().split("\n")

# lines = [
# "....#..",
# "..###.#",
# "#...#.#",
# ".#...##",
# "#.###..",
# "##.#.##",
# ".#..#.."
# ]

# Part 1:
rounds = 10

# Part 2
rounds = 2000


ground = np.full((len(lines), len(lines[0])), False)
elves = set()

for i, line in enumerate(lines):
    for j, char in enumerate(line):
        if char == "#":
            ground[i, j] = True
            elves.add((i+rounds, j+rounds))

def print_ground():
    for line in ground:
        print("".join(["#" if x else "." for x in line]))

ground = np.pad(ground, rounds)
# print_ground()
directions = ["north", "south", "west", "east"]

for r in range(rounds):
    proposed_moves = {}
    for elf in elves:
        # Do nothing for elves with no neighbors
        north = ground[elf[0]-1,elf[1]-1:elf[1]+2]
        south = ground[elf[0]+1,elf[1]-1:elf[1]+2]
        west = ground[elf[0]-1:elf[0]+2, elf[1]-1]
        east = ground[elf[0]-1:elf[0]+2, elf[1]+1]
        if any([any(x) for x in [north, south, west, east]]):
            for direction in directions:
                if direction == "north" and not any(north):
                    proposed_location = (elf[0] - 1, elf[1])
                    if proposed_location not in proposed_moves:
                        proposed_moves[proposed_location] = []
                    proposed_moves[proposed_location].append(elf)
                    break
                if direction == "south" and not any(south):
                    proposed_location = (elf[0] + 1, elf[1])
                    if proposed_location not in proposed_moves:
                        proposed_moves[proposed_location] = []
                    proposed_moves[proposed_location].append(elf)
                    break
                if direction == "west" and not any(west):
                    proposed_location = (elf[0], elf[1] -1)
                    if proposed_location not in proposed_moves:
                        proposed_moves[proposed_location] = []
                    proposed_moves[proposed_location].append(elf)
                    break
                if direction == "east" and not any(east):
                    proposed_location = (elf[0], elf[1] + 1)
                    if proposed_location not in proposed_moves:
                        proposed_moves[proposed_location] = []
                    proposed_moves[proposed_location].append(elf)
                    break

    for proposed_location in list(proposed_moves.keys()):
        if len(proposed_moves[proposed_location]) > 1:
            del proposed_moves[proposed_location]
    new_locations = list(proposed_moves.keys())
    old_locations = [loc[0] for loc in proposed_moves.values()]
    for loc in old_locations:
        ground[loc] = False
        elves.remove(loc)
    for loc in new_locations:
        ground[loc] = True
        elves.add(loc)
    directions = directions[1:] + [directions[0]]
    
    if len(new_locations) == 0:
        print(r + 1)
        break

if rounds == 10:
    min_row, min_col = np.min(np.array(list(elves)), axis=0)
    max_row, max_col = np.max(np.array(list(elves)), axis=0)
    print((max_row - min_row + 1) * (max_col - min_col + 1) - len(elves))
