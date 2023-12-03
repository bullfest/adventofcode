#!/usr/bin/env python3
import dataclasses
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
    for l in reversed(transpose(g)):
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


year = 2022
day = 23

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


@dataclasses.dataclass
class Elf:
    id: int
    x: int
    y: int


elves: dict[tuple[int, int], Elf | None] = defaultdict(lambda: None)
i = 0
for y, l in enumerate(reversed(lines)):
    for x, c in enumerate(l):
        if c == "#":
            elves[(x, y)] = Elf(i, x, y)
            i += 1

direction = ("N", "S", "W", "E")


def print_elves(elves):
    min_x = min(e.x for e in elves.values())
    max_x = max(e.x for e in elves.values())
    min_y = min(e.y for e in elves.values())
    max_y = max(e.y for e in elves.values())
    grid = [["."] * (max_y - min_y + 1) for _ in range(max_x - min_x + 1)]
    for e in elves.values():
        grid[e.x - min_x][e.y - min_y] = "#"
    print_grid(grid)


for r in range(1000):
    if r == 10:
        min_x = min(e.x for e in elves.values())
        max_x = max(e.x for e in elves.values())
        min_y = min(e.y for e in elves.values())
        max_y = max(e.y for e in elves.values())

        ans1 = (max_x - min_x + 1) * (max_y - min_y + 1) - len(elves)
        print("1:", ans1)

    proposed_positions: dict[tuple[int, int], list[Elf]] = defaultdict(list)
    for e in elves.values():
        x, y = e.x, e.y
        neighbours = {
            (x - 1, y - 1),
            (x - 1, y),
            (x - 1, y + 1),
            (x, y + 1),
            (x + 1, y + 1),
            (x + 1, y),
            (x + 1, y - 1),
            (x, y - 1),
        }
        assert len(neighbours) == 8
        if all(p not in elves for p in neighbours):
            proposed_positions[(x, y)].append(e)
            continue
        moved = False
        for d in direction[r % 4 :] + direction[: r % 4]:
            if d == "N" and all(p not in elves for p in ((x - 1, y + 1), (x, y + 1), (x + 1, y + 1))):
                proposed_positions[(x, y + 1)].append(e)
                moved = True
                break
            if d == "S" and all(p not in elves for p in ((x - 1, y - 1), (x, y - 1), (x + 1, y - 1))):
                proposed_positions[(x, y - 1)].append(e)
                moved = True
                break
            if d == "W" and all(p not in elves for p in ((x - 1, y - 1), (x - 1, y), (x - 1, y + 1))):
                proposed_positions[(x - 1, y)].append(e)
                moved = True
                break
            if d == "E" and all(p not in elves for p in ((x + 1, y - 1), (x + 1, y), (x + 1, y + 1))):
                proposed_positions[(x + 1, y)].append(e)
                moved = True
                break
        if not moved:
            proposed_positions[(x, y)].append(e)

    new_elves: dict[tuple[int, int], Elf | None] = defaultdict(lambda: None)
    for pos, prop_elves in proposed_positions.items():
        if len(prop_elves) > 1:
            for elf in prop_elves:
                new_elves[(elf.x, elf.y)] = elf
        else:
            assert new_elves[pos] is None
            elf = next(iter(prop_elves))
            elf.x = pos[0]
            elf.y = pos[1]
            new_elves[pos] = elf
    assert len(elves) == len(new_elves)
    # Part 2
    if set(new_elves.keys()) == set(elves.keys()):
        ans2 = r + 1
        break

    elves = new_elves

###########
print("2:", ans2)

if filename == "input":
    submit = input("submit?")
    if "y" in submit.lower():
        if ans1 != 0:
            aocd.submit(ans1, year=year, day=day, part="a")
        if ans2 != 0:
            aocd.submit(ans2, year=year, day=day, part="b")
