import json
import itertools
import copy
import math
import sys
import q
from typing import List, Tuple
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class Elem:
    value: int
    depth: int


def parse(l):
    num = []

    def rec_parse(l, depth):
        if isinstance(l[0], int):
            num.append(Elem(l[0], depth))
        else:
            rec_parse(l[0], depth + 1)
        if isinstance(l[1], int):
            num.append(Elem(l[1], depth))
        else:
            rec_parse(l[1], depth + 1)

    rec_parse(l, 1)
    return num


def add(l1, l2):
    l1 = copy.deepcopy(l1)
    l2 = copy.deepcopy(l2)
    l1 += l2
    for e in l1:
        e.depth += 1
    return l1


def test_add():
    assert add(parse([1, 2]), parse([3, 4])) == parse([[1, 2], [3, 4]])


def explode(l):
    for i in range(len(l) - 1):
        if l[i].depth > 4 and l[i].depth == l[i + 1].depth:
            if i > 0:
                l[i - 1].value += l[i].value
            if i + 2 < len(l):
                l[i + 2].value += l[i + 1].value
            del l[i + 1]
            l[i].value = 0
            l[i].depth -= 1
            return l
    return False


def test_explode():
    assert explode(parse([[[[[9, 8], 1], 2], 3], 4])) == parse([[[[0, 9], 2], 3], 4])
    assert not explode(parse([[[[0, 9], 2], 3], 4]))
    assert explode(parse([7, [6, [5, [4, [3, 2]]]]])) == parse([7, [6, [5, [7, 0]]]])


def split(l):
    for i in range(len(l)):
        if l[i].value >= 10:
            e1 = Elem(l[i].value // 2, l[i].depth + 1)
            e2 = Elem(l[i].value - l[i].value // 2, l[i].depth + 1)
            l[i] = e1
            l.insert(i + 1, e2)
            return l
    return False


def reduce(l):
    while True:
        if explode(l):
            continue
        if not split(l):
            break
    return l


def reconstruct(l):
    stack = []
    i = 0
    for e in l:
        while len(stack) < e.depth:
            stack.append([])
        while len(stack) > e.depth:
            last = stack.pop()
            stack[-1].append(last)
        stack[-1].append(e.value)

        while len(stack[-1]) == 2 and len(stack) != 1:
            last = stack.pop()
            stack[-1].append(last)
    return stack[-1]


def magnitude(l):
    if isinstance(l, int):
        return l
    return magnitude(l[0]) * 3 + magnitude(l[1]) * 2


if __name__ == "__main__":
    lines = [l.strip() for l in sys.stdin]

    snail_nums = [parse(json.loads(l)) for l in lines]
    s = snail_nums[0]
    for s_a in snail_nums[1:]:
        s = add(s, s_a)
        s = reduce(s)
    ans1 = magnitude(reconstruct(s))
    print("1:", ans1)

    ans2 = 0
    for s1, s2 in itertools.product(snail_nums, snail_nums):
        s = add(s1, s2)
        s = reduce(s)
        ans2 = max(ans2, magnitude(reconstruct(s)))

    print("2:", ans2)
