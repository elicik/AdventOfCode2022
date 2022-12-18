# DAY 16 PART 2 NOT COMPLETED

import re
import numpy as np
import math
import bisect
import functools
import time
import itertools

lines = []
with open("day16.txt") as input_file:
    lines = input_file.read().rstrip().split("\n")

lines = [
"Valve AA has flow rate=0; tunnels lead to valves DD, II, BB",
"Valve BB has flow rate=13; tunnels lead to valves CC, AA",
"Valve CC has flow rate=2; tunnels lead to valves DD, BB",
"Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE",
"Valve EE has flow rate=3; tunnels lead to valves FF, DD",
"Valve FF has flow rate=0; tunnels lead to valves EE, GG",
"Valve GG has flow rate=0; tunnels lead to valves FF, HH",
"Valve HH has flow rate=22; tunnel leads to valve GG",
"Valve II has flow rate=0; tunnels lead to valves AA, JJ",
"Valve JJ has flow rate=21; tunnel leads to valve II"
]

class valve:
    def __init__(self, label, flow_rate, tunnels):
        self.label = label
        self.flow_rate = flow_rate
        self.tunnels = tunnels

labels = []
valves = {}
for line in lines:
    arr = re.match("Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.+)", line)
    label = arr[1]

    valves[label] = valve(label, int(arr[2]), sorted(arr[3].split(", ")))
    labels.append(label)


pressure_map = {}

def get_pressure(label, open_valves, minutes_left):
    if minutes_left == 0:
        return 0
    if (label, open_valves, minutes_left) in pressure_map:
        return pressure_map[(label, open_valves, minutes_left)]

    max_pressure = 0

    if label not in open_valves and valves[label].flow_rate != 0:
        new_open_valves = open_valves.union({label})
        pressure = (minutes_left - 1) * valves[label].flow_rate + get_pressure(label, new_open_valves, minutes_left - 1)
        if pressure > max_pressure:
            max_pressure = pressure

    for tunnel in valves[label].tunnels:
        pressure = get_pressure(tunnel, open_valves, minutes_left - 1)
        if pressure > max_pressure:
            max_pressure = pressure

    pressure_map[(label, open_valves, minutes_left)] = max_pressure
    # print(label, open_valves, minutes_left, max_pressure)
    return max_pressure

print(get_pressure("AA", frozenset(), 30))

pressure_map = {}
all_possible_open = frozenset(label for label in labels if valves[label].flow_rate == 0)

def get_pressure_with_elephant(my_label, elephants_label, open_valves, minutes_left):
    if minutes_left == 0:
        return 0
    if (my_label, elephants_label, open_valves, minutes_left) in pressure_map:
        return pressure_map[(my_label, elephants_label, open_valves, minutes_left)]

    max_pressure = 0
    if open_valves == all_possible_open:
        return 0

    for my_tunnel in valves[my_label].tunnels:
        for elephants_tunnel in valves[elephants_label].tunnels:
            pressure = get_pressure_with_elephant(my_tunnel, elephants_tunnel, open_valves, minutes_left - 1)
            if pressure > max_pressure:
                max_pressure = pressure

    for elephants_tunnel in valves[elephants_label].tunnels:
        if my_label not in open_valves and valves[my_label].flow_rate != 0:
            new_open_valves = open_valves.union({my_label})
            pressure = (minutes_left - 1) * valves[my_label].flow_rate + get_pressure_with_elephant(my_label, elephants_tunnel, new_open_valves, minutes_left - 1)
            if pressure > max_pressure:
                max_pressure = pressure


    for my_tunnel in valves[my_label].tunnels:
        if elephants_label not in open_valves and valves[elephants_label].flow_rate != 0:
            new_open_valves = open_valves.union({elephants_label})
            pressure = (minutes_left - 1) * valves[elephants_label].flow_rate + get_pressure_with_elephant(my_tunnel, elephants_label, new_open_valves, minutes_left - 1)
            if pressure > max_pressure:
                max_pressure = pressure

    if my_label not in open_valves and valves[my_label].flow_rate != 0 and elephants_label not in open_valves and valves[elephants_label].flow_rate != 0 and my_label != elephants_label:
        new_open_valves = open_valves.union({my_label, elephants_label})
        pressure = (minutes_left - 1) * (valves[my_label].flow_rate + valves[elephants_label].flow_rate) + get_pressure_with_elephant(my_label, elephants_label, new_open_valves, minutes_left - 1)
        if pressure > max_pressure:
            max_pressure = pressure

    pressure_map[(my_label, elephants_label, open_valves, minutes_left)] = max_pressure
    # print(label, open_valves, minutes_left, max_pressure)
    return max_pressure

print(get_pressure_with_elephant("AA", "AA", frozenset(), 26))














# make smaller graph
weighted_graph = {}
valves_to_delete = []
for label in labels:
    weighted_graph[label] = { tunnel: 1 for tunnel in valves[label].tunnels}
    if valves[label].flow_rate == 0 and label != "AA":
        valves_to_delete.append(label)


