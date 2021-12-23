import json
import math
import sys
import q
import itertools
from typing import List, Tuple
from dataclasses import dataclass
from collections import defaultdict


def add_l(s, val):
    if isinstance(s, int):
        return s + val
    return [add_l(s[0], val), s[1]]


def add_r(s, val):
    if isinstance(s, int):
        return s + val
    return [s[0], add_r(s[1], val)]


def explode(s, depth=0):
    # if isinstance(s, int):
    #    return None, s, None
    if depth >= 3:
        if isinstance(s[0], list):
            return s[0][0], [0, add_l(s[1], s[0][1])], None
        if isinstance(s[1], list):
            return None, [add_r(s[0], s[1][0]), 0], s[1][1]
    if isinstance(s[0], list):
        l, val, r = explode(s[0], depth + 1)
        if val:
            if r:
                return l, [val, add_l(s[1], r)], None
            return l, [val, s[1]], None
    if isinstance(s[1], list):
        l, val, r = explode(s[1], depth + 1)
        if val:
            if l:
                return None, [add_r(s[0], l), val], r
            return None, [s[0], val], r
    return None, None, None


def split(s):
    if isinstance(s, int):
        if s > 9:
            return [s // 2, s - (s // 2)]
        return None
    if s0 := split(s[0]):
        return [s0, s[1]]
    if s1 := split(s[1]):
        return [s[0], s1]
    return None


def reduce(s_num):
    while True:
        _, ret, _ = explode(s_num)
        if ret:
            s_num = ret
            continue
        ret = split(s_num)
        if ret is None:
            break
        s_num = ret
    return s_num


def add(s1, s2):
    return [s1, s2]


def magnitude(l):
    if isinstance(l, int):
        return l
    return magnitude(l[0]) * 3 + magnitude(l[1]) * 2


if __name__ == "__main__":
    lines = [l.strip() for l in sys.stdin]

    snail_nums = [json.loads(l) for l in lines]
    s = snail_nums[0]
    for s_a in snail_nums[1:]:
        s = add(s, s_a)
        s = reduce(s)
    ans1 = magnitude(s)
    print("1:", ans1)

    ans2 = 0
    for s1, s2 in itertools.product(snail_nums, snail_nums):
        ans2 = max(magnitude(reduce(add(s1, s2))), ans2)

    print("2:", ans2)
