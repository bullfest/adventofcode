#!/usr/bin/env python3
import sys
import aocd

year=2023
day=2

if len(sys.argv) > 1:
    filename = sys.argv[1]
    with open(filename) as file:
        lines = [l.strip('\n') for l in file]
else:
    filename = "input"
    lines = aocd.get_data(year=year, day=day).split("\n")

print("len(lines)", len(lines))
ans1 = 0
ans2 = 0
############
# SOLUTION #
############

available = {"red": 12, "green": 13, "blue": 14}

for l in lines:
    g = int(l.split(":")[0].split()[1])
    m = {}
    for set in l.split(":")[1].split(";"):
        for c in set.split(","):
            n, col = c.strip().split()
            n = int(n)
            if n > available[col]:
                break
        else:
            continue
        break
    else:
        ans1 += g

for l in lines:
    g = int(l.split(":")[0].split()[1])
    m = {}
    for set in l.split(":")[1].split(";"):
        for c in set.split(","):
            n, col = c.strip().split()
            n = int(n)
            m[col] = max(m.get(col,0), n)
    a = 1
    for v in m.values():
        a *= v
    print(g, m, a)
    ans2 += a

###########
print("1:", ans1)
print("2:", ans2)

if filename == "input":
    submit = input("submit?")
    if 'y' in submit.lower():
        if ans1 != 0:
            aocd.submit(ans1, year=year, day=day, part="a")
        if ans2 != 0:
            aocd.submit(ans2, year=year, day=day, part="b")
