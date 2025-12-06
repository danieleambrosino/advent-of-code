from collections.abc import Callable, Iterable
import io
import re

import pydantic


def parse_ranges(input: io.TextIOBase) -> list[tuple[int, int]]:
    return pydantic.TypeAdapter(list[tuple[int, int]]).validate_python(
        [r.split("-") for r in input.read().split(",")]
    )


def invalid_ids_in_range(lower: int, upper: int) -> Iterable[int]:
    for n in range(lower, upper + 1):
        if re.fullmatch(r"(\d+)\1", str(n)):
            yield n


def invalid_ids_in_range_v2(lower: int, upper: int) -> Iterable[int]:
    for n in range(lower, upper + 1):
        if re.fullmatch(r"(\d+)\1+", str(n)):
            yield n


def sum_invalid_ids_in_ranges(
    detector: Callable[[int, int], Iterable[int]],
    ranges: Iterable[tuple[int, int]],
) -> int:
    return sum(i for lower, upper in ranges for i in detector(lower, upper))


def main() -> None:
    with open("input.txt") as file:
        ranges = parse_ranges(file)
    print(sum_invalid_ids_in_ranges(invalid_ids_in_range, ranges))
    print(sum_invalid_ids_in_ranges(invalid_ids_in_range_v2, ranges))


if __name__ == "__main__":
    main()
