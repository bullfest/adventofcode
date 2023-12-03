#!/usr/bin/env python3
import dataclasses
import sys
from functools import cached_property

import z3
import aocd
from collections import defaultdict


year = 2022
day = 15

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
class Sensor:
    x: int
    y: int
    beacon_x: int
    beacon_y: int

    @cached_property
    def distance_to_beacon(self):
        return abs(self.x - self.beacon_x) + abs(self.y - self.beacon_y)

    def seen_cells_in_row(self, y: int):
        dx = self.distance_to_beacon - abs(self.y - y)
        if dx < 0:
            return set()
        s = set(range(self.x - dx, self.x + dx + 1))
        return s

    def boundary(self, y):
        dx = self.distance_to_beacon - abs(self.y - y)
        if dx < 0:
            return (-1, -1)
        return (self.x - dx, self.x + dx)


beacons = defaultdict(set)
sensors = []
for l in lines:
    l = l.split()
    x = int(l[2].strip(",").split("=")[1])
    y = int(l[3].strip(":").split("=")[1])
    b_x = int(l[8].strip(",").split("=")[1])
    b_y = int(l[9].split("=")[1])
    beacons[b_y].add(b_x)
    sensors.append(
        Sensor(
            x=x,
            y=y,
            beacon_x=b_x,
            beacon_y=b_y,
        )
    )

seen = defaultdict(set)
line = 2000000
for s in sensors:
    seen[line] |= s.seen_cells_in_row(line)

for by in beacons:
    seen[by] -= beacons[by]

ans1 = len(seen[line])
print("1:", ans1)

max_v = 20
if filename == "input":
    max_v = 4000000
solver = z3.Solver()
x = z3.Int("x")
y = z3.Int("y")
solver.add(0 <= x)
solver.add(x <= max_v)
solver.add(0 <= y)
solver.add(y <= max_v)


def zabs(x):
    return z3.If(x >= 0, x, -x)


for i, s in enumerate(sensors):
    solver.add(zabs(x - s.x) + zabs(y - s.y) > s.distance_to_beacon)

solver.check()
model = solver.model()

ans2 = 4000000 * model[x].as_long() + model[y].as_long()

###########
print("2:", ans2)

if filename == "input":
    submit = input("submit?")
    if "y" in submit.lower():
        if ans1 != 0:
            aocd.submit(ans1, year=year, day=day, part="a")
        if ans2 != 0:
            aocd.submit(ans2, year=year, day=day, part="b")
