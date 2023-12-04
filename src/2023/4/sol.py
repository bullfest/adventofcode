#!/usr/bin/env python3
import functools
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
day = 4

if len(sys.argv) > 1:
    filename = sys.argv[1]
    with open(filename) as file:
        lines = [l.strip('\n') for l in file]
else:
    filename = "input"
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

win_cards = []
cards = []

for l in lines:
    w, c = l.split(":")[1].split("|")
    w = w.strip()
    win_cards.append(aoclib.parse_ints(*w.strip().split()))
    cards.append(aoclib.parse_ints(*c.strip().split()))

def score(i):
    n = len(set(win_cards[i]).intersection(cards[i]))
    if n == 0:
        return 0
    return 2**(n-1)

@functools.cache
def n_cards(i):
    n = len(set(win_cards[i]).intersection(cards[i]))
    return 1 + sum(map(n_cards,range(i+1,i+n+1)))


for i in range(len(lines)):
    ans1 += score(i)
    ans2 += n_cards(i)


###########
print("1:", ans1)
print("2:", ans2)

if filename == "input":
    submit = input("submit?")
    if 'y' in submit.lower():
        if ans1 != 0:
            aocd.submit(ans1, year=year, day=day, part="a")
        if ans2 != 0:
            aocd.submit(ans2, year=year, day=day, part="b")
