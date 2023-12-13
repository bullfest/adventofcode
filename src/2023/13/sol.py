#!/usr/bin/env python3
import sys
import re

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
day = 13

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


def has_reflection(m: List[str], i: int, require_smudge=False):
    l, h = i - 1, i
    while l >= 0 and h < len(m):
        for left, right in zip(m[l], m[h]):
            if left != right:
                if require_smudge:
                    require_smudge = False
                else:
                    return False
        l -= 1
        h += 1
    return not require_smudge


for sect in sections:
    for i in range(1, len(sect)):
        if has_reflection(sect, i):
            ans1 += 100 * i
        if has_reflection(sect, i, require_smudge=True):
            ans2 += 100 * i
    else:
        sect = transpose(sect)
        for i in range(1, len(sect)):
            if has_reflection(sect, i):
                ans1 += i
            if has_reflection(sect, i, require_smudge=True):
                ans2 += i

############
print("1:", ans1)
print("2:", ans2)

if filename is None:
    submit = input("submit?")
    if 'y' in submit.lower():
        if ans1 != 0:
            aocd.submit(ans1, year=year, day=day, part="a")
        if ans2 != 0:
            aocd.submit(ans2, year=year, day=day, part="b")
