#!/usr/bin/env python3
import sys
from copy import deepcopy
from typing import List, Optional, Any

import aocd


def transpose(m):
    """[[1, 2], [3, 4]] -> [[1, 3], [2, 4]]"""
    return list(map(list, zip(*m)))


def parse_ints(*l):
    return list(map(int, l))


def v_to_str(v):
    if v is True:
        return "#"
    if v is False:
        return " "
    if v is None:
        return "."


def print_grid(g):
    for l in transpose(g):
        print("".join(v_to_str(v) for v in l))
        # print("".join(map(lambda n: "X" if n > 10 else str(n % 10), l)))
    print()


max_p: Optional[List[int]] = None


def points_to_grid(points, default_value=False, point_value=True):
    global max_p
    max_p = [0] * len(points[0])

    for p in points:
        for i, v in enumerate(p):
            max_p[i] = max(v, max_p[i])
    max_p = [v + 1 for v in max_p]

    grid = default_value
    for v in reversed(max_p):
        grid = [deepcopy(grid) for _ in range(v)]

    for p in points:
        acc = grid
        for v in p[:-1]:
            acc = acc[v]
        acc[p[-1]] = point_value
    return grid


def neighbours(x, y, z, diagonal=False):
    l = []
    if x > 0:
        l.append((x - 1, y, z))
        if y > 0 and diagonal:
            l.append((x - 1, y - 1, z))
        if y + 1 < max_y and diagonal:
            l.append((x - 1, y + 1, z))
    if y > 0:
        l.append((x, y - 1, z))
    if z > 0:
        l.append((x, y, z - 1))

    if x + 1 < max_x:
        l.append((x + 1, y, z))
        if y > 0 and diagonal:
            l.append((x + 1, y - 1, z))
        if y + 1 < max_y and diagonal:
            l.append((x + 1, y + 1, z))
    if y + 1 < max_y:
        l.append((x, y + 1, z))
    if z + 1 < max_z:
        l.append((x, y, z + 1))
    return set(l)


year = 2022
day = 18

if len(sys.argv) > 1:
    filename = sys.argv[1]
    with open(filename) as file:
        lines = [l.strip("\n") for l in file]
else:
    filename = "input"
    lines = aocd.get_data(year=year, day=day).split("\n")

print("len(lines)", len(lines))
ans1 = 0
ans2 = 0
############
# SOLUTION #
############

points = []
for l in lines:
    p = parse_ints(*l.split(","))
    points.append(p)
grid = points_to_grid(points)

assert max_p
max_x = max_p[0]
max_y = max_p[1]
max_z = max_p[2]


def find_surface_area(grid):
    ans = 0
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            for z in range(len(grid[x][y])):
                if not grid[x][y][z]:
                    continue
                ns = neighbours(x, y, z)
                ans += 6 - len(ns)  # "open" sides
                for x1, y1, z1 in ns:
                    if not grid[x1][y1][z1]:
                        ans += 1
    return ans


def fill(x, y, z):
    dfs = [(x, y, z)]
    seen = set()
    while dfs:
        x0, y0, z0 = dfs.pop()
        if grid[x0][y0][z0] is True:
            continue
        # point is reachable from edge
        if 0 in (x0, y0, z0) or x0 == max_x - 1 or y0 == max_y - 1 or z0 == max_z - 1:
            return

        seen.add((x0, y0, z0))
        for n in neighbours(x0, y0, z0):
            if n in seen:
                continue
            dfs.append(n)
    grid[x][y][z] = True


ans1 = find_surface_area(grid)
print("1:", ans1)

for x in range(len(grid)):
    for y in range(len(grid[x])):
        for z in range(len(grid[x][y])):
            fill(x, y, z)

ans2 = find_surface_area(grid)

###########
print("2:", ans2)

if filename == "input":
    submit = input("submit?")
    if "y" in submit.lower():
        if ans1 != 0:
            aocd.submit(ans1, year=year, day=day, part="a")
        if ans2 != 0:
            aocd.submit(ans2, year=year, day=day, part="b")
