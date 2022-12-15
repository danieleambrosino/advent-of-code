from itertools import product
from typing import NamedTuple


class Unit(NamedTuple):
    x: int
    y: int

    @property
    def depth(self) -> int:
        return self.y

    def __add__(self, other: "Unit") -> "Unit":
        return Unit(self.x + other.x, self.y + other.y)


with open(0) as file:
    paths = [[Unit(*map(int, p.split(",")))
              for p in l.strip().split(" -> ")]
             for l in file.readlines()]

occupied_units: set[Unit] = set()
for path in paths:
    for u1, u2 in zip(path[:-1], path[1:]):
        (min_x, max_x), (min_y, max_y) = sorted(
            [u1.x, u2.x]), sorted([u1.y, u2.y])

        for x, y in product(range(min_x, max_x + 1), range(min_y, max_y + 1)):
            occupied_units.add(Unit(x, y))

abyss_depth = max(p.depth for p in occupied_units) + 1

deposited_grains = 0
while True:
    grain = Unit(500, 0)
    while True:
        if grain.depth >= abyss_depth:
            print(deposited_grains)
            exit(0)
        if grain + Unit(0, 1) not in occupied_units:
            grain += Unit(0, 1)
            continue
        if grain + Unit(-1, 1) not in occupied_units:
            grain += Unit(-1, 1)
            continue
        if grain + Unit(1, 1) not in occupied_units:
            grain += Unit(1, 1)
            continue
        occupied_units.add(grain)
        deposited_grains += 1
        break
