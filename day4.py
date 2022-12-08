lines = []
with open("day4.txt") as input_file:
    lines = input_file.read().strip().split("\n")

# lines = [
#     "2-4,6-8",
#     "2-3,4-5",
#     "5-7,7-9",
#     "2-8,3-7",
#     "6-6,4-6",
#     "2-6,4-8"]

total = 0
for line in lines:
    arr = line.split(",")
    first = [int(x) for x in arr[0].split("-")]
    second = [int(x) for x in arr[1].split("-")]

    if (first[0] <= second[0] and first[1] >= second[1]) or (first[0] >= second[0] and first[1] <= second[1]):
        total += 1

print(total)

total = 0
for line in lines:
    arr = line.split(",")
    first = [int(x) for x in arr[0].split("-")]
    second = [int(x) for x in arr[1].split("-")]

    # a-b, c-d
    a = first[0]
    b = first[1]
    c = second[0]
    d = second[1]
    if (a <= c and b >= c) or (a <= d and b >= d) or (c <= a and d >= a) or (c <= b and d >= b):
        total += 1

print(total)