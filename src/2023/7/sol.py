#!/usr/bin/env python3
import dataclasses
import itertools
import sys
import re

import aoclib
import q
import itertools as it
import math
import aocd
from typing import List, Tuple
from dataclasses import dataclass
from collections import defaultdict


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
day = 7

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
ans2 = 0

set_max_x(len(lines))
set_max_y(len(lines[0]))

############
# SOLUTION #
############
card_order1 = list("AKQJT98765432")
card_order1.reverse()
card_order2 = list("AKQT98765432J")
card_order2.reverse()


@dataclasses.dataclass
class Hand:
    cards: str
    bid: int

    def sort_key1(self):
        counts = []
        for k, g in itertools.groupby(sorted(self.cards)):
            counts.append(len(list(g)))
        counts.sort(reverse=True)

        return counts, [card_order1.index(c) for c in self.cards]

    def sort_key2(self):
        counts = []
        cmj = list(filter(lambda c: c != "J", self.cards))
        jokers = 5 - len(cmj)
        for k, g in itertools.groupby(sorted(cmj)):
            counts.append(len(list(g)))
        counts.sort(reverse=True)
        
        if jokers == 5:
            counts = [5]
        else:
            counts[0] += jokers

        return counts, [card_order2.index(c) for c in self.cards]


hands = []
for l in lines:
    h, b = l.split()
    hands.append(Hand(h, int(b)))

hands.sort(key=lambda k: k.sort_key1())
for i, h in enumerate(hands):
    ans1 += (i + 1) * h.bid

hands.sort(key=lambda k: k.sort_key2())
for i, h in enumerate(hands):
    ans2 += (i + 1) * h.bid
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
