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


def get_sections(lines):
    """Split lines on empty lines"""
    sections = []
    section = []
    for l in lines:
        if l == "":
            if section != []:
                sections.append(section)
                section = []
        else:
            section.append(l)
    sections.append(section)
    return sections


def parse_ints(*l):
    return list(map(int, l))


def get_grid(lines, f=None, sep=None):
    """ """
    f = f or (lambda x: x)
    return transpose([list(map(f, l if sep is None else l.split(sep))) for l in lines])


def print_grid(g):
    for l in transpose(g):
        print(l)
        # print("".join(map(lambda n: "X" if n > 10 else str(n % 10), l)))
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


def neighbours(x, y, diagonal=False):
    l = []
    if x > 0:
        l.append((x - 1, y))
        if y > 0 and diagonal:
            l.append((x - 1, y - 1))
        if y + 1 < max_y and diagonal:
            l.append((x - 1, y + 1))
    if y > 0:
        l.append((x, y - 1))

    if x + 1 < max_x:
        l.append((x + 1, y))
        if y > 0 and diagonal:
            l.append((x + 1, y - 1))
        if y + 1 < max_y and diagonal:
            l.append((x + 1, y + 1))
    if y + 1 < max_y:
        l.append((x, y + 1))
    return l


year = 2022
day = 10

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
x = [1]

for i, l in enumerate(lines):
    if l == "noop":
        x.append(x[-1])
        continue
    elif l.startswith("addx"):
        _, a = l.split()
        a = int(a)
        x.append(x[-1])
        x.append(x[-1] + a)

ans1 = sum((i * 2 + 1) * 20 * v for i, v in enumerate(x[19::40]))

pixels = ["#" if abs(x[i] - (i % 40)) <= 1 else " " for i in range(len(x))]
for i in range(0, len(x) + 1, 40):
    print("".join(pixels[i : i + 40]))

###########
print("1:", ans1)
print("2:", ans2)

if filename == "input":
    submit = input("submit?")
    if "y" in submit.lower():
        if ans1 != 0:
            aocd.submit(ans1, year=year, day=day, part="a")
        ans2 = input("ans2?")
        if len(ans2) == 8:
            aocd.submit(ans2, year=year, day=day, part="b")
