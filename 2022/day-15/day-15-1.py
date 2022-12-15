import re

Position = tuple[int, int]


def manhattan_distance(a: Position, b: Position) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


ROW_Y = 2_000_000

pattern = re.compile(r"-?\d+")
sensor_to_nearest_beacon: dict[Position, Position] = {}

with open(0) as file:
    for line in file:
        sx, sy, bx, by = map(int, pattern.findall(line))
        sensor_to_nearest_beacon[(sx, sy)] = (bx, by)

x_no_beacon: set[int] = set()
for s, b in sensor_to_nearest_beacon.items():
    d = manhattan_distance(s, b)
    sx, sy = s
    if d < abs(sy - ROW_Y):
        continue

    bound = sy + (d if sy < ROW_Y else -d)
    shift = abs(bound - ROW_Y)

    for i in range(shift + 1):
        if (sx - i, ROW_Y) != b:
            x_no_beacon.add(sx - i)
        if (sx + i, ROW_Y) != b:
            x_no_beacon.add(sx + i)

for (bx, by) in set(sensor_to_nearest_beacon.values()):
    if by == ROW_Y:
        try:
            x_no_beacon.remove(bx)
        except KeyError:
            pass

print(len(x_no_beacon))
