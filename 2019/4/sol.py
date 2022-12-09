import sys
import q
import itertools as it
import math
import time
import copy
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


def next(n):
    n = list(n)
    for i in range(len(n) - 1, -1, -1):
        if n[i] < 9:
            n[i] += 1
            break
        else:
            n[i] = 0

    for i in range(len(n) - 1):
        if n[i] > n[i + 1]:
            for i2 in range(i, len(n)):
                n[i2] = n[i]
            break

    return tuple(n)


def smallest_double(n):
    c = 1
    sm = 1000
    for i in range(len(n) - 1):
        if n[i] == n[i + 1]:
            c += 1
        else:
            if c > 1:
                sm = min(sm, c)
            c = 1
    if c > 1:
        sm = min(sm, c)
    if sm != 1000:
        return sm
    return 0


if __name__ == "__main__":
    lines = [l.strip() for l in sys.stdin]
    start, end = lines[0].split("-")
    start = tuple(map(int, start))
    end = tuple(map(int, end))
    print(start, end)
    assert start < end

    ans1 = 0
    ans2 = 0
    n = next(start)
    while n < end:
        d = smallest_double(n)
        if d and d > 1:
            ans1 += 1
        if d and d == 2:
            ans2 += 1
        n = next(n)

    print("1:", ans1)
    print("2:", ans2)
