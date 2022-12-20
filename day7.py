import math

lines = []
with open("day7.txt") as input_file:
    lines = input_file.read().rstrip().split("\n")

# lines = [
# "$ cd /",
# "$ ls",
# "dir a",
# "14848514 b.txt",
# "8504156 c.dat",
# "dir d",
# "$ cd a",
# "$ ls",
# "dir e",
# "29116 f",
# "2557 g",
# "62596 h.lst",
# "$ cd e",
# "$ ls",
# "584 i",
# "$ cd ..",
# "$ cd ..",
# "$ cd d",
# "$ ls",
# "4060174 j",
# "8033020 d.log",
# "5626152 d.ext",
# "7214296 k"
# ]

class file:
    def __init__(self, name, size):
        self.name = name
        self._size = size
    def size(self):
        return self._size

class directory:
    def __init__(self, name, parent):
        self.name = name
        self.files = {}
        self.parent = parent
    
    def size(self):
        return 0 if len(self.files) == 0 else sum([file.size() for file in self.files.values()])

slash = directory("/", None)
all_dirs = [slash]

def process_ls(dir, output):
    for line in output:
        if line.startswith("dir"):
            name = line[4:]
            new_dir = directory(name, dir)
            dir.files[name] = new_dir
            all_dirs.append(new_dir)
        else:
            arr = line.split(" ")
            size = int(arr[0])
            name = arr[1]
            dir.files[name] = file(name, size)

current_dir = slash
output = []

for line in lines[1:]:
    if line.startswith("$"):
        if len(output) != 0:
            process_ls(current_dir, output)
            output = []
        if line.startswith("$ cd"):
            name = line[5:]
            if name == "..":
                current_dir = current_dir.parent
            else:
                current_dir = current_dir.files[name]
    else:
        output.append(line)

process_ls(current_dir, output)

# part 1:

total = 0
for dir in all_dirs:
    size = dir.size()
    if size <= 100000:
        total += size

print(total)

# part 2:

unused_space = 70000000 - slash.size()
needed_clear = 30000000 - unused_space

min_size = math.inf

for dir in all_dirs:
    size = dir.size()
    if size >= needed_clear:
        if size <= min_size:
            min_size = size

print(min_size)