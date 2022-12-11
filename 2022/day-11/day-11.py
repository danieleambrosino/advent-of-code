from collections import deque
from copy import deepcopy
from io import TextIOWrapper
from math import prod
from operator import add, mul, pow
from typing import Callable, Iterable, NamedTuple


class Operation(NamedTuple):
    operator: Callable[[int, int], int]
    operand: int


class ThrowingItem(NamedTuple):
    worry_level: int
    monkey_id: int


class Monkey:
    items: deque[int]
    operation: Operation
    test_modulus: int
    target_monkeys_id: dict[bool, int]
    worry_level_reducer: Callable[[int], int]
    inspections_count: int = 0

    def __init__(self) -> None:
        self.items = deque()
        self.target_monkeys_id = {}

    def throw_all_items(self) -> list[ThrowingItem]:
        throwing_items: list[ThrowingItem] = []
        while len(self.items) > 0:
            throwing_items.append(self._throw_next_item())
        return throwing_items

    def _throw_next_item(self) -> ThrowingItem:
        self.inspections_count += 1
        item = self.items.popleft()
        item = self.operation.operator(
            item,
            self.operation.operand
        )
        item = self.worry_level_reducer(item)
        test = item % self.test_modulus == 0
        monkey_id = self.target_monkeys_id[test]
        return ThrowingItem(item, monkey_id)


def build_monkeys(file: TextIOWrapper) -> list[Monkey]:
    def definition_to_monkey(definition: list[str]) -> Monkey:
        monkey = Monkey()
        for line in definition:
            match line.strip().split(": "):

                case "Starting items", items:
                    items = [int(i) for i in items.split(", ")]
                    for item in items:
                        monkey.items.append(item)

                case "Operation", tokens:
                    tokens = tokens.split()[-2:]
                    match tokens:
                        case "*", "old":
                            monkey.operation = Operation(pow, 2)
                        case "*", operand:
                            monkey.operation = Operation(mul, int(operand))
                        case "+", operand:
                            monkey.operation = Operation(add, int(operand))
                        case _: pass

                case "Test", divisible_by:
                    monkey.test_modulus = int(divisible_by.split(" by ")[1])

                case "If true", throw_to:
                    monkey_id = int(throw_to.split(" to monkey ")[1])
                    monkey.target_monkeys_id[True] = monkey_id
                case "If false", throw_to:
                    monkey_id = int(throw_to.split(" to monkey ")[1])
                    monkey.target_monkeys_id[False] = monkey_id

                case _: pass
        return monkey

    definitions = [c.split("\n") for c in file.read().split("\n\n")]
    return [definition_to_monkey(definition) for definition in definitions]


def round(monkeys: list[Monkey]):
    for monkey in monkeys:
        throwing_items = monkey.throw_all_items()
        for item in throwing_items:
            monkeys[item.monkey_id].items.append(item.worry_level)


def top_two_monkeys(monkeys: list[Monkey]) -> tuple[Monkey, Monkey]:
    sorted_monkeys = sorted(
        monkeys,
        key=lambda m: m.inspections_count,
        reverse=True
    )
    return tuple(sorted_monkeys[:2])


def monkey_business(monkeys: Iterable[Monkey]) -> int:
    return prod(m.inspections_count for m in monkeys)


def part_one(monkeys: list[Monkey]) -> int:
    for monkey in monkeys:
        monkey.worry_level_reducer = lambda x: x // 3
    for _ in range(20):
        round(monkeys)
    return monkey_business(top_two_monkeys(monkeys))


def part_two(monkeys: list[Monkey]) -> int:
    modulus = prod(m.test_modulus for m in monkeys)
    for monkey in monkeys:
        monkey.worry_level_reducer = lambda x: x % modulus
    for _ in range(10_000):
        round(monkeys)
    return monkey_business(top_two_monkeys(monkeys))


def main():
    with open("input.txt", "r") as file:
        monkeys = build_monkeys(file)
    print(part_one(deepcopy(monkeys)))
    print(part_two(deepcopy(monkeys)))


if __name__ == "__main__":
    main()
