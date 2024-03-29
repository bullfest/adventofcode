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
day = 8

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

nodes = {}
ins = lines[0]
for l in lines[2:]:
    s, d = l.split("=")
    s = s.strip()
    d = d.strip(" ()")
    l, r = d.split(", ")
    nodes[s] = (l, r)

if "AAA" in nodes:
    n = "AAA"
    i = 0
    while n != "ZZZ":
        d = ins[i % (len(ins))]
        if d == "L":
            n = nodes[n][0]
        else:
            n = nodes[n][1]
        i +=1
    ans1 = i

ns = [n for n in nodes if n.endswith("A")]
anss = []

for n in ns:
    i = 0
    while not n.endswith("Z"):
        d = ins[i % (len(ins))]
        if d == "L":
            n = nodes[n][0]
        else:
            n = nodes[n][1]
        i +=1
    anss.append(i)
ans2 = math.lcm(*anss)



##########
print("1:", ans1)
print("2:", ans2)

if filename is None:
    submit = input("submit?")
    if 'y' in submit.lower():
        if ans1 != 0:
            aocd.submit(ans1, year=year, day=day, part="a")
        if ans2 != 0:
            aocd.submit(ans2, year=year, day=day, part="b")
