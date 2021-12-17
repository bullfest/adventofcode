import sys
import q
from collections import defaultdict


def transpose(m):
    return list(map(list, zip(*m)))


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
    return sections


def get_grid(lines, f=None, sep=None):
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


lines = [l.strip() for l in sys.stdin]


polymer = lines[0]

rules = {}

for l in lines[2:]:
    i, o = l.split(" -> ")
    rules[i] = o

pairs = defaultdict(lambda: 0)
for i in range(len(polymer) - 1):
    pairs[polymer[i] + polymer[i + 1]] += 1

for i in range(40):
    new_pairs = defaultdict(lambda: 0)
    for pair, count in pairs.items():
        ins_c = rules[pair]
        new_pairs[pair[0] + ins_c] += count
        new_pairs[ins_c + pair[1]] += count
    pairs = new_pairs
    print(pairs)


freq = defaultdict(lambda: 0)
for p, count in pairs.items():
    for c in p:
        freq[c] += count

freq_k = list(sorted(freq.values()))

ans1 = freq_k[-1] / 2 - freq_k[0] / 2


ans2 = 0
print("1:", ans1)
print("2:", ans2)
