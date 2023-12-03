#!/usr/bin/env python3
import dataclasses
import sys
import re
from functools import cached_property

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
day = 15

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


@dataclasses.dataclass
class Sensor:
    x: int
    y: int
    beacon_x: int
    beacon_y: int

    @cached_property
    def distance_to_beacon(self):
        return abs(self.x - self.beacon_x) + abs(self.y - self.beacon_y)

    def seen_cells_in_row(self, y: int):
        dx = self.distance_to_beacon - abs(self.y - y)
        if dx < 0:
            return set()
        s = set(range(self.x - dx, self.x + dx + 1))
        return s

    def boundary(self, y):
        dx = self.distance_to_beacon - abs(self.y - y)
        if dx < 0:
            return (-1, -1)
        return (self.x - dx, self.x + dx)


beacons = defaultdict(set)
sensors = []
for l in lines:
    l = l.split()
    x = int(l[2].strip(",").split("=")[1])
    y = int(l[3].strip(":").split("=")[1])
    b_x = int(l[8].strip(",").split("=")[1])
    b_y = int(l[9].split("=")[1])
    beacons[b_y].add(b_x)
    sensors.append(
        Sensor(
            x=x,
            y=y,
            beacon_x=b_x,
            beacon_y=b_y,
        )
    )

seen = defaultdict(set)
line = 2000000
for s in sensors:
    seen[line] |= s.seen_cells_in_row(line)

for by in beacons:
    seen[by] -= beacons[by]

ans1 = len(seen[line])
max_v = 20
if filename == "input":
    max_v = 4000000

for y in range(0, max_v + 1):
    rs = []
    for s in sensors:
        rs.append(s.boundary(y))
    rs.sort()
    comb_rs = []
    for x0, x1 in rs:
        # Outside boundary
        if x1 < 0 or x0 > max_v:
            continue
        start = max(0, x0)
        end = min(max_v, x1)
        if len(comb_rs) == 0:
            comb_rs.append((start, end))
            continue
        p_start, p_end = comb_rs[-1]
        if start <= p_end + 1:
            if end <= p_end:
                continue
            comb_rs.pop()
            comb_rs.append((p_start, end))
        else:
            print("ans2", p_end, start)
            ans2 = 4000000 * (p_end + 1) + y
            break
    if ans2:
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
