#!/usr/bin/env python3
import sys
import re
import q
import itertools as it
import math
import aocd
import dataclasses
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


if len(sys.argv) > 1:
    filename = sys.argv[1]
    with open(filename) as file:
        lines = [l.strip("\n") for l in file]
else:
    filename = "input"
    lines = aocd.get_data().split("\n")

print("len(lines)", len(lines))
ans1 = 0
ans2 = 0

ds = []


@dataclass
class Node:
    name: str
    parent: "Node"
    children: Dict = dataclasses.field(default_factory=dict)
    size: int = None
    _size_m = None

    def add_child(self, n: "Node"):
        if n.name not in self.children:
            self.children[n.name] = n

    def r_size(self):
        if self._size_m is not None:
            return self._size_m
        if self.size is not None:
            return self.size
        s = 0
        for n in self.children.values():
            s += n.r_size()
        ds.append(s)
        self._size_m = s
        return s

    def dir_sizes_smaller_than(self, i: int):
        s = 0
        for n in self.children.values():
            if n.size is None:
                s += n.dir_sizes_smaller_than(i)

        if self._size_m < i:
            s += self._size_m
        return s


h = Node(name="/", parent=None)
h.parent = h
curr = h
for l in lines:
    if l.startswith("$ cd"):
        directory = l.split()[2]
        if directory == "/":
            curr = h
            continue
        elif directory == "..":
            curr = curr.parent
            continue
        print(directory)
        if directory not in curr.children:
            print(curr.name, curr.children.keys())
        curr = curr.children[directory]
    elif l.startswith("$ ls"):
        continue
    elif l.startswith("dir"):
        name = l.split()[1]
        n = Node(name=name, parent=curr)
        curr.add_child(n)
    else:
        size, name = l.split()
        size = int(size)
        n = Node(name=name, parent=curr, size=size)
        curr.add_child(n)

free_space = 70000000 - h.r_size()
ans1 = h.dir_sizes_smaller_than(100000)
needed_space = 30000000 - free_space


ds.sort()
for i in ds:
    if i < needed_space:
        continue
    ans2 = i
    break
print("1:", ans1)
print("2:", ans2)

if filename == "input":
    submit = input("submit?")
    if "y" in submit.lower():
        if ans1 != 0:
            aocd.submit(ans1, part="a")
        if ans2 != 0:
            aocd.submit(ans2, part="b")
