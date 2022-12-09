import sys
import q
import itertools as it
import math
from typing import List, Tuple
from dataclasses import dataclass
from collections import defaultdict


def transpose(m):
    return list(map(list, zip(*m)))


def get_sections(lines):
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
    f = f or (lambda x: x)
    return transpose([list(map(f, l if sep is None else l.split(sep))) for l in lines])


def print_grid(g):
    for l in transpose(g):
        print("".join(l))
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


lines = [l.strip() for l in sys.stdin]
cukes = get_grid(lines)
max_x = len(cukes)
max_y = len(cukes[0])
downs = {(x, y) for x in range(max_x) for y in range(max_y) if cukes[x][y] == "v"}
rights = {(x, y) for x in range(max_x) for y in range(max_y) if cukes[x][y] == ">"}


def right(p):
    x, y = p
    return (x + 1) % max_x, y


def down(p):
    x, y = p
    return x, (y + 1) % max_y


ans1 = 0
moved = True
while moved:
    ans1 += 1

    occupado = rights | downs
    new_rights = {p if right(p) in occupado else right(p) for p in rights}
    occupado = new_rights | downs
    new_downs = rights = {p if down(p) in occupado else down(p) for p in downs}
    herd = rights | downs
    new_herd = new_rights | new_downs
    moved = herd != new_herd
    rights = new_rights
    downs = new_downs
print("1:", ans1)