for valve_to_delete in valves_to_delete:
    tunnels = list(weighted_graph[valve_to_delete].keys())
    for label in tunnels:
        # Go to the connection - add all of the other nodes as a connection to it
        weight_from_label_to_valve_to_delete = weighted_graph[label][valve_to_delete]
        for tunnel in tunnels:
            if tunnel != label:
                weight_from_valve_to_delete_to_tunnel = weighted_graph[valve_to_delete][tunnel]
                combined_weight = weight_from_label_to_valve_to_delete + weight_from_valve_to_delete_to_tunnel
                existing_weight_of_label_to_tunnel = weighted_graph[label].get(tunnel, math.inf)
                if combined_weight < existing_weight_of_label_to_tunnel:
                    weighted_graph[label][tunnel] = combined_weight
        del weighted_graph[label][valve_to_delete]
    del weighted_graph[valve_to_delete]
# print(weighted_graph)
# print(len(weighted_graph))

part1_pressure_map = {}
def get_pressure_fast(label, open_valves, minutes_left):
    if minutes_left <= 0:
        return 0
    if (label, open_valves, minutes_left) in part1_pressure_map:
        return part1_pressure_map[(label, open_valves, minutes_left)]

    max_pressure = 0

    if label not in open_valves:
        new_open_valves = open_valves.union({label})
        pressure = (minutes_left - 1) * valves[label].flow_rate + get_pressure_fast(label, new_open_valves, minutes_left - 1)
        if pressure > max_pressure:
            max_pressure = pressure

    for tunnel, weight in weighted_graph[label].items():
        pressure = get_pressure_fast(tunnel, open_valves, minutes_left - weight)
        if pressure > max_pressure:
            max_pressure = pressure

    part1_pressure_map[(label, open_valves, minutes_left)] = max_pressure
    # print(label, open_valves, minutes_left, max_pressure)
    return max_pressure

print(get_pressure_fast("AA", frozenset(), 30))

part2_pressure_map = {}
def get_pressure_with_elephant_fast(my_label, elephants_label, open_valves, my_minutes_left, elephants_minutes_left):
    if my_minutes_left <= 0 or elephants_minutes_left <= 0:
        return 0
        # return get_pressure_fast(elephants_label, open_valves, elephants_minutes_left) + get_pressure_fast(my_label, open_valves, my_minutes_left)

    if (my_label, elephants_label, open_valves, my_minutes_left, elephants_minutes_left) in part2_pressure_map:
        return part2_pressure_map[(my_label, elephants_label, open_valves, my_minutes_left, elephants_minutes_left)]

    if open_valves == all_possible_open:
        return 0
    max_pressure = 0

    for my_tunnel, my_weight in weighted_graph[my_label].items():
        for elephants_tunnel, elephants_weight in weighted_graph[elephants_label].items():
            pressure = get_pressure_with_elephant_fast(my_tunnel, elephants_tunnel, open_valves, my_minutes_left - my_weight, elephants_minutes_left - elephants_weight)
            if pressure > max_pressure:
                max_pressure = pressure

    for elephants_tunnel, elephants_weight in weighted_graph[elephants_label].items():
        if my_label not in open_valves:
            new_open_valves = open_valves.union({my_label})
            pressure = (my_minutes_left - 1) * valves[my_label].flow_rate + get_pressure_with_elephant_fast(my_label, elephants_tunnel, new_open_valves, my_minutes_left - 1, elephants_minutes_left - elephants_weight)
            if pressure > max_pressure:
                max_pressure = pressure

    for my_tunnel, my_weight in weighted_graph[my_label].items():
        if elephants_label not in open_valves and valves[elephants_label].flow_rate != 0:
            new_open_valves = open_valves.union({elephants_label})
            pressure = (elephants_minutes_left - 1) * valves[elephants_label].flow_rate + get_pressure_with_elephant_fast(my_tunnel, elephants_label, new_open_valves, my_minutes_left - my_weight, elephants_minutes_left - 1)
            if pressure > max_pressure:
                max_pressure = pressure

    if my_label not in open_valves and elephants_label not in open_valves and my_label != elephants_label:
        new_open_valves = open_valves.union({my_label, elephants_label})
        pressure = (my_minutes_left - 1) * valves[my_label].flow_rate + (elephants_minutes_left - 1) * valves[elephants_label].flow_rate + get_pressure_with_elephant_fast(my_label, elephants_label, new_open_valves, my_minutes_left - 1, elephants_minutes_left - 1)
        if pressure > max_pressure:
            max_pressure = pressure

    part2_pressure_map[(my_label, elephants_label, open_valves, my_minutes_left, elephants_minutes_left)] = max_pressure
    return max_pressure

print(get_pressure_with_elephant_fast("AA", "AA", frozenset(), 26, 26))



# adj = np.full((len(labels), len(labels)), 0)
# for i in range(len(labels)):
#     for tunnel in valves[labels[i]].tunnels:
#         j = labels.index(tunnel)
#         adj[i, j] = 1
#     print(", ".join([str(x) for x in adj[i]]))
# exit()

