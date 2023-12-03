#!/usr/bin/env python3
import sys
import aocd


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


year = 2023
day = 3

if len(sys.argv) > 1:
    filename = sys.argv[1]
    with open(filename) as file:
        lines = [l.strip('\n') for l in file]
else:
    filename = "input"
    lines = aocd.get_data(year=year, day=day).split("\n")

print("len(lines)", len(lines))
ans1 = 0
ans2 = 0
############
# SOLUTION #
############


non_symbols = {".", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"}
max_x = len(lines[0])
max_y = len(lines[0])


def has_symbol_neighbour(i, j):
    for x, y in neighbours(i, j, diagonal=True):
        if lines[x][y] not in non_symbols:
            return True
    return False


def read_number(i, j):
    while j > 0 and lines[i][j - 1].isdigit():
        j -= 1
    d = ""
    d += lines[i][j]
    while j < max_y - 1 and lines[i][j + 1].isdigit():
        j += 1
        d += lines[i][j]
    print(d)
    return int(d)


def prod_neighbour_numbers(i, j):
    numbers = set()
    for x, y in neighbours(i, j, diagonal=True):
        if lines[x][y].isdigit():
            numbers.add(read_number(x, y))
    if len(numbers) == 2:
        ns = list(numbers)
        return ns[0] * ns[1]


curr_number = ""
curr_has_symbol_neigh = False

for i, l in enumerate(lines):
    for j, c in enumerate(l):
        c: str
        if c.isnumeric():
            curr_number += c
            if has_symbol_neighbour(i, j):
                curr_has_symbol_neigh = True
        else:
            if curr_has_symbol_neigh:
                ans1 += int(curr_number)
            curr_number = ""
            curr_has_symbol_neigh = False

for i, l in enumerate(lines):
    for j, c in enumerate(l):
        if c == "*":
            if pr := prod_neighbour_numbers(i, j):
                ans2 += pr

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
