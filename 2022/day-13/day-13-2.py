from functools import cmp_to_key
from typing import TypeAlias

PacketData: TypeAlias = int | list[int]
Packet: TypeAlias = list[PacketData]

with open(0) as file:
    packets: list[Packet] = [eval(l.strip())
                             for l in file.readlines()
                             if l.strip()]


def ordered(left: Packet, right: Packet) -> bool:
    def compare(left: PacketData, right: PacketData) -> bool | None:
        if type(left) is int and type(right) is int:
            if left == right:
                return None
            return left < right
        if type(left) is list and type(right) is list:
            for l, r in zip(left, right):
                result = compare(l, r)
                if result is None:
                    continue
                return result
            if len(left) == len(right):
                return None
            return len(left) < len(right)
        if type(left) is list and type(right) is int:
            return compare(left, [right])
        if type(left) is int and type(right) is list:
            return compare([left], right)
        return True

    for l, r in zip(left, right):
        result = compare(l, r)
        if result is None:
            continue
        return result
    return len(left) < len(right)


ordered_packets = sorted(
    packets + [[[2]]] + [[[6]]],
    key=cmp_to_key(lambda x, y: -1 if ordered(x, y) else 1)
)

print((ordered_packets.index([[2]]) + 1) * (ordered_packets.index([[6]]) + 1))
