import re
import numpy as np
import math
import bisect
import functools
import time
import itertools
import copy

lines = []
with open("day19.txt") as input_file:
    lines = input_file.read().rstrip().split("\n")

# lines = [
# "Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.",
# "Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian."
# ]

blueprints = [None]

for line in lines:
    arr = re.match("Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.", line)
    bp = tuple([int(arr[i]) for i in range(1, 8)])
    blueprints.append(bp)

max_geodes = [0] * (len(blueprints) + 1)
max_ore_cost = [0] * (len(blueprints) + 1)
for bp in blueprints[1:]:
    id, ore_cost, clay_cost, obsidian_cost_ore, obsidian_cost_clay, geode_cost_ore, geode_cost_obsidian = bp
    for cost in [ore_cost, clay_cost, obsidian_cost_ore, geode_cost_ore]:
        if cost > max_ore_cost[id]:
            max_ore_cost[id] = cost

@functools.lru_cache(maxsize=None)
def loop_through_decisions(bp_id, state, minutes_left):
    id, ore_cost, clay_cost, obsidian_cost_ore, obsidian_cost_clay, geode_cost_ore, geode_cost_obsidian = blueprints[bp_id]
    ore, clay, obsidian, geodes, ore_robots, clay_robots, obsidian_robots, geode_robots = state

    # gr + (gr + 1) + (gr + 2)... = gr * ml + ml * (ml-1) / 2
    best_case = geodes + geode_robots * minutes_left + minutes_left * (minutes_left - 1) // 2
    if best_case < max_geodes[id]:
        return

    new_geodes = geodes + geode_robots
    if new_geodes > max_geodes[id]:
        max_geodes[id] = new_geodes

    if minutes_left == 1:
        # print(id, state)
        return

    decision_states = []

    decision_states.append((ore + ore_robots, clay + clay_robots, obsidian + obsidian_robots, geodes + geode_robots, ore_robots, clay_robots, obsidian_robots, geode_robots))

    if ore >= geode_cost_ore and obsidian >= geode_cost_obsidian:
        decision_states.append((ore + ore_robots - geode_cost_ore, clay + clay_robots, obsidian + obsidian_robots - geode_cost_obsidian, geodes + geode_robots, ore_robots, clay_robots, obsidian_robots, geode_robots + 1))
    if ore >= obsidian_cost_ore and clay >= obsidian_cost_clay and (minutes_left * obsidian_robots + obsidian) < minutes_left * geode_cost_obsidian:
        decision_states.append((ore + ore_robots - obsidian_cost_ore, clay + clay_robots - obsidian_cost_clay, obsidian + obsidian_robots, geodes + geode_robots, ore_robots, clay_robots, obsidian_robots + 1, geode_robots))
    if ore >= clay_cost and (minutes_left * clay_robots + clay) < minutes_left * obsidian_cost_clay:
        decision_states.append((ore + ore_robots - clay_cost, clay + clay_robots, obsidian + obsidian_robots, geodes + geode_robots, ore_robots, clay_robots + 1, obsidian_robots, geode_robots))
    if ore >= ore_cost and (minutes_left * ore_robots + ore) < minutes_left * max_ore_cost[id]:
        decision_states.append((ore + ore_robots - ore_cost, clay + clay_robots, obsidian + obsidian_robots, geodes + geode_robots, ore_robots + 1, clay_robots, obsidian_robots, geode_robots))

    for decision in decision_states:
        loop_through_decisions(bp_id, decision, minutes_left - 1)

total_quality = 0
for bp in blueprints[1:]:
    state = (0, 0, 0, 0, 1, 0, 0, 0)
    id = bp[0]
    loop_through_decisions(id, state, 24)
    quality = id * max_geodes[id]
    # print(id, quality)
    total_quality += quality

print("Part 1:", total_quality)

for bp in blueprints[1:4]:
    state = (0, 0, 0, 0, 1, 0, 0, 0)
    id = bp[0]
    loop_through_decisions(id, state, 32)
    # print(id, max_geodes[id])

part2_answer = math.prod(max_geodes[1:4])
print("Part 2:", part2_answer)