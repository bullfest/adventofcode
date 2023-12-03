import sys
import q
import itertools
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
        # print("".join(map(lambda n: "#" if n == 1 else ".", l)))
    print()


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
sections = get_sections(lines)
enhance_alg = "".join(sections[0])
mappy = get_grid(sections[1])


def pixel_value(m, x, y, outside):
    bits = []
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if x + dx < 0 or y + dy < 0 or x + dx >= len(m) or y + dy >= len(m[0]):
                bits.append(outside)
                continue
            c = m[x + dx][y + dy]
            if c == ".":
                bits.append(0)
            elif c == "#":
                bits.append(1)
    # print(bits)
    n = int("".join(map(str, bits)), 2)
    return enhance_alg[n]


def enhance(m, outside):
    new_m = [[0] * (len(m[0]) + 2) for _ in range(len(m) + 2)]
    for x in range(len(new_m)):
        for y in range(len(new_m[0])):
            new_m[x][y] = pixel_value(m, x - 1, y - 1, outside)
    return new_m


odd_outside = 1 if enhance_alg[0] == "#" else 0

for i in range(50):
    if i % 2 == 0:
        mappy = enhance(mappy, 0)
    else:
        mappy = enhance(mappy, odd_outside)

    if i == 1:
        ans1 = 0
        for l in mappy:
            for c in l:
                if c == "#":
                    ans1 += 1
ans2 = 0
for l in mappy:
    for c in l:
        if c == "#":
            ans2 += 1

print("1:", ans1)
print("2:", ans2)
