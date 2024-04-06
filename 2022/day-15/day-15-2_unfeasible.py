import re

pattern = re.compile(r"-?\d+")

Position = tuple[int, int]


def manhattan_distance(a: Position, b: Position) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# max_x = max_y = 4_000_000
max_x = max_y = 20
sensor_to_nearest_beacon: dict[Position, Position] = {}
no_beacon: set[Position] = set()

with open("example.txt") as file:
    for line in file:
        sx, sy, bx, by = list(map(int, pattern.findall(line)))
        sensor_to_nearest_beacon[(sx, sy)] = (bx, by)

for s, b in sensor_to_nearest_beacon.items():
    d = manhattan_distance(s, b)

    for i in range(1, d + 1):
        for j in range(i):
            no_beacon.add((s[0] + i, s[1] + j))
            no_beacon.add((s[0] + j, s[1] + i))
            no_beacon.add((s[0] - i, s[1] + j))
            no_beacon.add((s[0] - j, s[1] + i))


for b in set(sensor_to_nearest_beacon.values()):
    try:
        no_beacon.remove(b)
    except KeyError:
        pass

print(no_beacon)
