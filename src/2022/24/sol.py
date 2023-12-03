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
day = 24

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

grid = get_grid(lines)
print_grid(grid)

max_x = len(grid)
max_y = len(grid[0])


def is_empty(x, y, t):
    inner_x = x - 1
    inner_y = y - 1
    up_y = (inner_y - t) % (max_y - 2)
    down_y = (inner_y + t) % (max_y - 2)
    left_x = (inner_x - t) % (max_x - 2)
    right_x = (inner_x + t) % (max_x - 2)
    if grid[x][up_y + 1] == "v":
        return False
    if grid[x][down_y + 1] == "^":
        return False
    if grid[left_x + 1][y] == ">":
        return False
    if grid[right_x + 1][y] == "<":
        return False
    return True


def distance(start: Tuple[int, int], end: Tuple[int, int], start_time: int):
    dfs = []
    dfs.append(start + (start_time,))  # x, y, t
    dist = defaultdict(set)

    t = 0
    while dfs:
        x, y, t = dfs.pop()
        if t > start_time + 500:
            continue
        if t in dist[(x, y)]:
            continue  # We've already been her at this point in time
        dist[(x, y)].add(t)

        # If we can stand still
        if is_empty(x, y, t + 1):
            dfs.append((x, y, t + 1))
        for x1, y1 in neighbours(x, y):
            if grid[x1][y1] == "#":
                continue
            if not is_empty(x1, y1, t + 1):
                continue  # Is Blizzard next turn
            dfs.append((x1, y1, t + 1))
    return min(dist[end])


start = (1, 0)
end = (max_x - 2, max_y - 1)
# There
ans1 = distance(start, end, 0)
print("1:", ans1)
# Home
home_again_time = distance(end, start, ans1)
print("home", home_again_time)
# And back again
ans2 = distance(start, end, home_again_time)

###########
print("2:", ans2)

if filename == "input":
    submit = input("submit?")
    if "y" in submit.lower():
        if ans1 != 0:
            aocd.submit(ans1, year=year, day=day, part="a")
        if ans2 != 0:
            aocd.submit(ans2, year=year, day=day, part="b")
