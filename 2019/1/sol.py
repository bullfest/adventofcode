import sys

def calc_fuel(w):
    fuels = []
    while w > 0:
        w = w//3 - 2
        fuels.append(w)
    fuels.append(-w)
    return sum(fuels)

def test_calc():
    assert calc_fuel(100756) == 50346


if __name__ == "__main__":
    lines = [l.strip() for l in sys.stdin]
    w = list(map(int, lines))

    ans1 = sum(map(lambda n: n//3-2, w))
    ans2 = sum(map(calc_fuel, w))

    print("1:", ans1)
    print("2:", ans2)
