import sys
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


lines = [l.strip().split() for l in sys.stdin]
beats = {"X": "C", "Y": "A", "Z": "B"}
draw = {"X": "A", "Y": "B", "Z": "C"}
loose = {"X": "B", "Y": "C", "Z": "A"}
cscore = {"X": 1, "Y": 2, "Z": 3}

ans1 = 0
for l in lines:
    op, me = l
    ans1 += cscore[me]
    if beats[me] == op:
        ans1 += 6
    if draw[me] == op:
        ans1 += 3

beat = {v: k for k, v in beats.items()}
draw = {v: k for k, v in draw.items()}
loose = {v: k for k, v in loose.items()}

ans2 = 0
for l in lines:
    op, me = l
    if me == "X":  # loose
        choice = loose[op]
        ans2 += cscore[choice]
    if me == "Y":  # draw
        choice = draw[op]
        ans2 += 3 + cscore[choice]
    if me == "Z":  # win
        choice = beat[op]
        ans2 += 6 + cscore[choice]


print("1:", ans1)
print("2:", ans2)
