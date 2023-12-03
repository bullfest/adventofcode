#!/usr/bin/env python3
import sys
import re
import q
import itertools as it
import math
import aocd
from typing import List, Tuple
from dataclasses import dataclass
from collections import defaultdict


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
day = 11

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
monkeys = []


@dataclass
class Rule:
    div: int
    t_target: int
    f_target: int


@dataclass
class Monkey:
    items: List[int]
    rules: List[Rule]
    operation: List[str]
    n: int = 0

    def do_op(self, i: int) -> int:
        op, v = self.operation
        if op == "+":
            if v == "old":
                return i + i
            else:
                return i + int(v)
        elif op == "*":
            if v == "old":
                return i * i
            else:
                return i * int(v)
        assert False

    def take_turn(self):
        for i in self.items:
            self.n += 1
            i = self.do_op(i)
            # i = i//3
            i %= mod
            for r in self.rules:
                if i % r.div == 0:
                    monkeys[r.t_target].items.append(i)
                else:
                    monkeys[r.f_target].items.append(i)
        self.items = []


mod = 1

for s in get_sections(lines):
    _, items, op, test, ttest, ftest = s
    items = items.split()[2:]
    items = [int(i.strip(",")) for i in items]
    op = op.split()[4:]
    test = int(test.split()[-1])
    ttest = int(ttest.split()[-1])
    ftest = int(ftest.split()[-1])
    mod *= test
    monkeys.append(
        Monkey(
            items=items,
            rules=[Rule(div=test, t_target=ttest, f_target=ftest)],
            operation=op,
        )
    )

for m in monkeys:
    print(m.items, m.operation)

for i in range(10000):
    if i % 100 == 0:
        print(i)
    for m in monkeys:
        m.take_turn()


ns = [m.n for m in monkeys]
print(ns)
ns.sort()
ans2 = ns[-2] * ns[-1]


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
