#!/usr/bin/env python3
import dataclasses
import functools
import sys
from time import sleep
import re
import q
import itertools as it
import math
import aocd
from typing import List, Tuple
from dataclasses import dataclass
from collections import defaultdict

import z3


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
day = 19

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
class Blueprint:
    id: int
    ore_cost: int
    clay_cost: int
    obsidian_cost: Tuple[int, int]  # ore, clay
    geode_cost: Tuple[int, int]  # ore, obsidian

    @functools.cached_property
    def max_ore(self):
        return max(
            self.ore_cost, self.clay_cost, self.obsidian_cost[0], self.geode_cost[0]
        )

    @functools.cached_property
    def max_clay(self):
        return self.obsidian_cost[1]

    @functools.cached_property
    def max_obsidian(self):
        return self.geode_cost[1]


@dataclasses.dataclass
class State:
    pass


blueprints = []
for i, l in enumerate(lines):
    parts = l.split(":")[1].split(".")
    obs_part = parts[2].split()
    geo_part = parts[3].split()
    blueprints.append(
        Blueprint(
            id=i + 1,
            ore_cost=int(parts[0].split()[-2]),
            clay_cost=int(parts[1].split()[-2]),
            obsidian_cost=(int(obs_part[-5]), int(obs_part[-2])),
            geode_cost=(int(geo_part[-5]), int(geo_part[-2])),
        )
    )

dp = {}


def solve(bp: Blueprint, time=24):
    """Basically 3 ways to reduce search space:
    The first 2 are arguably always correct:
    Never build more robots than the maximum cost for that resource, there's no need for 10 ore robots if we only can use 5 ore each minute.
    Don't store more of a resource than what we can use if we consume the max of it each minute for the rest of the time.

    The last one feels like there might be edge cases where it's not optimal, but it works:
    If we can build a geode robot, always build one.
    """
    states = set()
    states.add((1, 0, 0, 0, 0, 0, 0, 0))
    new_states = states
    max_geo = 0
    for t in range(time):
        states = new_states
        max_geo = 0
        new_states = set()
        for state in states:
            ore_r, clay_r, obs_r, geo_r, ore, clay, obs, geo = state
            new_ore = ore + ore_r
            new_ore = min(new_ore, (time - 1 - t) * bp.max_ore)
            new_clay = clay + clay_r
            new_clay = min(new_clay, (time - 1 - t) * bp.max_clay)
            new_obs = obs + obs_r
            new_obs = min(new_obs, (time - 1 - t) * bp.max_obsidian)
            new_geo = geo + geo_r
            max_geo = max(new_geo, max_geo)
            new_states.add((*state[:4], new_ore, new_clay, new_obs, new_geo))
            if ore >= bp.geode_cost[0] and obs >= bp.geode_cost[1]:
                # Heuristic: Always buy a geode robot if we can, the idea is that it's important to buy them early to
                # make sure that we maximize their output
                # I imagine that there might be some data for which this doesn't work... but it seems to work here
                new_states.add(
                    (
                        ore_r,
                        clay_r,
                        obs_r,
                        geo_r + 1,
                        new_ore - bp.geode_cost[0],
                        new_clay,
                        new_obs - bp.geode_cost[1],
                        new_geo,
                    )
                )
                continue
            if (
                ore >= bp.obsidian_cost[0]
                and clay >= bp.obsidian_cost[1]
                and obs_r < bp.max_obsidian
            ):
                new_states.add(
                    (
                        ore_r,
                        clay_r,
                        obs_r + 1,
                        geo_r,
                        new_ore - bp.obsidian_cost[0],
                        new_clay - bp.obsidian_cost[1],
                        new_obs,
                        new_geo,
                    )
                )
            if ore >= bp.ore_cost and ore_r < bp.max_ore:
                new_states.add(
                    (
                        ore_r + 1,
                        clay_r,
                        obs_r,
                        geo_r,
                        new_ore - bp.ore_cost,
                        new_clay,
                        new_obs,
                        new_geo,
                    )
                )
            if ore >= bp.clay_cost and clay_r < bp.max_clay:
                new_states.add(
                    (
                        ore_r,
                        clay_r + 1,
                        obs_r,
                        geo_r,
                        new_ore - bp.clay_cost,
                        new_clay,
                        new_obs,
                        new_geo,
                    )
                )
        print(bp.id, t, len(states), max_geo)
    return max_geo


for bp in blueprints:
    s = solve(bp)
    print("---------------")
    ans1 += bp.id * s
print("1:", ans1)
ans2 = 1
for bp in blueprints[:3]:
    s = solve(bp, time=32)
    print("---------------")
    ans2 *= s

###########
print("2:", ans2)

if filename == "input":
    submit = input("submit?")
    if "y" in submit.lower():
        if ans1 != 0:
            aocd.submit(ans1, year=year, day=day, part="a")
        if ans2 != 0:
            aocd.submit(ans2, year=year, day=day, part="b")
