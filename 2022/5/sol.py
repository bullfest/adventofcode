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
from copy import deepcopy


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


def parse_stacks(s):
    idxs = list(map(int, s[-1].split()))
    stacks = [list() for _ in range(len(idxs))]
    for line in reversed(s[:-1]):
        for i, c in enumerate(line):
            if not ("A" <= c <= "Z"):
                continue
            stacks[i // 4].append(c)
    print(stacks)
    return stacks


if len(sys.argv) > 1:
    filename = sys.argv[1]
    with open(filename) as file:
        lines = [l.strip("\n") for l in file]
    print(lines)
else:
    filename = "input"
    lines = aocd.get_data(day=5, year=2022).split("\n")

print("len(lines)", len(lines))
ans1 = 0
ans2 = 0

stacks_str, moves = get_sections(lines)

stacks = parse_stacks(stacks_str)
os = deepcopy(stacks)
for move in moves:
    _, n, _, f, _, t = move.split()
    n = int(n)
    f = int(f)
    t = int(t)
    for _ in range(n):
        item = stacks[f - 1].pop()
        stacks[t - 1].append(item)

ans1 = "".join([s[-1] for s in stacks])

stacks = os

for move in moves:
    _, n, _, f, _, t = move.split()
    n, f, t = parse_ints(n, f, t)
    items = stacks[f - 1][-n:]
    stacks[f - 1] = stacks[f - 1][:-n]
    stacks[t - 1] += items
ans2 = "".join([s[-1] for s in stacks])

print("1:", ans1)
print("2:", ans2)

if filename == "input":
    submit = input("submit?")
    if "y" in submit.lower():
        if ans1 != 0:
            aocd.submit(ans1, part="a")
        if ans2 != 0:
            aocd.submit(ans2, part="b")