# def paths_to_goal(start_label, end_label, path):
#     new_path = path.copy()
#     new_path.append(start_label)
#     if new_path[-1] == end_label:
#         return [new_path]
#     paths = []
#     for tunnel in valves[start_label].tunnels:
#         if tunnel not in path:
#             paths.extend(paths_to_goal(tunnel, end_label, new_path))
#     paths = [p for p in paths if p is not None]
#     if len(paths) == 0:
#         # Dead end
#         return [None]
#     min_path_length = min(len(p) for p in paths)
#     return [p for p in paths if len(p) == min_path_length]

# valid_tunnels = { label : {} for label in labels}
# for start_label, end_label in itertools.permutations(labels, 2):
#     # Lazy DFS
#     paths = paths_to_goal(start_label, end_label, [])
#     valid_tunnels[start_label][end_label] = set(path[1] for path in paths)

# # current valve, minutes left, pressure
# def get_best_case(minutes_left, pressure):
#     return pressure + minutes_left * sum(valves[label].flow_rate for label in labels)

# def get_worst_case(minutes_left, pressure, valve_states):
#     return pressure + minutes_left * sum(valves[label].flow_rate if valve_states[label] else 0 for label in labels)

# def get_good_tunnels(start_label, valve_states):
#     sets = [valid_tunnels[start_label][end_label] for end_label in labels if valve_states[end_label] == False and end_label != start_label]
#     return set.union(*sets)

# possibilities = {} # [minutes_left][label] = (pressure, valve_states, best_case, worst_case)
# max_worst_case = {}
# for minutes_left in range(31):
#     possibilities[minutes_left] = {}
#     max_worst_case[minutes_left] = {}
#     for label in labels:
#         possibilities[minutes_left][label] = []
#         max_worst_case[minutes_left][label] = 0

# closed_valve_states = { label: True if valves[label].flow_rate == 0 else False for label in labels}

# possibilities[30]["AA"].append((0, closed_valve_states))

# for minutes_left in range(30, 0, -1):
#     print(minutes_left)
#     max_pressure = 0
#     for label in labels:
#         options = possibilities[minutes_left][label]
#         for option in options:
#             if option[0] > max_pressure:
#                 max_pressure = option[0]
#     print(max_pressure)
#     for label in labels:
#         options = possibilities[minutes_left][label]
#         if len(options) != 0:
#             print(minutes_left, label, len(options))
#         for option in options:
#             (pressure, valve_states) = option
#             new_pressure = pressure + sum(valves[v].flow_rate if valve_states[v] else 0 for v in labels)
#             # num_open_valves = list(valve_states.values()).count(False)
#             if not valve_states[label]:
#                 new_valve_states = valve_states.copy()
#                 new_valve_states[label] = True
#                 if all(new_valve_states.values()):
#                     best_case = get_best_case(minutes_left - 1, new_pressure)
#                     possibilities[0][label].append((best_case, new_valve_states))
#                     continue
#                 else:
#                     new_worst_case = get_worst_case(minutes_left - 1, new_pressure, new_valve_states)
#                     if new_worst_case > max_worst_case[minutes_left - 1][label]:
#                         # its definitely fine
#                         max_worst_case[minutes_left - 1][label] = new_worst_case
#                         possibilities[minutes_left - 1][label].append((new_pressure, new_valve_states))
#                     else:
#                         # its maybe fine
#                         new_best_case = get_best_case(minutes_left - 1, new_pressure)
#                         if new_best_case >= max_worst_case[minutes_left - 1][label]:
#                             possibilities[minutes_left - 1][label].append((new_pressure, new_valve_states))
            
#             # if num_open_valves == 1:
#             #     if valve_states[label]:
#             #         # Follow one of the shortest paths
#             #         final_open_valve = [v for v in labels if valve_states[v] == False][0]
#             #         tunnel = best_paths_to_last_open_valve[label][final_open_valve][1]
#             #         possibilities[minutes_left - 1][tunnel].append((new_pressure, valve_states))
#             # else:
#             new_worst_case = get_worst_case(minutes_left - 1, new_pressure, valve_states)
#             # tunnels = get_good_tunnels(label, valve_states)
#             # for tunnel in tunnels:
#             for tunnel in valves[label].tunnels:
#                 if new_worst_case > max_worst_case[minutes_left - 1][tunnel]:
#                     # its definitely fine
#                     max_worst_case[minutes_left - 1][tunnel] = new_worst_case
#                     possibilities[minutes_left - 1][tunnel].append((new_pressure, valve_states))
#                 else:
#                     # its maybe fine
#                     new_best_case = get_best_case(minutes_left - 1, new_pressure)
#                     if new_best_case >= max_worst_case[minutes_left - 1][tunnel]:
#                         possibilities[minutes_left - 1][tunnel].append((new_pressure, valve_states))

#         # keep our storage small
#         del possibilities[minutes_left][label]

# flatten final pressures
# max_pressure = 0
# for label in labels:
#     options = possibilities[0][label]
#     for option in options:
#         if option[0] > max_pressure:
#             max_pressure = option[0]
# print(max_pressure)