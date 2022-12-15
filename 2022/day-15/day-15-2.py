import re

import z3

Position = tuple[int, int]
SATPosition = tuple[z3.ArithRef, z3.ArithRef]


def manhattan_distance(a: Position, b: Position) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def sat_manhattan_distance(a: Position, b: SATPosition) -> z3.ArithRef:
    return z3.Abs(a[0] - b[0]) + z3.Abs(a[1] - b[1])


solver = z3.Solver()
x, y = z3.Ints("x y")

BOUND = 4_000_000
solver.add(z3.And(0 <= x, x <= BOUND))
solver.add(z3.And(0 <= y, y <= BOUND))

pattern = re.compile(r"-?\d+")

with open(0) as file:
    for line in file:
        sx, sy, bx, by = map(int, pattern.findall(line))
        solver.add(manhattan_distance((sx, sy), (bx, by)) <
                   sat_manhattan_distance((sx, sy), (x, y)))
        solver.add(z3.And(x != bx, y != by))

solver.check()
solution = solver.model()

x, y = solution[x].as_long(), solution[y].as_long()

print(x * BOUND + y)
