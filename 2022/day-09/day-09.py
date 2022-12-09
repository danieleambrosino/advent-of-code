from copy import copy

from numpy import array, ceil, int_, sign

directions = {
    "D": array([1, 0]),
    "R": array([0, 1]),
    "U": array([-1, 0]),
    "L": array([0, -1]),
}


def part_one(moves) -> int:
    head = array([0, 0])
    tail = array([0, 0])

    tail_positions: set[tuple[int, int]] = set()

    tail_positions.add(tuple(tail))
    for move in moves:
        direction, amount = move[0], int(move[1])
        for _ in range(amount):
            head += directions[direction]
            diff = head - tail
            if any(abs(diff) > 1):
                correction = (ceil(abs(diff/2)) * sign(diff/2)).astype(int_)
                tail += correction
            tail_positions.add(tuple(tail))

    return len(tail_positions)


def part_two(moves) -> int:
    head = array([0, 0])
    knots = [copy(head) for _ in range(10)]

    tail_positions: set[tuple[int, int]] = set()

    for move in moves:
        direction, amount = move[0], int(move[1])
        for _ in range(amount):
            knots[0] += directions[direction]

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
        moves = [l.strip().split() for l in file.readlines()]
    print(part_one(moves))
    print(part_two(moves))


if __name__ == "__main__":
    main()
