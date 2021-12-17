import sys

moves = [l.split() for l in sys.stdin]

x = 0
y = 0
for l in moves:
    if l[0] == "forward":
        x += int(l[1])
    elif l[0] == "up":
        y -= int(l[1])
    elif l[0] == "down":
        y += int(l[1])

print("1:", x * y)

x = 0
y = 0
aim = 0
for l in moves:
    if l[0] == "forward":
        x += int(l[1])
        y += aim * int(l[1])
    elif l[0] == "up":
        aim -= int(l[1])
    elif l[0] == "down":
        aim += int(l[1])

print("2:", x * y)
