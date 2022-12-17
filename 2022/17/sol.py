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
        print("".join(l))
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
day = 17

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
shapes = [
    ((0, 0), (1, 0), (2, 0), (3, 0)),  # -
    ((1, 0), (0, 1), (1, 1), (2, 1), (1, 2)),  # +
    ((2, 0), (2, 1), (0, 2), (1, 2), (2, 2)),  # L
    ((0, 0), (0, 1), (0, 2), (0, 3)),  # |
    ((0, 0), (1, 0), (0, 1), (1, 1)),  # #
]
height = [1, 3, 3, 4, 2]
stream = lines[0]


def tower_to_grid():
    max_y = max(y for _, y in tower)
    grid = [[" "] * (max_y + 1) for _ in range(7)]
    for x, y in tower:
        grid[x][max_y - y] = "#"
    return grid


def coords(x, y, shape):
    return set((x + x1, y - y1) for x1, y1 in shape)


def forbidden(x, y, shape):
    cs = coords(x, y, shape)
    if not all(0 <= x < 7 for x, _ in cs):
        return True
    if any(y < 0 for _, y in cs):
        return True
    return any(c in tower for c in cs)


tower = set()
stream_i = 0
top_rock = 0
for i in range(2022):
    # print(i, top_rock)
    y = top_rock + 2 + height[i % 5]
    x = 2
    shape = shapes[i % 5]
    while True:
        # Attempt to follow stream
        if stream[stream_i % len(stream)] == "<":
            x1 = x - 1
        else:
            x1 = x + 1
        stream_i += 1
        if not forbidden(x1, y, shape):
            x = x1
        y1 = y - 1
        if not forbidden(x, y1, shape):
            y = y1
        else:
            tower |= coords(x, y, shape)
            top_rock = max(top_rock, y + 1)
            # print_grid(tower_to_grid())

            break
ans1 = top_rock

print("1:", ans1)


########### Part 2
def top_to_key(tower):
    max_y = max(y for _, y in tower)
    return frozenset((x, max_y - y) for x, y in tower if max_y - y <= 30)


seen = {}

tower = set()
stream_i = 0
top_rock = 0
goal = 1000000000000
i = -1
extra = 0
while i < goal:
    i += 1
    y = top_rock + 2 + height[i % 5]
    x = 2
    shape = shapes[i % 5]
    while True:
        # Attempt to follow stream
        if stream[stream_i] == "<":
            x1 = x - 1
        else:
            x1 = x + 1
        stream_i += 1
        stream_i %= len(stream)
        if not forbidden(x1, y, shape):
            x = x1
        # Attempt to go down
        y1 = y - 1
        if not forbidden(x, y1, shape):
            y = y1
        else:
            tower |= coords(x, y, shape)
            top_rock = max(top_rock, y + 1)
            key = (i % 5, stream_i, top_to_key(tower))
            if key in seen:
                pi, ptop = seen[key]
                di = i - pi
                dt = top_rock - ptop
                times = (goal - i) // di
                i += di * times
                extra += dt * times
            seen[key] = (i, top_rock)

            break
ans2 = top_rock + extra - 1
print("2:", ans2)
if filename == "test":
    assert ans2 == 1514285714288

    ###########

if filename == "input":
    submit = input("submit?")
    if "y" in submit.lower():
        if ans1 != 0:
            aocd.submit(ans1, year=year, day=day, part="a")
        if ans2 != 0:
            aocd.submit(ans2, year=year, day=day, part="b")
