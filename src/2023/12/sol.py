#!/usr/bin/env python3
import functools
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
day = 12

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

for sect in sections[0:]:
    for l in sect:
        pass


@functools.cache
def ways(springs, ns, run=0):
    ans = 0
    if run == ns[0]:
        if not springs:
            if ns[1:]:
                return 0
            return 1
        if springs[0] == "#":
            return 0
        # Remove 1 ensures next is "."
        ns = ns[1:]
        run = 0
        springs = springs[1:]

    if len(ns) == 0:
        if "#" not in springs:
            return 1
        else:
            return 0
    if len(springs) == 0:
        return 0

    if springs[0] == "#":
        return ways(springs[1:], ns, run + 1)
    if springs[0] == ".":
        if run != 0:
            return 0
        return ways(springs[1:], ns, run)
    ans += ways(springs[1:], ns, run + 1)
    if run == 0:
        ans += ways(springs[1:], ns, 0)
    return ans


for l in lines:
    springs, ns = l.split()
    ns = tuple(parse_ints(*ns.split(",")))
    w = ways(springs, ns)
    ans1 += w
    long_springs = "?".join(springs for _ in range(5))
    w = ways(long_springs, ns*5)
    #print((springs+"?")*5, ns*5)
    print(springs, w)
    ans2 += w

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
