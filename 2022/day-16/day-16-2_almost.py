import re
from collections import deque
from functools import cache
from itertools import chain, combinations
from typing import Iterable, NamedTuple


class Valve(NamedTuple):
    id: str
    flow_rate: int
    neighbors: frozenset[str]


pattern = re.compile(
    r"Valve (\w{2}) has flow rate=(\d+); tunnels? leads? to valves? (.+)")

with open("input.txt") as file:
    matches: list[tuple[str, str, str]] = pattern.findall(file.read())

valves: dict[str, Valve] = {
    id: Valve(id, int(rate), frozenset(n.split(", "))) for (id, rate, n) in matches
}

# Floyd-Warshall-like (generalization of Djikstra) approach
# https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm
# The "schoolbook" approach requests computing ALL distances for every pair of nodes.
# Our environment has some constraints though.

# The only valves that are actually useful are only the ones that are not jammed
# and the valve whose ID is "AA" (it's our starting valve).
# The other valves will be needed only to compute the distance between useful valves.
useful_valves = {
    k: v for k, v in valves.items() if v.flow_rate > 0 or v.id == "AA"
}

distance: dict[str, dict[str, int]] = {}

# For each useful valve, compute the distance with the other useful valves
for valve in useful_valves.values():
    distance[valve.id] = {valve.id: 0}

    # "classic" BFS
    frontier: deque[tuple[str, int]] = deque([(valve.id, 0)])
    # we keep track of the already visited valves
    visited: set[str] = set()

    while len(frontier) > 0:
        v, dist = frontier.popleft()
        for neighbor in (valves[n] for n in valves[v].neighbors):
            # if already visited, ignore
            if neighbor.id in visited:
                continue
            # store the distance only if the valve is open
            if neighbor.flow_rate > 0:
                distance[valve.id][neighbor.id] = dist + 1
            frontier.append((neighbor.id, dist + 1))
            visited.add(neighbor.id)

    del distance[valve.id][valve.id]


@cache
def max_total_pressure(valve: Valve, time: int, visited: frozenset[str]) -> int:
    total_pressure = 0

    # for each reachable open valve from current valve
    for id, dist in distance[valve.id].items():
        # subtract the time of reaching the valve + the time of opening it
        residual_time = time - (dist + 1)
        if id in visited or residual_time <= 0:
            continue
        total_pressure = max(
            max_total_pressure(
                valves[id],
                residual_time,
                visited | {id}
            ) + valves[id].flow_rate * residual_time,
            total_pressure,
        )

    return total_pressure


def powerset(iterable: Iterable[str]):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


total_pressure = 0

useful_valves_ids = frozenset(useful_valves.keys())
print(useful_valves_ids)
for subset in powerset(useful_valves_ids):
    subset = frozenset(subset)
    print(subset, useful_valves_ids - subset)
    total_pressure = max(
        total_pressure,
        max_total_pressure(
            valves["AA"],
            26,
            subset,
        ) +
        max_total_pressure(
            valves["AA"],
            26,
            useful_valves_ids - subset,
        )
    )

print(total_pressure)
