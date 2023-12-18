#!/usr/bin/env python3
import itertools
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


def set_min_x(n: int):
    global min_x
    min_x = aoclib.min_x = n


def set_min_y(n: int):
    global min_y
    min_y = aoclib.min_y = n


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
day = 18


def run():
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

    # "Stupid" p1
    trench = set()
    x, y = 0, 0
    max_x = 0
    max_y = 0
    min_x = 0
    min_y = 0
    for l in lines:
        d, n, _ = l.split()
        n = int(n)
        match d:
            case "R":
                dx, dy = (1, 0)
            case "L":
                dx, dy = (-1, 0)
            case "D":
                dx, dy = (0, 1)
            case "U":
                dx, dy = (0, -1)
        for _ in range(n):
            trench.add((x, y))
            x += dx
            y += dy
        min_x = min(x, min_x)
        min_y = min(y, min_y)
        max_x = max(x, max_x)
        max_y = max(y, max_y)
    assert x == 0
    assert y == 0
    max_x += 1
    max_y += 1
    set_max_x(max_x)
    set_max_y(max_y)
    set_min_x(min_x)
    set_min_y(min_y)

    inside = None
    x = 1
    y = max_y // 2
    while not inside:
        if (x - 1, y) in trench and (x, y) not in trench:
            inside = (x, y)
        x += 1

    dfs = [inside]
    seen = set()
    while dfs:
        n = dfs.pop()
        if n in seen:
            continue
        seen.add(n)
        for n1 in neighbours(*n):
            if n1 in trench:
                continue
            dfs.append(n1)

    print("edge", len(trench))
    ans1 = len(trench) + len(seen)

    # P1 like P2
    x, y = 0, 0
    corners = []
    edge_length = 0
    for l in lines:
        d, n, _ = l.split()
        n = int(n)
        dx, dy = 0, 0
        match d:
            case "R":
                dx = 1
            case "D":
                dy = 1
            case "L":
                dx = -1
            case "U":
                dy = -1
        x = x + dx * n
        y = y + dy * n
        corners.append((x, y))
        edge_length += n

    ans1b = polygon_area(corners)
    ans1b = round(ans1b)
    assert ans1 == ans1b
    # P2
    x, y = 0, 0
    corners = []
    edge_length = 0
    for l in lines:
        _, _, c = l.split()
        c = c.strip("(#)")
        n = int(c[:5], 16)
        d = int(c[5])
        dx, dy = 0, 0
        match d:
            case 0:
                dx = 1
            case 1:
                dy = 1
            case 2:
                dx = -1
            case 3:
                dy = -1
        x = x + dx * n
        y = y + dy * n
        corners.append((x, y))
        edge_length += n

    ans2 = polygon_area(corners)
    ans2 = round(ans2)

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


if __name__ == "__main__":
    run()
