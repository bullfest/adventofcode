import sys
from typing import List, Tuple
from dataclasses import dataclass
from collections import defaultdict


def get_sections(lines):
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


@dataclass
class Inp:
    inp: str
    i = 0

    def next(this):
        this.i += 1
        return this.inp[this.i - 1]


@dataclass
class Instr:
    operation: str
    args: List[str]


lines = [l.strip() for l in sys.stdin]
sections = get_sections(lines)
i_lines = sections[0]
inputs = [Inp(l) for l in sections[1]]

instructions = []

for l in i_lines:
    instructions.append(Instr(l.split()[0], l.split()[1:]))


def run(inp):
    state = defaultdict(lambda: 0)
    for instr in instructions:
        if instr.operation == "inp":
            state[instr.args[0]] = int(inp.next())
        elif instr.operation == "add":
            try:
                v = int(instr.args[1])
            except:
                v = state[instr.args[1]]
            state[instr.args[0]] += v
        elif instr.operation == "mul":
            try:
                v = int(instr.args[1])
            except:
                v = state[instr.args[1]]
            state[instr.args[0]] *= v
        elif instr.operation == "div":
            try:
                v = int(instr.args[1])
            except:
                v = state[instr.args[1]]
            state[instr.args[0]] //= v
        elif instr.operation == "mod":
            try:
                v = int(instr.args[1])
            except:
                v = state[instr.args[1]]
            state[instr.args[0]] %= v
        elif instr.operation == "eql":
            try:
                v = int(instr.args[1])
            except:
                v = state[instr.args[1]]
            if state[instr.args[0]] == v:
                state[instr.args[0]] = 1
            else:
                state[instr.args[0]] = 0
    return state


for inp in inputs:
    state = run(inp)
    print(dict(state))
    if state["z"] == 0:
        print(inp.inp, "is a valid model number!\n")
    else:
        print(inp.inp, "is not a valid model number!\n")
