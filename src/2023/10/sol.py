#!/usr/bin/env python3
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
day = 10

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

sx, sy = 0, 0


def neighbours(x, y):
    if 0 < x and lines[x][y] in "|LJS" and lines[x - 1][y] in "|F7":
        yield x - 1, y, "N"
    if x < aoclib.max_x - 1 and lines[x][y] in "|F7S" and lines[x + 1][y] in "|LJ":
        yield x + 1, y, "S"
    if 0 < y and lines[x][y] in "-J7" and lines[x][y - 1] in "-LF":
        yield x, y - 1, "W"
    if y < aoclib.max_y - 1 and lines[x][y] in "-LF" and lines[x][y + 1] in "-J7":
        yield x, y + 1, "E"


def print_board():
    for i, l in enumerate(lines):
        line = []
        for j, c in enumerate(l):
            if (i, j) in loop:
                line.append(c)
            elif (i, j) in inside:
                line.append("■")
            else:
                line.append(" ")
        print("".join(line))


for x, l in enumerate(lines):
    for y, c in enumerate(l):
        if c == "S":
            sx, sy = x, y


nodes = [(sx, sy)]

loop = set()
while nodes:
    x, y = nodes.pop()
    if (x, y) in loop:
        continue
    loop.add((x, y))
    for nx, ny, _ in neighbours(x, y):
        nodes.append((nx, ny))
ans1 = math.ceil(len(loop) / 2)

s_headings = []
for _, _, h in neighbours(sx, sy):
    s_headings.append(h)

inside = set()
for i in range(len(lines)):
    walls = 0
    for j in range(len(lines[0])):
        if (i, j) in loop:
            if lines[i][j] == "S" and "N" in s_headings:
                walls += 1
            if lines[i][j] in "|JL":
                walls += 1
            continue
        if walls % 2 == 1:
            inside.add((i, j))
            ans2 += 1
print_board()
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
