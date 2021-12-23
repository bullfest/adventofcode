import sys
from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class Packet:
    version: int = 0
    p_type: int = 0
    val: int = 0
    data = []
    sub_packets: Tuple["Packet", ...] = None


lines = [l.strip() for l in sys.stdin]
assert len(lines) == 1
binary = []

hex_to_bin = {c: list(map(int, bin(int("1" + c, 16))[3:])) for c in "0123456789ABCDEF"}

for c in lines[0]:
    binary += hex_to_bin[c]


def decode(b):
    s = "".join(map(str, b))
    return int(s, 2)


def decode_packet(b, i):
    packet = Packet()
    packet.version = decode(b[i : i + 3])
    i += 3
    packet.p_type = decode(b[i : i + 3])
    i += 3
    if packet.p_type == 4:
        num = []
        while b[i] == 1:
            num += b[i + 1 : i + 5]
            i += 5
        # The last word
        num += b[i + 1 : i + 5]
        i += 5
        packet.val = decode(num)
        packet.data = num
    else:
        # Operator
        bits = -1
        packets = -1
        if b[i] == 0:
            length = decode(b[i + 1 : i + 16])
            i += 16
            init_i = i
            packets = []
            while i - init_i < length:
                sub_p, i = decode_packet(b, i)
                packets.append(sub_p)
        else:
            n_packets = decode(b[i + 1 : i + 12])
            i += 12
            packets = []
            for _ in range(n_packets):
                sub_p, i = decode_packet(b, i)
                packets.append(sub_p)
        packet.sub_packets = packets
    return packet, i


packets = []
i = 0
packet = Packet()
while i < len(binary):
    packet, i = decode_packet(binary, i)
    packets.append(packet)
    if all(map(lambda n: n == 0, binary[i:])):
        break


def sum_versions(ps):
    s = 0
    for p in ps:
        s += p.version
        if p.sub_packets:
            s += sum_versions(p.sub_packets)
    return s


ans1 = sum_versions(packets)
print("1:", ans1)


def eval(packet):
    if packet.p_type == 0:  # sum
        s = 0
        for p in packet.sub_packets:
            s += eval(p)
        return s
    elif packet.p_type == 1:  # product
        s = 1
        for p in packet.sub_packets:
            s *= eval(p)
        return s
    elif packet.p_type == 2:  # min
        s = eval(packet.sub_packets[0])
        for p in packet.sub_packets[1:]:
            s = min(eval(p), s)
        return s
    elif packet.p_type == 3:  # max
        s = eval(packet.sub_packets[0])
        for p in packet.sub_packets[1:]:
            s = max(eval(p), s)
        return s
    elif packet.p_type == 4:  # const
        return packet.val
    elif packet.p_type == 5:  # gt
        p1_val = eval(packet.sub_packets[0])
        p2_val = eval(packet.sub_packets[1])
        if p1_val > p2_val:
            return 1
        return 0
    elif packet.p_type == 6:  # lt
        p1_val = eval(packet.sub_packets[0])
        p2_val = eval(packet.sub_packets[1])
        if p1_val < p2_val:
            return 1
        return 0
    elif packet.p_type == 7:  # product
        p1_val = eval(packet.sub_packets[0])
        p2_val = eval(packet.sub_packets[1])
        if p1_val == p2_val:
            return 1
        return 0
    else:
        print("PANIC AT THE DISCO")


ans2 = eval(packets[0])

print("2:", ans2)
