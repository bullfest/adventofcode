#!/usr/bin/env python3
import sys
import re
import q
import itertools as it
import math
import aocd
from typing import List, Tuple
from dataclasses import dataclass
from collections import defaultdict


def transpose(m):
    """[[1, 2], [3, 4]] -> [[1, 3], [2, 4]]"""
    return list(map(list, zip(*m)))


def get_grid(lines, f=None, sep=None):
    """ """
    f = f or (lambda x: x)
    g1 = [list(map(f, list(l) if sep is None else l.split(sep))) for l in lines]
    print(g1)
    return transpose(g1)


def print_grid(g):
    for l in transpose(g):
        # print(l)
        print("".join(map(lambda n: "X" if n else ".", l)))
    print()


def zero_index_points(points):
    return [(x - 1, y - 1) for x, y in points]


def points_to_grid(points, default_value=False, point_value=True):
    max_x = 0
    max_y = 0
    for x, y in points:
        max_x = max(x, max_x)
        max_y = max(y, max_y)

    grid = [[default_value] * (max_y + 1) for _ in range(max_x + 1)]
    for x, y in points:
        grid[x][y] = point_value
    return grid


if len(sys.argv) > 1:
    filename = sys.argv[1]
    with open(filename) as file:
        lines = [l.strip("\n") for l in file]
else:
    filename = "input"
    lines = aocd.get_data(year=2022, day=8).split("\n")

print("len(lines)", len(lines))
ans1 = 0
ans2 = 0

trees = get_grid(lines, f=int)
print(lines)
visible = [[False] * len(trees[0]) for _ in range(len(trees))]


for x in range(len(trees)):
    m = -1
    for y in range(len(trees[x])):
        if trees[x][y] > m:
            visible[x][y] = True
        m = max(trees[x][y], m)

    m = -1
    for y in reversed(range(len(trees[x]))):
        if trees[x][y] > m:
            m = trees[x][y]
            visible[x][y] = True
        m = max(trees[x][y], m)

for y in range(len(trees[0])):
    m = -1
    for x in range(len(trees)):
        if trees[x][y] > m:
            m = trees[x][y]
            visible[x][y] = True
        m = max(trees[x][y], m)

    m = -1
    for x in reversed(range(len(trees))):
        if trees[x][y] > m:
            m = trees[x][y]
            visible[x][y] = True
        m = max(trees[x][y], m)


def ss(x0, y0):
    l = []
    m = trees[x0][y0]
    s = 0
    # print("D")
    for y in range(y0 + 1, len(trees[0])):
        s += 1
        if trees[x0][y] >= m:
            break
    l.append(s)
    s = 0

    # print("U")
    for y in range(y0 - 1, -1, -1):
        s += 1
        if trees[x0][y] >= m:
            break
    l.append(s)
    s = 0

    # print("R")
    for x in range(x0 + 1, len(trees)):
        s += 1
        if trees[x][y0] >= m:
            break
    l.append(s)
    s = 0

    # print("L")
    for x in range(x0 - 1, -1, -1):
        s += 1
        if trees[x][y0] >= m:
            break
    l.append(s)
    s = 1
    for v in l:
        s *= v
    if s > 8:
        print(x0, y0, l, s)
    return s


for l in visible:
    for v in l:
        if v:
            ans1 += 1

for x in range(len(trees)):
    for y in range(len(trees)):
        ans2 = max(ans2, ss(x, y))
print("1:", ans1)
print("2:", ans2)

if filename == "input":
    submit = input("submit?")
    if "y" in submit.lower():
        if ans1 != 0:
            aocd.submit(ans1, year=2022, day=8, part="a")
        if ans2 != 0:
            aocd.submit(ans2, year=2022, day=8, part="b")
