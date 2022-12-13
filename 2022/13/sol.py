#!/usr/bin/env python3
import json
import sys
from functools import cmp_to_key

import aocd


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


year = 2022
day = 13

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


def compare(l, r):
    if isinstance(l, int) and isinstance(r, int):
        if l < r:
            return -1
        if l == r:
            return 0
        return 1
    if isinstance(l, list) and isinstance(r, list):
        for i in range(min(len(l), len(r))):
            c = compare(l[i], r[i])
            if c != 0:
                return c
        if len(l) < len(r):
            return -1
        if len(l) == len(r):
            return 0
        return 1
    if isinstance(l, list) and isinstance(r, int):
        return compare(l, [r])
    if isinstance(l, int) and isinstance(r, list):
        return compare([l], r)


sections = get_sections(lines)
for i, section in enumerate(sections, start=1):
    first, second = section
    first = json.loads(first)
    second = json.loads(second)
    if compare(first, second) <= 0:
        ans1 += i

all = [json.loads(s) for section in sections for s in section]

divider1 = [[2]]
divider2 = [[6]]
all.append(divider1)
all.append(divider2)
all.sort(key=cmp_to_key(compare))
ans2 = 1

for i, l in enumerate(all, start=1):
    if l in (divider1, divider2):
        ans2 *= i

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
