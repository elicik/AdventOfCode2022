lines = []
with open("day1.txt") as input_file:
    lines = input_file.read().split("\n")

cals = []
cal = 0
for line in lines:
    if line == "":
        cals.append(cal)
        cal = 0
    else:
        cal += int(line)

cals.sort(reverse=True)
print(cals[0])
print(sum(cals[0:3]))