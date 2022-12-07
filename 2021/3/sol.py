import sys

binarys = [l.strip() for l in sys.stdin]
zeroes = [0 for _ in range(len(binarys[0]))]
ones = [0 for _ in range(len(binarys[0]))]

for b in binarys:
    for i in range(len(b)):
        if b[i] == "0":
            zeroes[i] += 1
        else:
            ones[i] += 1

alpha = ""
gamma = ""
for i in range(len(zeroes)):
    if zeroes[i] > ones[i]:
        alpha += "0"
        gamma += "1"
    else:
        alpha += "1"
        gamma += "0"

# print("b", binarys)
# print("alpha", alpha, "gamma", gamma)
print("1:", int(alpha, 2) * int(gamma, 2))


def find_rating(bins, inv=False):
    bins = list(bins)
    for i in range(len(bins[0])):
        z = 0
        o = 0
        for b in bins:
            if b[i] == "0":
                z += 1
            else:
                o += 1
        if z > o:
            filt = "0"
            if inv:
                filt = "1"
        else:
            filt = "1"
            if inv:
                filt = "0"
        bins = list(filter(lambda b: b[i] == filt, bins))
        if len(bins) == 1:
            return bins[0]


oxy = find_rating(binarys)
co2 = find_rating(binarys, True)
print("oxy:", oxy)
print("c02:", co2)
print("2:", int(oxy, 2) * int(co2, 2))
