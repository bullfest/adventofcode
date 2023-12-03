#!/usr/bin/env python3
import dataclasses
import sys
import re
from functools import cached_property

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
day = 20

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
class LL:
    prev: "LL"
    next: "LL"
    i: int

    @cached_property
    def delta(self):
        i = self.i
        return i % (len(lines) - 1)

    def swap_next(self):
        # s.p - s - n - n.n
        # n.p - n - s - s.n
        n = self.next

        n.prev = self.prev
        n.prev.next = n

        self.next = n.next
        self.next.prev = self

        n.next = self
        self.prev = n

    def swap_prev(self):
        # n.p - n - s - s.n
        # s.p - s - n - n.n

        n = self.prev

        self.prev = n.prev
        self.prev.next = self

        n.next = self.next
        n.next.prev = n

        self.next = n
        n.prev = self


key = 811589153


def print_ll(n: LL):
    res = []
    for _ in range(len(lines)):
        res.append(n.i)
        n = n.next
    print(res)


def create_nodes(numbers) -> Tuple[List[LL], LL]:
    node = LL(None, None, numbers[0])
    node.next = node.prev = node
    zero_node = node
    nodes = [node]
    for i in numbers[1:]:
        new_node = LL(
            prev=nodes[-1],
            next=nodes[0],
            i=i,
        )
        if i == 0:
            zero_node = new_node
        nodes[-1].next = new_node
        nodes[0].prev = new_node
        nodes.append(new_node)
    return nodes, zero_node


def shuffle(nodes):
    for n in nodes:
        if n.i != 0:
            for _ in range(n.delta):
                n.swap_next()
        else:
            zero_node = n


def compute_answer(node) -> int:
    ans = 0
    for _ in range(3):
        for _ in range(1000):
            node = node.next
        ans += node.i
    return ans


def part1():
    nodes, zero_node = create_nodes(parse_ints(*lines))
    shuffle(nodes)
    return compute_answer(zero_node)


def part2():
    nodes, zero_node = create_nodes(parse_ints(*lines))
    for node in nodes:
        node.i *= key
    for i in range(10):
        shuffle(nodes)
        print("part2:", i + 1, "out of 10")
    return compute_answer(zero_node)


ans1 = part1()
print("1:", ans1)
ans2 = part2()
print("2:", ans2)

###########

if filename == "input":
    submit = input("submit?")
    if "y" in submit.lower():
        if ans1 != 0:
            aocd.submit(ans1, year=year, day=day, part="a")
        if ans2 != 0:
            aocd.submit(ans2, year=year, day=day, part="b")
