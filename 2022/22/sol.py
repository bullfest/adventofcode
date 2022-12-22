#!/usr/bin/env python3
import dataclasses
import sys
import re
import q
import itertools as it
import math
import aocd
from typing import List, Tuple, Dict
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
day = 22

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

parts = get_sections(lines)
map = parts[0]
path_str = parts[1][0]
max_x = max(len(l) for l in map)
max_y = len(map)
OUTSIDE = -1
EMPTY = 0
WALL = 1
grid = [[OUTSIDE for _ in range(max_y)] for _ in range(max_x)]
for y, l in enumerate(lines):
    for x, c in enumerate(l):
        if c == ".":
            grid[x][y] = EMPTY
        elif c == "#":
            grid[x][y] = WALL

RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3

y_start = 0
x_start = 0
dir_start = RIGHT
for x0 in range(max_x):
    if grid[x0][y_start] == EMPTY:
        x_start = x0
        break

part_regex = re.compile("(\d+|[RL])")
path = []
for match in part_regex.findall(path_str):
    if match.isdigit():
        match = int(match)
    path.append(match)


@dataclasses.dataclass
class Node:
    pos: Tuple[int, int]
    neighs: Dict[int, Tuple[int, "Node"]]
    content: int


nodes = {}
for x in range(max_x):
    for y in range(max_y):
        if grid[x][y] == OUTSIDE:
            continue
        nodes[(x, y)] = Node(pos=(x, y), neighs={}, content=grid[x][y])
start_node = nodes[(x_start, y_start)]

### Part 1
x = x_start
y = y_start
dir = dir_start


def forward1():
    global x, y
    dx, dy = 0, 0
    if dir == RIGHT:
        dx, dy = (1, 0)
    elif dir == DOWN:
        dx, dy = (0, 1)
    elif dir == LEFT:
        dx, dy = (-1, 0)
    elif dir == UP:
        dx, dy = (0, -1)
    x1 = (x + dx) % max_x
    y1 = (y + dy) % max_y
    while grid[x1][y1] == OUTSIDE:
        x1 = (x1 + dx) % max_x
        y1 = (y1 + dy) % max_y
    if grid[x1][y1] == WALL:
        return
    x = x1
    y = y1
    return


for p in path:
    if isinstance(p, int):
        for _ in range(p):
            forward1()
        continue
    if p == "L":
        dir -= 1
    if p == "R":
        dir += 1

    dir %= 4

ans1 = 1000 * (y + 1) + 4 * (x + 1) + dir
print("1:", ans1)

# Part 2

# Obvious neighbours
for n in nodes.values():
    x, y = n.pos
    if (x + 1, y) in nodes:
        n.neighs[RIGHT] = (RIGHT, nodes[(x + 1, y)])
    if (x, y + 1) in nodes:
        n.neighs[DOWN] = (DOWN, nodes[(x, y + 1)])
    if (x - 1, y) in nodes:
        n.neighs[LEFT] = (LEFT, nodes[(x - 1, y)])
    if (x, y - 1) in nodes:
        n.neighs[UP] = (UP, nodes[(x, y - 1)])

#     ab
#    z##y
#    q#x
#   z##y
#   a#c
#    b

# Cube neighbours
zips = [
    # x
    (1, 0, {(x, 49): (99, y) for x, y in zip(range(100, 150), range(50, 100))}),
    (0, 1, {(99, y): (x, 49) for x, y in zip(range(100, 150), range(50, 100))}),
    # y
    (0, 0, {(149, y1): (99, y2) for y1, y2 in zip(range(0, 50), reversed(range(100, 150)))}),
    (0, 0, {(99, y2): (149, y1) for y1, y2 in zip(range(0, 50), reversed(range(100, 150)))}),
    # q
    (2, 3, {(50, y): (x, 100) for y, x in zip(range(50, 100), range(0, 50))}),
    (3, 2, {(x, 100): (50, y) for y, x in zip(range(50, 100), range(0, 50))}),
    # c
    (1, 0, {(x, 149): (49, y) for x, y in zip(range(50, 100), range(150, 200))}),
    (0, 1, {(49, y): (x, 149) for x, y in zip(range(50, 100), range(150, 200))}),
    # z
    (2, 2, {(50, y1): (0, y2) for y1, y2 in zip(range(0, 50), reversed(range(100, 150)))}),
    (2, 2, {(0, y2): (50, y1) for y1, y2 in zip(range(0, 50), reversed(range(100, 150)))}),
    # a
    (3, 2, {(x, 0): (0, y) for x, y in zip(range(50, 100), range(150, 200))}),
    (2, 3, {(0, y): (x, 0) for x, y in zip(range(50, 100), range(150, 200))}),
    # b
    (3, 1, {(x1, 0): (x2, 199) for x1, x2 in zip(range(100, 150), range(0, 50))}),
    (1, 3, {(x2, 199): (x1, 0) for x1, x2 in zip(range(100, 150), range(0, 50))}),
]
for d, rd, g in zips:
    for n1, n2 in g.items():
        assert d not in nodes[n1].neighs
        nodes[n1].neighs[d] = ((rd + 2) % 4, nodes[n2])
# Sanity - all nodes has a neighbour
for node in nodes.values():
    for dir in range(4):
        assert dir in node.neighs
        d, n = node.neighs[dir]
        opposite = (d + 2) % 4
        _, same = n.neighs[opposite]
        assert same == node, f"{node.pos} != {same.pos} ({n.pos})"

node = start_node
dir = dir_start


def forward2():
    global node, dir
    new_dir, next_node = node.neighs[dir]
    if next_node.content == EMPTY:
        dir = new_dir
        node = next_node
        print(node.pos)


for p in path:
    if isinstance(p, int):
        for _ in range(p):
            forward2()
        continue
    if p == "L":
        dir -= 1
    if p == "R":
        dir += 1

    dir %= 4

ans2 = 1000 * (node.pos[1] + 1) + 4 * (node.pos[0] + 1) + dir
###########
print("2:", ans2)

if filename == "input":
    submit = input("submit?")
    if "y" in submit.lower():
        if ans1 != 0:
            aocd.submit(ans1, year=year, day=day, part="a")
        if ans2 != 0:
            aocd.submit(ans2, year=year, day=day, part="b")
