import re
from collections import deque
from dataclasses import dataclass, field
from functools import cache


@dataclass()
class Valve:
    id: str
    flow_rate: int
    tunnels: list["Valve"] = field(default_factory=list)


pattern = re.compile(
    r"Valve (\w{2}) has flow rate=(\d+); tunnels? leads? to valves? (.+)")

with open("example.txt") as file:
    matches: list[tuple[str, str, str]] = pattern.findall(file.read())
lines = [(v, int(f), t.split(", ")) for (v, f, t) in matches]

valves: dict[str, Valve] = {}
for id, rate, tunnels in lines:
    valves[id] = Valve(id, rate)
for id, rate, tunnels in lines:
    valves[id].tunnels = [valves[t] for t in tunnels]

# Floyd-Warshall-like (generalization of Djikstra) approach
# https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm
# The "schoolbook" approach requests computing ALL distances for every pair of nodes.
# Our environment has some constraints though.

distance: dict[str, dict[str, int]] = {}

# For each valve, compute the distance with the other valves
# First of all, we can ignore the jammed valves (with flow rate 0)
# except for "AA" which is our starting point.
for id, valve in filter(lambda x: x[1].flow_rate > 0 or x[0] == "AA", valves.items()):
    distance[id] = {id: 0}

    # "classic" BFS
    frontier: deque[tuple[Valve, int]] = deque([(valve, 0)])
    # we keep track of the valves already visited
    visited: set[str] = set()

    while len(frontier) > 0:
        v, dist = frontier.popleft()
        for neighbor in valves[v.id].tunnels:
            # if already visited, ignore
            if neighbor.id in visited:
                continue
            # store the distance only if the valve is open
            if neighbor.flow_rate > 0:
                distance[id][neighbor.id] = dist + 1
            frontier.append((neighbor, dist + 1))
            visited.add(neighbor.id)

    del distance[id][id]


def max_total_pressure(valve: Valve, time: int, visited: set[str]) -> int:
    total_pressure = 0

    # for each reachable open valve from current valve
    for id, dist in distance[valve.id].items():
        # subtract the time of reaching the valve + the time of opening it
        residual_time = time - (dist + 1)
        if id in visited or residual_time <= 0:
            continue
        total_pressure = max(
            (valve.flow_rate + max_total_pressure(
                valves[id],
                residual_time,
                visited | {id}
            )) * residual_time,
            total_pressure,
        )

    return total_pressure


print(max_total_pressure(valves["AA"], 30, set()))
