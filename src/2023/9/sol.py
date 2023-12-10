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
day = 9

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

def extrapolate(ns):
    diffs = []
    all_zero = True
    for n1, n2 in itertools.pairwise(ns):
        diffs.append(n2 - n1)
        if diffs[-1] != 0:
            all_zero = False

    if all_zero:
        return ns[-1]
    next_diff = extrapolate(diffs)
    return ns[-1] + next_diff


def extrapolate_back(ns):
    diffs = []
    all_zero = True
    for n1, n2 in itertools.pairwise(ns):
        diffs.append(n2 - n1)
        if diffs[-1] != 0:
            all_zero = False
    if all_zero:
        return ns[0]
    next_diff = extrapolate_back(diffs)
    return ns[0] - next_diff


for l in lines:
    d = aoclib.parse_ints(*l.split())
    ans1 += extrapolate(d)
    ans2 += extrapolate_back(d)

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
