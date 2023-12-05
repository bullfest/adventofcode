#!/usr/bin/env python3
import dataclasses
import functools
import itertools
import sys
import re

import aoclib
import q
import itertools as it
import math
import aocd
from typing import List, Tuple, Dict
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
day = 5

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
ans2_correct = 0

set_max_x(len(lines))
set_max_y(len(lines[0]))

############
# SOLUTION #
############

maps = {}
rev_maps = {}


@dataclasses.dataclass
class Map:
    source: str = None
    dest: str = None
    map: List = dataclasses.field(default_factory=list)

    def get_target(self, n):
        for m in self.map:
            if m[0] <= n < m[0] + m[2]:
                ds = m[0]
                ts = m[1]
                dest = ts + n - ds
                return dest
        return n

    def reverse(self, n):
        for m in self.map:
            if m[1] <= n < m[1] + m[2]:
                ds = m[0]
                ts = m[1]
                return ds + n - ts
        return n


i = 0
sections = aoclib.get_sections(lines)
for grp in sections[1:]:
    f, t = grp[0].split()[0].split("-to-")
    m = Map(source=f, dest=t)
    for l in grp[1:]:
        ds, ss, n = aoclib.parse_ints(*l.split())
        m.map.append((ss, ds, n))
    m.map.sort()
    maps[m.source] = m
    rev_maps[m.dest] = m


def location(seed):
    n = seed
    m = maps["seed"]
    while m.dest != "location":
        n = m.get_target(n)
        m = maps[m.dest]
    return m.get_target(n)


def get_seed(location):
    n = location
    m = rev_maps["location"]
    while m.source != "seed":
        n = m.reverse(n)
        m = rev_maps[m.source]
    return m.reverse(n)


seeds = aoclib.parse_ints(*sections[0][0].split()[1:])
ans1 = 100000000000000000000000000000000
for seed in seeds:
    l = location(seed)
    if l is not None:
        ans1 = min(ans1, l)

i = 0
# Slow (~1 min) but arguably correct solution
ans2_correct = None
while ans2_correct is None:
    seed = get_seed(i)
    j = 0
    while j < len(seeds):
        if seeds[j] <= seed < seeds[j] + seeds[j + 1]:
            ans2_correct = i
            break
        j += 2
    i += 1

print(ans2_correct)

# Fast but not 100% correct solution (Can construct testcase for which this fails)
i = 0
best_range = [0, 0]
ans2 = 100000000000000000000000000000000
while i < len(seeds):
    seed = seeds[i]
    n = seeds[i + 1]
    sq = int(math.sqrt(n))
    while seed < seeds[i] + n:
        l = location(seed)
        if l < ans2:
            best_range = (max(seed - sq, seeds[i]), min(seed + sq, seeds[i] + n))
            ans2 = l
        seed += sq

    i += 2
for seed in range(best_range[0], best_range[1]):
    ans2 = min(ans2, location(seed))

###########
print("1:", ans1)
print("2(incorrect):", ans2)
print("2:", ans2_correct)

if filename is None:
    submit = input("submit?")
    if 'y' in submit.lower():
        if ans1 != 0:
            aocd.submit(ans1, year=year, day=day, part="a")
        if ans2_correct != 0:
            aocd.submit(ans2_correct, year=year, day=day, part="b")
