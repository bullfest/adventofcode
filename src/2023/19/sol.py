#!/usr/bin/env python3
import dataclasses
import sys
import re
from copy import deepcopy

import aoclib
from aoclib import *
import q
import itertools as it
import math
import aocd
from typing import List, Tuple, Dict
from dataclasses import dataclass
from collections import defaultdict


def set_min_x(n: int):
    global min_x
    min_x = aoclib.min_x = n


def set_min_y(n: int):
    global min_y
    min_y = aoclib.min_y = n


def set_max_x(n: int):
    global max_x
    max_x = aoclib.max_x = n


def set_max_y(n: int):
    global max_y
    max_y = aoclib.max_y = n


def flip_x_y():
    global max_x, max_y
    max_x, max_y = max_y, max_x
    aoclib.max_x = max_x
    aoclib.max_y = max_y


year = 2023
day = 19


@dataclasses.dataclass
class Rule:
    field: str
    condition: str
    val: int
    result: str

    def passes(self, item):
        field = item[self.field]
        match self.condition:
            case "<":
                return field < self.val
            case ">":
                return field > self.val
        raise NotImplementedError()

    def constrain(self, item):
        item = deepcopy(item)
        min_v, max_v = item[self.field]
        match self.condition:
            case "<":
                max_v = min(max_v, self.val - 1)
            case ">":
                min_v = max(min_v, self.val + 1)
        item[self.field] = (min_v, max_v)
        return item

    def reverse_constrain(self, item):
        item = deepcopy(item)
        min_v, max_v = item[self.field]
        match self.condition:
            case "<":
                min_v = max(min_v, self.val)
            case ">":
                max_v = min(max_v, self.val)
        item[self.field] = (min_v, max_v)
        return item


@dataclasses.dataclass
class Workflow:
    name: str
    rules: List[Rule]
    default: str

    def get_next(self, item):
        for r in self.rules:
            if r.passes(item):
                return r.result
        return self.default


def prod_sum(item):
    combs = 1
    for f, vs in item.items():
        min_v, max_v = vs
        combs *= max((max_v - min_v + 1), 0)
    return combs


def acceptances(item, wf_name: str, workflows: Dict[str, Workflow]):
    if prod_sum(item) == 0:
        return 0
    if wf_name == "A":
        return prod_sum(item)
    if wf_name == "R":
        return 0
    ans = 0
    wf = workflows[wf_name]

    for r in wf.rules:
        new_item = r.constrain(item)
        if prod_sum(new_item) > 0:
            ans += acceptances(new_item, r.result, workflows)
        item = r.reverse_constrain(item)

    if prod_sum(item) > 0:
        ans += acceptances(item, wf.default, workflows)

    return ans


def accepted(item, workflows):
    wf_name = "in"
    while wf_name not in "AR":
        wf = workflows[wf_name]
        wf_name = wf.get_next(item)

    return wf_name == "A"


def run():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        with open(filename) as file:
            lines = [l.strip('\n') for l in file]
    else:
        filename = None
        lines = aocd.get_data(year=year, day=day).split("\n")

    print("len(lines)", len(lines))
    print("len(lines[0])", len(lines[0]))

    ans1 = 0

    set_max_x(len(lines))
    set_max_y(len(lines[0]))

    ############
    # SOLUTION #
    ############
    sections = get_sections(lines)

    workflows = {}
    for l in sections[0]:
        name, conds = l.strip("}").split("{")
        rules = []
        for r in conds.split(",")[:-1]:
            cond, result = r.split(":")
            field = cond[0]
            c = cond[1]
            val = int(cond[2:])
            rules.append(Rule(field, c, val, result))
        default = conds.split(",")[-1]
        workflows[name] = Workflow(name, rules, default)

    for l in sections[1]:
        item = {}
        for i in l.strip("{}").split(","):
            n, v = i.split("=")
            item[n] = int(v)
        if accepted(item, workflows):
            ans1 += sum(item.values())

    item = {f: (1, 4000) for f in "xmas"}
    ans2 = acceptances(item, "in", workflows)

    ###########
    print("1:", ans1)
    print("2:", ans2)

    if filename is None:
        submit = input("submit?")
        if 'y' in submit.lower():
            if ans1 != 0:
                aocd.submit(ans1, year=year, day=day, part="a")
            if ans2 != 0:
                aocd.submit(ans2, year=year, day=day, part="b")


if __name__ == "__main__":
    run()
