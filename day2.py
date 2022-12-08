lines = []
with open("day2.txt") as input_file:
    lines = input_file.read().strip().split("\n")
# lines = ["A Y", "B X", "C Z"]

total = 0
for line in lines:
    arr = line.split(" ")
    opp = arr[0]
    me = arr[1]
    # 1 is win, 0 is tie, -1 is loss
    if (me == "X" and opp == "C") or (me == "Y" and opp == "A") or (me == "Z" and opp == "B"):
        winner = 1
    elif (me == "X" and opp == "A") or (me == "Y" and opp == "B") or (me == "Z" and opp == "C"):
        winner = 0
    else:
        winner = -1
    convert = {
        "X": 1,
        "Y": 2,
        "Z": 3,
    }
    
    score = convert[me] + 3 * (winner + 1)
    # print(arr, convert[me], 3 * (winner + 1), score)
    total += score

print(total)

total = 0
for line in lines:
    arr = line.split(" ")
    opp = arr[0]
    winner = arr[1]
    # X is lose, Y is draw, Z is win
    if winner == "X":
        winner = -1
        if opp == "A":
            me = "Z"
        if opp == "B":
            me = "X"
        if opp == "C":
            me = "Y"
    elif winner == "Y":
        winner = 0
        me = chr(ord(opp) + 23)
    else:
        winner = 1
        if opp == "A":
            me = "Y"
        if opp == "B":
            me = "Z"
        if opp == "C":
            me = "X"
    # 1 is win, 0 is tie, -1 is loss
    convert = {
        "X": 1,
        "Y": 2,
        "Z": 3,
    }
    
    score = convert[me] + 3 * (winner + 1)
    # print(arr, convert[me], 3 * (winner + 1), score)
    total += score

print(total)