#!/usr/bin/env python3
import itertools
import sys
import re

import networkx

import aoclib
from aoclib import *
import q
import itertools as it
import math
import aocd
from typing import List, Tuple
from dataclasses import dataclass
from collections import defaultdict


def set_max_x(n: int):
    global max_x
    max_x = aoclib.max_x = n


def set_max_y(n: int):
    global max_y
    max_y = aoclib.max_y = n


def flip_x_y():
    global max_x, max_y
    max_x, max_y = max_y, max_x
    aoclib.max_x = max_x
    aoclib.max_y = max_y


year = 2023
day = 11

if len(sys.argv) > 1:
    filename = sys.argv[1]
    with open(filename) as file:
        lines = [l.strip('\n') for l in file]
else:
    filename = None
    lines = aocd.get_data(year=year, day=day).split("\n")

print("len(lines)", len(lines))
print("len(lines[0])", len(lines[0]))

ans1 = 0
ans2 = 0

set_max_x(len(lines))
set_max_y(len(lines[0]))

############
# SOLUTION #
############
sections = get_sections(lines)

row_has_galaxies = defaultdict(lambda: False)
col_has_galaxies = defaultdict(lambda: False)

galaxies1 = []
galaxies2 = []
for i, l in enumerate(lines):
    if "#" in l:
        row_has_galaxies[i] = True
    for j, c in enumerate(l):
        if c == "#":
            col_has_galaxies[j] = True

for i, l in enumerate(lines):
    for j, c in enumerate(l):
        if c == "#":
            extra_x, extra_y = 0, 0
            for x in range(i):
                if not row_has_galaxies[x]:
                    extra_x += 1
            for y in range(j):
                if not col_has_galaxies[y]:
                    extra_y += 1
            galaxies1.append((i + extra_x, j + extra_y))
            galaxies2.append((i + (extra_x * (1000000 - 1)), j + (extra_y * (1000000 - 1))))

for (x1, y1), (x2, y2) in itertools.combinations(galaxies1, 2):
    ans1 += abs(x1 - x2) + abs(y1 - y2)

for (x1, y1), (x2, y2) in itertools.combinations(galaxies2, 2):
    ans2 += abs(x1 - x2) + abs(y1 - y2)


###########
print("1:", ans1)
print("2:", ans2)

if filename is None:
    submit = input("submit?")
    if 'y' in submit.lower():
        if ans1 != 0:
            aocd.submit(ans1, year=year, day=day, part="a")
        if ans2 != 0:
            aocd.submit(ans2, year=year, day=day, part="b")
