#!/usr/bin/env python3
import itertools
import sys
import re

import aoclib
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
day = 6

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
times = aoclib.parse_ints(*lines[0].split()[1:])
distances = aoclib.parse_ints(*lines[1].split()[1:])

ans1 = 1
for t, d in zip(times, distances):
    ways = 0
    for i in range(t):
        if (t-i)*i > d:
            ways += 1
    ans1 *= ways

time = int(lines[0].replace(" ", "").split(":")[1])
dist = int(lines[1].replace(" ", "").split(":")[1])

for i in range(time):
    if (time-i)*i > dist:
        ans2 += 1

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
