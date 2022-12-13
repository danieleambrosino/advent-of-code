from typing import TypeAlias

PacketData: TypeAlias = int | list[int]
Packet: TypeAlias = list[PacketData]

with open(0) as file:
    pairs: list[tuple[Packet, Packet]] = [tuple(map(eval, ls.splitlines()))
                                          for ls in file.read().split("\n\n")]


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


print(sum(i * int(ordered(pair[0], pair[1]))
      for i, pair in enumerate(pairs, start=1)))
