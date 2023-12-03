#!/usr/bin/env python3
import copy
import functools
import sys
import re
import q
import itertools as it
import math
import aocd
from typing import List, Tuple
from dataclasses import dataclass
from collections import defaultdict

import z3


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
day = 21

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
monkeys = {}
for l in lines:
    monkey, op = l.split(": ")
    op: str
    if op.isdigit():
        monkeys[monkey] = int(op)
        continue
    monkeys[monkey] = op.split(" ")


#### Defunct part 1 solution
def value(name):
    if isinstance(monkeys[name], int):
        return monkeys[name]
    instr = monkeys[name]
    if instr[1] == "+":
        return value(instr[0]) + value(instr[2])
    if instr[1] == "-":
        return value(instr[0]) - value(instr[2])
    if instr[1] == "*":
        return value(instr[0]) * value(instr[2])
    if instr[1] == "/":
        return value(instr[0]) // value(instr[2])


ans1 = value("root")

#### Z3-based solution for both parts

solver = z3.Solver()
human = z3.Real("humn")
root = z3.Real("root")
vars = {"humn": human, "root": root}
for monkey in monkeys:
    if monkey in ("humn", "root)"):
        continue
    vars[monkey] = z3.Real(monkey)


def add_constraint(solver, monkey):
    instr = monkeys[monkey]
    var = vars[monkey]
    if isinstance(instr, int):
        solver.add(var == instr)
        return
    left = vars[instr[0]]
    right = vars[instr[2]]
    if instr[1] == "+":
        solver.add(left + right == var)
    if instr[1] == "-":
        solver.add(left - right == var)
    if instr[1] == "*":
        solver.add(left * right == var)
    if instr[1] == "/":
        solver.add(left / right == var)


for monkey in monkeys:
    if monkey in ("humn", "root"):
        continue
    add_constraint(solver, monkey)

p1_solver = copy.deepcopy(solver)
add_constraint(p1_solver, "humn")
add_constraint(p1_solver, "root")
p1_solver.check()
model = p1_solver.model()
ans1 = model[root].as_long()

p2_solver = copy.deepcopy(solver)
root_left = monkeys["root"][0]
root_left = vars[root_left]
root_right = monkeys["root"][2]
root_right = vars[root_right]
p2_solver.add(root_left == root_right)
p2_solver.check()
model = p2_solver.model()
ans2 = model[human].as_long()

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
