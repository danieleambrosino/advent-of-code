from collections import defaultdict
from io import TextIOWrapper
from typing import NamedTuple


def parse_stacks(file: TextIOWrapper) -> dict[int, list[str]]:
    stacks: dict[int, list[str]] = defaultdict(list)
    for line in file:
        if "[" not in line:
            break
        for i in range(1, len(line), 4):
            if line[i] != " ":
                stacks[(i//4)+1].append(line[i])
    for i, stack in stacks.items():
        stacks[i] = list(reversed(stack))
    return stacks


class Instruction(NamedTuple):
    amount: int
    src_stack: int
    dst_stack: int


def parse_instructions(file: TextIOWrapper) -> list[Instruction]:
    import re
    regex = re.compile(r"move (\d+) from (\d+) to (\d+)")

    instructions: list[Instruction] = []
    for line in file:
        chunks = re.match(regex, line.strip())
        if not chunks:
            break
        amount, src_stack, dst_stack = map(int, chunks.groups())
        instructions.append(Instruction(amount, src_stack, dst_stack))

    return instructions


def part_one(file: TextIOWrapper) -> str:
    stacks = parse_stacks(file)
    file.readline()  # skip empty line
    instructions = parse_instructions(file)

    for instruction in instructions:
        crates_to_move = (stacks[instruction.src_stack].pop()
                          for _ in range(instruction.amount))
        for crate in crates_to_move:
            stacks[instruction.dst_stack].append(crate)

    return "".join(stack[-1] for _, stack in sorted(stacks.items()))


def part_two(file: TextIOWrapper) -> str:
    stacks = parse_stacks(file)
    file.readline()  # skip empty line
    instructions = parse_instructions(file)

    for instruction in instructions:
        crates_to_move = [stacks[instruction.src_stack].pop()
                          for _ in range(instruction.amount)]
        for crate in reversed(crates_to_move):
            stacks[instruction.dst_stack].append(crate)

    return "".join(stack[-1] for _, stack in sorted(stacks.items()))


def main() -> None:
    with open("input.txt", "r") as file:
        print(part_one(file))
        file.seek(0)
        print(part_two(file))


if __name__ == "__main__":
    main()
