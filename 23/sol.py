import sys
import copy


def transpose(m):
    return list(map(list, zip(*m)))


def print_grid(g):
    for l in transpose(g):
        print("".join(l))
        # print("".join(map(lambda n: "X" if n > 10 else str(n % 10), l)))
    print()


def h(m):
    return hash("".join("".join(l) for l in m))


def path_between(m, p0, p1):
    if p0 == p1:
        return None
    x0, y0 = p0
    x1, y1 = p1
    s = 0
    while y0 != 1:
        s += 1
        y0 -= 1
        if m[x0][y0] != ".":
            return False
    while x0 != x1:
        s += 1
        if x0 < x1:
            x0 += 1
        else:
            x0 -= 1
        if m[x0][y0] != ".":
            return False
    while y0 != y1:
        s += 1
        y0 += 1
        if m[x0][y0] != ".":
            return False
    return s


def solve(m):
    shuffle_pos = ((1, 1), (2, 1), (4, 1), (6, 1), (8, 1), (10, 1), (11, 1))
    costs = {"A": 1, "B": 10, "C": 100, "D": 1000}

    goal_pos = {
        "A": tuple((3, y) for y in reversed(range(2, len(m[0]) - 1))),
        "B": tuple((5, y) for y in reversed(range(2, len(m[0]) - 1))),
        "C": tuple((7, y) for y in reversed(range(2, len(m[0]) - 1))),
        "D": tuple((9, y) for y in reversed(range(2, len(m[0]) - 1))),
    }
    dp = {h(m): 0}
    states = {h(m): m}

    while states:
        hm = next(iter(states))
        m = states.pop(hm)
        c = dp[h(m)]
        for x, y in shuffle_pos:
            if m[x][y] == ".":
                for poddy in goal_pos:
                    for x0, y0 in goal_pos[poddy]:
                        if m[x0][y0] == ".":
                            continue  # Nothing to move
                        if m[x0][y0] == poddy:
                            for y1 in range(y0 + 1, 6):
                                if m[x0][y1] != poddy:
                                    break
                            else:
                                continue  # If no pod below is other type
                        pod = m[x0][y0]
                        if s := path_between(m, (x0, y0), (x, y)):
                            mp = copy.deepcopy(m)
                            mc = s * costs[pod] + c
                            mp[x][y] = pod
                            mp[x0][y0] = "."
                            mh = h(mp)
                            if mh not in dp or mc < dp[mh]:
                                dp[mh] = mc
                                if mh not in states:
                                    states[mh] = mp
            else:
                # Try to move to pos
                pod = m[x][y]
                gp = None
                for xg, yg in goal_pos[pod]:
                    if m[xg][yg] == ".":
                        gp = (xg, yg)
                        break
                    if m[xg][yg] != pod:
                        break
                if gp is None:
                    continue
                if s := path_between(m, (x, y), gp):
                    mp = copy.deepcopy(m)
                    mc = s * costs[pod] + c
                    mp[gp[0]][gp[1]] = pod
                    mp[x][y] = "."
                    mh = h(mp)
                    if mh not in dp or mc < dp[mh]:
                        dp[mh] = mc
                        if mh not in states:
                            states[mh] = mp
    solved = [
        "#############",
        "#...........#",
        "###A#B#C#D###",
    ]
    solved += ["  #A#B#C#D#  "] * (1 if len(m[0]) == 5 else 3)
    solved.append("  #########  ")
    solved = transpose(solved)
    return dp[h(solved)]


lines = [l.strip("\n") for l in sys.stdin]

m1 = transpose(lines)
print_grid(m1)

ans1 = solve(m1)

lines.insert(3, "  #D#C#B#A#  ")
lines.insert(4, "  #D#B#A#C#  ")

m2 = transpose(lines)
print_grid(m2)

ans2 = solve(m2)
print("1:", ans1)
print("2:", ans2)
