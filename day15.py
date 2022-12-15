import re

lines = []
with open("day15.txt") as input_file:
    lines = input_file.read().rstrip().split("\n")

row = 2000000
max_x_y = 4000000

# lines = [
# "Sensor at x=2, y=18: closest beacon is at x=-2, y=15",
# "Sensor at x=9, y=16: closest beacon is at x=10, y=16",
# "Sensor at x=13, y=2: closest beacon is at x=15, y=3",
# "Sensor at x=12, y=14: closest beacon is at x=10, y=16",
# "Sensor at x=10, y=20: closest beacon is at x=10, y=16",
# "Sensor at x=14, y=17: closest beacon is at x=10, y=16",
# "Sensor at x=8, y=7: closest beacon is at x=2, y=10",
# "Sensor at x=2, y=0: closest beacon is at x=2, y=10",
# "Sensor at x=0, y=11: closest beacon is at x=2, y=10",
# "Sensor at x=20, y=14: closest beacon is at x=25, y=17",
# "Sensor at x=17, y=20: closest beacon is at x=21, y=22",
# "Sensor at x=16, y=7: closest beacon is at x=15, y=3",
# "Sensor at x=14, y=3: closest beacon is at x=15, y=3",
# "Sensor at x=20, y=1: closest beacon is at x=15, y=3"
# ]
# row = 10
# max_x_y = 20

x_not_beacon = set()
x_beacon = set()

sensors = []

for line in lines:
    arr = re.match("Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)", line)
    sensor_x = int(arr[1])
    sensor_y = int(arr[2])
    beacon_x = int(arr[3])
    beacon_y = int(arr[4])
    distance = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)
    sensors.append((sensor_x, sensor_y, distance))
    if beacon_y == row:
        x_beacon.add(beacon_x)

# Part 1
for sensor in sensors:
    sensor_x, sensor_y, distance = sensor
    distance_from_row = abs(sensor_y - row)
    distance_remaining = distance - distance_from_row
    if distance_remaining < 0:
        continue
    for x in range(sensor_x - distance_remaining, sensor_x + distance_remaining + 1):
        x_not_beacon.add(x)

x_not_beacon.difference_update(x_beacon)
print(len(x_not_beacon))

# Part 2 - must be touching the outside of 4 diagonals, as well as within the right range
# First we get all the line segments of diagonals (distance + 1), then get all the intersection points between them - then manually check

line_segments_positive_slope = []
line_segments_negative_slope = []
for sensor in sensors:
    sensor_x, sensor_y, distance = sensor
    top = (sensor_x, sensor_y + distance + 1)
    bottom = (sensor_x, sensor_y - distance - 1)
    right = (sensor_x + distance + 1, sensor_y)
    left = (sensor_x - distance - 1, sensor_y)

    line_segments_positive_slope.append((left, top))
    line_segments_positive_slope.append((bottom, right))
    line_segments_negative_slope.append((top, right))
    line_segments_negative_slope.append((left, bottom))

def intersection(pos_line, neg_line):
    a = pos_line[0]
    b = pos_line[1]
    c = neg_line[0]
    d = neg_line[1]

    delta_a = (c[0] + c[1] - a[0] - a[1]) // 2
    delta_c = (a[0] - a[1] - c[0] + c[1]) // 2

    r_pos = b[0] - a[0]
    r_neg = d[0] - c[0]

    # check if intersection is valid - this might not be enough to say its valid, but it eliminates obvious bad points
    if 0 <= delta_a <= r_pos and 0 <= delta_c <= r_neg:
        return (a[0] + delta_a, a[1] + delta_a)
    else:
        return None

intersection_points = {}
for pos_line in line_segments_positive_slope:
    for neg_line in line_segments_negative_slope:
        point = intersection(pos_line, neg_line)
        if point is not None:
            if 0 <= point[0] <= max_x_y and 0 <= point[1] <= max_x_y:
                num = intersection_points.get(point, 0)
                intersection_points[point] = num + 1

eligible_points = set(point for point, times in intersection_points.items() if times >= 4)

for point in eligible_points:
    point_found = False
    for sensor in sensors:
        (sensor_x, sensor_y, distance) = sensor
        distance_of_point = abs(sensor_x - point[0]) + abs(sensor_y - point[1])
        if distance_of_point <= distance:
            point_found = True
            break
    if not point_found:
        # print(point)
        print(4000000 * point[0] + point[1])
        break
