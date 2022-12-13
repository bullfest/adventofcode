#!/usr/bin/env python3
import json
import sys
import re
from functools import cmp_to_key

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
day = 13

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


def compare(l, r):
    if isinstance(l, int) and isinstance(r, int):
        if l < r:
            return -1
        if l == r:
            return 0
        return 1
    if isinstance(l, list) and isinstance(r, list):
        for i in range(min(len(l), len(r))):
            c = compare(l[i], r[i])
            if c != 0:
                return c
        if len(l) < len(r):
            return -1
        if len(l) == len(r):
            return 0
        return 1
    if isinstance(l, list) and isinstance(r, int):
        return compare(l, [r])
    if isinstance(l, int) and isinstance(r, list):
        return compare([l], r)


sections = get_sections(lines)
for i, section in enumerate(sections, start=1):
    first, second = section
    first = json.loads(first)
    second = json.loads(second)
    if compare(first, second) <= 0:
        ans1 += i

all = [json.loads(s) for section in sections for s in section]

divider1 = [[2]]
divider2 = [[6]]
all.append(divider1)
all.append(divider2)

print(all)
all.sort(key=cmp_to_key(compare))
i1 = 0
i2 = 0
for i, l in enumerate(all, start=1):
    if l == divider1:
        i1 = i
    if l == divider2:
        i2 = i
ans2 = i1 * i2

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
