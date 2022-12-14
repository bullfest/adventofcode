#!/usr/bin/env python3
import sys
import re
import time

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
day = 14

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

max_x = 0
max_y = 0
stones = set()
for l in lines:
    l = l.split(" -> ")
    for i in range(len(l) - 1):
        x1, y1 = parse_ints(*l[i].split(","))
        x2, y2 = parse_ints(*l[i + 1].split(","))
        max_x = max(max_x, x1, x2)
        max_y = max(max_y, y1, y2)

        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                stones.add((x1, y))
        else:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                stones.add((x, y1))

filled = set(stones)
done = False
while not done:
    x = 500
    y = 0
    while True:
        if x < 0 or x > max_x or y > max_y:
            done = True
            break
        if (x, y + 1) not in filled:
            y += 1
        elif (x - 1, y + 1) not in filled:
            x -= 1
            y += 1
        elif (x + 1, y + 1) not in filled:
            x += 1
            y += 1
        else:
            filled.add((x, y))
            ans1 += 1
            break


filled = set(stones)
for x in range(-1000, max_x + 1001):
    filled.add((x, max_y + 2))
done = False
while (500, 0) not in filled:
    x = 500
    y = 0
    while True:
        if (x, y + 1) not in filled:
            y += 1
        elif (x - 1, y + 1) not in filled:
            x -= 1
            y += 1
        elif (x + 1, y + 1) not in filled:
            x += 1
            y += 1
        else:
            filled.add((x, y))
            ans2 += 1
            break


###########
print("1:", ans1)
print("2:", ans2)

if filename == "input":
    submit = input("submit?")
    if "y" in submit.lower():
        if ans1 != 0:
            aocd.submit(ans1, year=year, day=day, part="a")
        if ans2 != 0:
            aocd.submit(ans2, year=year, day=day, part="b")
