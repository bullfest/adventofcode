import sys
from typing import List, Tuple
from dataclasses import dataclass
from collections import defaultdict

from ortools.sat.python import cp_model


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
class Instr:
    operation: str
    args: List[str]


lines = [l.strip() for l in sys.stdin]
sections = get_sections(lines)
i_lines = sections[0]

instructions = []

for l in i_lines:
    instructions.append(Instr(l.split()[0], l.split()[1:]))

model = cp_model.CpModel()
solver = cp_model.CpSolver()

inp_vars = [model.NewIntVar(1, 9, "i" + str(i)) for i in range(14)]
next_inp = 0
var = defaultdict(list)
var["w"].append(model.NewIntVar(0, 0, "w0"))
var["x"].append(model.NewIntVar(0, 0, "x0"))
var["y"].append(model.NewIntVar(0, 0, "y0"))
var["z"].append(model.NewIntVar(0, 0, "z0"))


def get_val(arg):
    try:
        i = int(arg)
        return i
    except:
        return var[arg][-1]


def new_var(arg):
    versions = var[arg]
    new_var = model.NewIntVar(0, 10**10, arg + str(len(versions)))
    var[arg].append(new_var)
    return new_var


for instr in instructions:
    if instr.operation == "inp":
        v = new_var(instr.args[0])
        model.Add(v == inp_vars[next_inp])
        next_inp += 1
    elif instr.operation == "add":
        # v = x + y
        x = get_val(instr.args[0])
        y = get_val(instr.args[1])
        v = new_var(instr.args[0])
        model.Add(v == x + y)
    elif instr.operation == "mul":
        # v = x * y
        x = get_val(instr.args[0])
        y = get_val(instr.args[1])
        v = new_var(instr.args[0])
        model.AddMultiplicationEquality(v, [x, y])
    elif instr.operation == "div":
        # v = x / y
        x = get_val(instr.args[0])
        y = get_val(instr.args[1])
        v = new_var(instr.args[0])
        model.AddDivisionEquality(v, x, y)
    elif instr.operation == "mod":
        # v = x / y
        x = get_val(instr.args[0])
        y = get_val(instr.args[1])
        v = new_var(instr.args[0])
        model.AddModuloEquality(v, x, y)
    elif instr.operation == "eql":
        # v = x / y
        x = get_val(instr.args[0])
        y = get_val(instr.args[1])
        v = new_var(instr.args[0])
        b = model.NewBoolVar("")
        model.Add(x == y).OnlyEnforceIf(b)
        model.Add(x != y).OnlyEnforceIf(b.Not())
        model.Add(v == 1).OnlyEnforceIf(b)
        model.Add(v == 0).OnlyEnforceIf(b.Not())

model.Add(var["z"][-1] == 0)

model.Maximize(
    cp_model.LinearExpr.ScalProd(inp_vars, list(reversed([10**i for i in range(14)])))
)

solver = cp_model.CpSolver()

status = solver.Solve(model)

if status == cp_model.OPTIMAL:
    s = ""
    for v in inp_vars:
        s += str(solver.Value(v))
    ans1 = s
    print("1:", s)
else:
    print("1:", solver.StatusName(status))


model.Minimize(
    cp_model.LinearExpr.ScalProd(inp_vars, list(reversed([10**i for i in range(14)])))
)

solver = cp_model.CpSolver()

status = solver.Solve(model)

if status == cp_model.OPTIMAL:
    s = ""
    for v in inp_vars:
        s += str(solver.Value(v))
    print("2:", s)
else:
    print("2:", solver.StatusName(status))
