from collections import defaultdict
from typing import NamedTuple


def parse_stacks() -> dict[int, list[str]]:
    stacks: dict[int, list[str]] = defaultdict(list)
    with open("input.txt", "r") as file:
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


def parse_instructions() -> list[Instruction]:
    import re
    regex = re.compile(r"move (\d+) from (\d+) to (\d+)")

    instructions: list[Instruction] = []
    with open("input.txt", "r") as file:
        # skip the stacks
        while file.readline() != "\n":
            continue
        for line in file:
            chunks = re.match(regex, line.strip())
            if not chunks:
                break
            amount, src_stack, dst_stack = map(int, chunks.groups())
            instructions.append(Instruction(amount, src_stack, dst_stack))

    return instructions


def part_one() -> str:
    stacks = parse_stacks()
    instructions = parse_instructions()

    for instruction in instructions:
        crates_to_move = (stacks[instruction.src_stack].pop()
                          for _ in range(instruction.amount))
        for crate in crates_to_move:
            stacks[instruction.dst_stack].append(crate)

    return "".join(stack[-1] for _, stack in sorted(stacks.items()))


def part_two() -> str:
    stacks = parse_stacks()
    instructions = parse_instructions()

    for instruction in instructions:
        crates_to_move = [stacks[instruction.src_stack].pop()
                          for _ in range(instruction.amount)]
        for crate in reversed(crates_to_move):
            stacks[instruction.dst_stack].append(crate)

    return "".join(stack[-1] for _, stack in sorted(stacks.items()))


def main() -> None:
    print(part_one())
    print(part_two())


if __name__ == "__main__":
    main()
