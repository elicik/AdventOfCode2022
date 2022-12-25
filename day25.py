lines = []
with open("day25.txt") as input_file:
    lines = input_file.read().rstrip().split("\n")

# lines = [
# "1=-0-2",
# "12111",
# "2=0=",
# "21",
# "2=01",
# "111",
# "20012",
# "112",
# "1=-1=",
# "1-12",
# "12",
# "1=",
# "122"
# ]

def snafu_to_decimal(line):
    result = 0
    multiplied_by = 1
    for char in reversed(line):
        if char == "-":
            num = -1
        elif char == "=":
            num = -2
        else:
            num = int(char)
        result += num * multiplied_by
        multiplied_by *= 5
    return result

def decimal_to_snafu(num):
    # Convert to base 5
    digits = []
    while num != 0:
        digits.append(num % 5)
        num //= 5
    digits = list(reversed(digits))

    # Make em negative
    for i in range(len(digits)-1, 0, -1):
        while digits[i] > 2:
            digits[i] -= 5
            digits[i-1] += 1

    if digits[0] > 2:
        digits[0] -= 5
        digits = [1] + digits
    result = ""
    for digit in digits:
        if digit == -1:
            char = "-"
        elif digit == -2:
            char = "="
        else:
            char = str(digit)
        result += char

    return result

total = 0
for line in lines:
    total += snafu_to_decimal(line)
print(decimal_to_snafu(total))