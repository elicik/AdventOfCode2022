import numpy as np

lines = []
with open("day8.txt") as input_file:
    lines = input_file.read().strip().split("\n")

# lines = ["30373",
# "25512",
# "65332",
# "33549",
# "35390"]

nums = []

for line in lines:
    nums.append([int(x) for x in line])

x_len = len(nums)
y_len = len(nums[0])

total = 0

nums = np.array(nums)
nums_tp = np.transpose(nums)

for x in range(x_len):
    for y in range(y_len):
        num = nums[x][y]
        if x == 0 or x == x_len-1 or y == 0 or y == y_len-1:
            total += 1
        else:
            left = nums[x][:y]
            right = nums[x][y+1:]
            up = nums_tp[y][:x]
            down = nums_tp[y][x+1:]
            # print(x, y, left)
            # print(x, y, right)
            # print(x, y, up)
            # print(x, y, down)
            if np.max(left) < num or np.max(right) < num or np.max(up) < num or np.max(down) < num:
                total += 1

# print(total)




max_score = 0

nums = np.array(nums)
nums_tp = np.transpose(nums)
print(nums)
print(nums.size, x_len, y_len)

for x in range(x_len):
    for y in range(y_len):
        num = nums[x][y]
        if x == 0 or x == x_len-1 or y == 0 or y == y_len-1:
            continue
        else:
            left = np.flip(nums[x][:y])
            right = nums[x][y+1:]
            up = np.flip(nums_tp[y][:x])
            down = nums_tp[y][x+1:]
            # print(x, y, left)
            # print(x, y, right)
            # print(x, y, up)
            # print(x, y, down)
            # print(left >= num)
            # print(right >= num)
            # print(up >= num)
            # print(down >= num)
            left_score = left.size if (~(left >= num)).all() else (np.argmax(left >= num) + 1)
            right_score = right.size if (~(right >= num)).all() else (np.argmax(right >= num) + 1)
            up_score = up.size if (~(up >= num)).all() else (np.argmax(up >= num) + 1)
            down_score = down.size if (~(down >= num)).all() else (np.argmax(down >= num) + 1)
            # print(x, y, left_score, right_score, up_score, down_score)
            score = left_score * right_score * up_score * down_score
            if score > max_score:
                max_score = score

print(max_score)