import io
import typing

import pydantic


class Rotation(pydantic.BaseModel):
    direction: typing.Literal["L", "R"]
    distance: int


def parse_rotations(input: io.TextIOBase) -> list[Rotation]:
    rotations: list[Rotation] = []
    for line in input:
        direction = line[0]
        distance = int(line[1:])
        rotations.append(Rotation(direction=direction, distance=distance))
    return rotations


def apply_rotation(current_value: int, rotation: Rotation) -> int:
    return (
        current_value + ((1 if rotation.direction == "R" else -1) * rotation.distance)
    ) % 100


def count_zeroes(initial_value: int, rotations: list[Rotation]) -> int:
    value = initial_value
    zero_counter = 0
    for rotation in rotations:
        value = apply_rotation(value, rotation)
        if value == 0:
            zero_counter += 1
    return zero_counter


def count_encountered_zeroes(current_value: int, rotation: Rotation) -> int:
    return (
        (current_value if rotation.direction == "R" else ((100 - current_value) % 100))
        + rotation.distance
    ) // 100


def count_total_encountered_zeroes(
    initial_value: int, rotations: list[Rotation]
) -> int:
    value = initial_value
    zero_counter = 0
    for rotation in rotations:
        zero_counter += count_encountered_zeroes(value, rotation)
        value = apply_rotation(value, rotation)
    return zero_counter


def main() -> None:
    with open("input.txt") as file:
        rotations = parse_rotations(file)
    print(count_zeroes(50, rotations))
    print(count_total_encountered_zeroes(50, rotations))


if __name__ == "__main__":
    main()
