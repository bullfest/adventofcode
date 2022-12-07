import sys
import q
import itertools as it
import math
import copy
from typing import List, Tuple
from dataclasses import dataclass
from collections import defaultdict


def run_program(prog):
    prog = copy.deepcopy(prog)
    i = 0
    while i < len(prog):
        v = prog[i]
        match v:
            case 1:
                v1 = prog[prog[i+1]]
                v2 = prog[prog[i+2]]
                prog[prog[i+3]] = v1 + v2
                i += 4
            case 2:
                v1 = prog[prog[i+1]]
                v2 = prog[prog[i+2]]
                prog[prog[i+3]] = v1 * v2
                i += 4
            case 3:
                prog[prog[i+1]] = int(input())

            case 99:
                break
    return prog

def test_run():
    assert run_program([]) == []
    assert run_program([1,9,10,3,2,3,11,0,99,30,40,50]) == [3500,9,10,70,2,3,11,0,99,30,40,50]
    assert run_program([1,0,0,0,99]) == [2,0,0,0,99]
    assert run_program([2,3,0,3,99]) == [2,3,0,6,99]
    assert run_program([2,4,4,5,99,0]) == [2,4,4,5,99,9801]
    assert run_program([1,1,1,4,99,5,6,0,99]) == [30,1,1,4,2,5,6,0,99]

if __name__ == "__main__":
    lines = [l.strip() for l in sys.stdin]
    prog = list(map(int, lines[0].split(",")))
    prog[1] = 12
    prog[2] = 2
    ans1 = run_program(prog)[0]
    for n in range(100):
        for v in range(100):
            prog[1] = n
            prog[2] = v
            res = run_program(prog)[0]
            if res == 19690720:
                ans2 = n*100 + v
                break
        else:
            continue
        break

    print("1:", ans1)
    print("2:", ans2)
