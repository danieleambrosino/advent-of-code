from copy import copy
from enum import Enum
from typing import NamedTuple

from numpy import array, ceil, int_, sign
from numpy.typing import NDArray


class Direction(Enum):
    DOWN = "D"
    RIGHT = "R"
    UP = "U"
    LEFT = "L"


char_to_direction: dict[str, Direction] = {
    v.value: v for v in Direction.__members__.values()
}

direction_to_array: dict[Direction, NDArray[int_]] = {
    Direction.DOWN: array([1, 0]),
    Direction.RIGHT: array([0, 1]),
    Direction.UP: array([-1, 0]),
    Direction.LEFT: array([0, -1]),
}


class Move(NamedTuple):
    direction: Direction
    amount: int

    @staticmethod
    def build(tokens: list[str]) -> "Move":
        return Move(char_to_direction[tokens[0]], int(tokens[1]))


def part_one(moves: list[Move]) -> int:
    head = array([0, 0])
    tail = array([0, 0])

    tail_positions: set[tuple[int, int]] = set()

    tail_positions.add(tuple(tail))
    for move in moves:
        for _ in range(move.amount):
            head += direction_to_array[move.direction]
            diff = head - tail
            if any(abs(diff) > 1):
                correction = (ceil(abs(diff/2)) * sign(diff/2)).astype(int_)
                tail += correction
            tail_positions.add(tuple(tail))

    return len(tail_positions)


def part_two(moves: list[Move]) -> int:
    head = array([0, 0])
    knots = [copy(head) for _ in range(10)]

    tail_positions: set[tuple[int, int]] = set()

    for move in moves:
        for _ in range(move.amount):
            knots[0] += direction_to_array[move.direction]

            for i, knot in enumerate(knots):
                if i == 0:
                    continue
                diff = knots[i - 1] - knot
                if any(abs(diff) > 1):
                    correction = (ceil(abs(diff/2)) *
                                  sign(diff/2)).astype(int_)
                    knot += correction
                if i == 9:
                    tail_positions.add(tuple(knot))

    return len(tail_positions)


def main():
    with open("input.txt", "r") as file:
        moves = list(map(Move.build, (l.strip().split()
                     for l in file.readlines())))
    print(part_one(moves))
    print(part_two(moves))


if __name__ == "__main__":
    main()
