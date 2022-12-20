import re
import math
import functools

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

remaining_labels = set(weighted_graph.keys())

# Floyd-Warshall
dist = { from_label : { to_label : math.inf for to_label in remaining_labels } for from_label in remaining_labels}
next = { from_label : { to_label : None for to_label in remaining_labels } for from_label in remaining_labels}

for from_label, tunnel_weights in weighted_graph.items():
    for tunnel, weight in tunnel_weights.items():
        dist[from_label][tunnel] = weight
        next[from_label][tunnel] = tunnel
for label in remaining_labels:
    dist[label][label] = 0
    next[label][label] = label
for k in remaining_labels:
    for i in remaining_labels:
        for j in remaining_labels:
            if dist[i][j] > dist[i][k] + dist[k][j]:
                dist[i][j] = dist[i][k] + dist[k][j]
                next[i][j] = next[i][k]

@functools.lru_cache(maxsize=None)
def get_pressure_from_ordering(ordering, minutes_left):
    if len(ordering) < 2 or minutes_left <= 0:
        return 0
    curr_valve = ordering[0]
    next_valve = ordering[1]
    distance = dist[curr_valve][next_valve]
    minutes_left -= distance + 1
    pressure = minutes_left * valves[next_valve].flow_rate
    return pressure + get_pressure_from_ordering(ordering[1:], minutes_left)


labels_without_start = remaining_labels.difference({"AA"})
# wait oh no this is TSP - we've got to reduce the n! time, here we just minimize the paths first
# held-karp algorithm-ish

# Lets us cut off paths sooner
def get_valid_paths(label, minutes_left, paths, valid_labels, max_length, add_short_paths):
    result = []
    for path in paths:
        for new_label in valid_labels:
            if new_label not in path:
                new_path = path + [new_label]
                new_minutes_left = minutes_left - dist[label][new_label] - 1
                if add_short_paths:
                    result.append(new_path)
                if new_minutes_left < 0:
                    result.append(path)
                elif len(new_path) == max_length and not add_short_paths:
                    result.append(new_path)
                else:
                    next_paths = get_valid_paths(new_label, new_minutes_left, [new_path], valid_labels, max_length, add_short_paths)
                    result.extend(next_paths)
    return result

valid_paths_part1 = get_valid_paths("AA", 30, [[]], labels_without_start, len(labels_without_start), False)
valid_paths_part2 = get_valid_paths("AA", 26, [[]], labels_without_start, len(labels_without_start) // 2 + 1, True)
len_part2 = len(valid_paths_part2)

max_pressure = 0
for ordering_without_aa in valid_paths_part1:
    minutes_left = 30
    ordering = tuple(["AA"] + ordering_without_aa)
    pressure = get_pressure_from_ordering(ordering, minutes_left)
    if pressure > max_pressure:
        max_pressure = pressure
print(max_pressure)



max_pressure = 0
for i, my_ordering_without_aa in enumerate(valid_paths_part2):
    # if i % 100 == 0:
        # print(i, "/", len_part2)
    my_length = len(my_ordering_without_aa)
    max_length = len(labels_without_start) - my_length
    elephants_labels_taken = labels_without_start.difference(my_ordering_without_aa)
    valid_elephant_paths = get_valid_paths("AA", 26, [[]], elephants_labels_taken, len(elephants_labels_taken), False)

    for elephants_ordering_without_aa in valid_elephant_paths:
        my_minutes_left = 26
        elephants_minutes_left = 26
        my_ordering = tuple(["AA"] + my_ordering_without_aa)
        elephants_ordering = tuple(["AA"] + elephants_ordering_without_aa)

        pressure = get_pressure_from_ordering(my_ordering, my_minutes_left) + get_pressure_from_ordering(elephants_ordering, elephants_minutes_left)
        if pressure > max_pressure:
            max_pressure = pressure

print(max_pressure)