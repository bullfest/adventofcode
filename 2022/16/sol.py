#!/usr/bin/env python3
import dataclasses
import datetime
import functools
import sys
import aocd
from typing import FrozenSet, Dict
from collections import defaultdict


# sys.setrecursionlimit(100000)


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
day = 16

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
t0 = datetime.datetime.now()
print("t0", t0.isoformat())


############
# SOLUTION #
############


@dataclasses.dataclass
class Valve:
    name: str
    flow_rate: int
    tunnels: Dict[str, int]

    @functools.cached_property
    def abbr_tunnels(self) -> Dict[str, int]:
        todo = [(self.name, 0)]
        distance = defaultdict(lambda: 10000000)
        while todo:
            v, d = todo.pop()
            if d >= distance[v]:
                continue
            distance[v] = d
            for n in valves[v].tunnels:
                todo.append((n, d + 1))
        distance = {
            n: d
            for n, d in distance.items()
            if valves[n].flow_rate != 0 and n != self.name
        }
        return distance


valves = {}

for l in lines:
    l = l.split()
    name = l[1]
    flow_rate = int(l[4].split("=")[1].strip(";"))
    tunnels = [n.strip(",") for n in l[9:]]
    valves[name] = Valve(
        name=name,
        flow_rate=flow_rate,
        tunnels={t: 1 for t in tunnels},
    )


@functools.cache
def solve1(time: int, pos: str, open: FrozenSet[str]) -> int:
    if time <= 0:
        return 0
    best = 0
    best_open = open
    curr_valve = valves[pos]
    for next_pos, d in curr_valve.abbr_tunnels.items():
        new_time = time - d - 1
        if next_pos not in open and new_time > 0:
            next_valve = valves[next_pos]
            score, this_open = solve1(new_time, next_pos, open.union({pos}))
            score += next_valve.flow_rate * new_time
            if score > best:
                best = score
                best_open = this_open

    return best, best_open


ans1, _ = solve1(30, "AA", frozenset())
t1 = datetime.datetime.now()
print("1:", ans1, "dt", t1 - t0, "t1", t1.isoformat())

# This works for the real input but not for the example
# s1, open1 = solve1(26, "AA", frozenset())
# s2, _ = solve1(26, "AA", open1)
# ans2 = s1+s2


@functools.cache
def solve2(time_me: int, time_e, pos: str, epos: str, open: FrozenSet[str]) -> int:
    best = 0
    if time_me > 1:
        curr_valve = valves[pos]
        for next_pos, d in curr_valve.abbr_tunnels.items():
            if next_pos not in open and time_me - d - 1 > 0:
                next_valve = valves[next_pos]
                if next_valve.flow_rate == 0:
                    continue
                best = max(
                    best,
                    solve2(
                        time_me - d - 1, time_e, next_pos, epos, open.union({next_pos})
                    )
                    + next_valve.flow_rate * (time_me - d - 1),
                )
    if time_e > 1:
        curr_valve = valves[epos]
        for next_pos, d in curr_valve.abbr_tunnels.items():
            if next_pos not in open and time_e - d - 1 > 0:
                next_valve = valves[next_pos]
                if next_valve.flow_rate == 0:
                    continue
                best = max(
                    best,
                    solve2(
                        time_me, time_e - d - 1, pos, next_pos, open.union({next_pos})
                    )
                    + next_valve.flow_rate * (time_e - d - 1),
                )
    return best


ans2 = solve2(26, 26, "AA", "AA", frozenset())
t2 = datetime.datetime.now()
print("2:", ans2, "dt", t2 - t1, "t2", t2.isoformat())

###########

if filename == "input":
    if ans1 != 0:
        aocd.submit(ans1, year=year, day=day, part="a")
    if ans2 != 0:
        aocd.submit(ans2, year=year, day=day, part="b")
