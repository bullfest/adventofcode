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


if len(sys.argv) > 1:
    filename = sys.argv[1]
    with open(filename) as file:
        lines = [l.strip("\n") for l in file]
else:
    filename = "input"
    lines = aocd.get_data(year=2022, day=9).split("\n")

print("len(lines)", len(lines))
ans1 = 0
ans2 = 0

visited = set()


@dataclass
class Point:
    x: int = 0
    y: int = 0

    def step(self, d):
        if d == "R":
            self.x += 1
        if d == "L":
            self.x -= 1
        if d == "U":
            self.y += 1
        if d == "D":
            self.y -= 1

    def follow(self, h: "Point"):
        if abs(self.x - h.x) <= 1 and abs(self.y - h.y) <= 1:
            return
        if self.x == h.x:
            if self.y < h.y:
                self.y += 1
            else:
                self.y -= 1
        elif self.y == h.y:
            if self.x < h.x:
                self.x += 1
            else:
                self.x -= 1
        else:
            # diagonal
            if self.x < h.x and self.y < h.y:
                self.x += 1
                self.y += 1
            elif self.x < h.x and self.y > h.y:
                self.x += 1
                self.y -= 1
            elif self.x > h.x and self.y < h.y:
                self.x -= 1
                self.y += 1
            elif self.x > h.x and self.y > h.y:
                self.x -= 1
                self.y -= 1


h = Point()
t = Point()

for move in lines:
    d, c = move.split()
    c = int(c)
    for _ in range(c):
        h.step(d)
        t.follow(h)
        visited.add((t.x, t.y))

ans1 = len(visited)

visited2 = set()

rope = [Point() for _ in range(10)]
for move in lines:
    d, c = move.split()
    c = int(c)
    for _ in range(c):
        rope[0].step(d)
        for i in range(9):
            rope[i + 1].follow(rope[i])
        t = rope[-1]
        visited2.add((t.x, t.y))

ans2 = len(visited2)

print("1:", ans1)
print("2:", ans2)

if filename == "input":
    submit = input("submit?")
    if "y" in submit.lower():
        if ans1 != 0:
            aocd.submit(ans1, year=2022, day=9, part="a")
        if ans2 != 0:
            aocd.submit(ans2, year=2022, day=9, part="b")
