#!/usr/bin/env python3
from functools import reduce
from operator import and_


def priority(item: str) -> int:
    assert len(item) == 1
    if item.isupper():
        return ord(item) - ord("A") + 27
    return ord(item) - ord("a") + 1


def part_one() -> int:
    total_priorities = 0
    with open("input.txt", "r") as input_file:
        for rucksack in input_file:
            compartment1, compartment2 = rucksack[:len(
                rucksack)//2], rucksack[len(rucksack)//2:]
            common_items = set(compartment1) & set(compartment2)
            total_priorities += sum(priority(i) for i in common_items)
    return total_priorities


def part_two() -> int:
    total_priorities = 0
    group = []
    with open("input.txt", "r") as input_file:
        for i, rucksack in enumerate(input_file):
            group.append(rucksack.strip())
            if i % 3 != 2:
                continue
            common_item = reduce(and_, map(set, group))
            total_priorities += priority(list(common_item)[0])
            group.clear()
    return total_priorities


def main() -> None:
    print(part_one())
    print(part_two())


if __name__ == "__main__":
    main()
