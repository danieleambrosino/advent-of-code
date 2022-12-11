from collections import deque
from math import prod
from operator import add, mul, pow
from typing import Any, Callable


class Monkey:
    items: deque[int]
    operation: tuple[Callable[[Any, Any], Any], int]
    test_modulus: int
    target_monkeys_id: dict[bool, int]
    inspections_count: int = 0

    def __init__(self) -> None:
        self.target_monkeys_id = dict()

    def inspect_item(self) -> None:
        worry_level = self.items.popleft()
        worry_level: int = self.operation[0](worry_level, self.operation[1])
        worry_level //= 3
        test = worry_level % self.test_modulus == 0
        target_monkey_id = self.target_monkeys_id[test]
        monkeys[target_monkey_id].items.append(worry_level)
        self.inspections_count += 1

    def turn(self) -> None:
        while len(self.items) > 0:
            self.inspect_item()


monkeys: dict[int, Monkey] = {}

with open("input.txt", "r") as file:
    current_id = 0
    for line in file:
        match line.strip().split():
            case "Monkey", id:
                current_id = id = int(id[:-1])
                monkey = Monkey()
                monkeys[id] = monkey
            case "Starting", "items:", *items:
                items = [int(i) for i in "".join(items).split(",")]
                monkeys[current_id].items = deque(items)
            case "Operation:", *operands:
                match operands[-2:]:
                    case "*", "old":
                        monkeys[current_id].operation = pow, 2
                    case "*", value:
                        monkeys[current_id].operation = mul, int(value)
                    case "+", value:
                        monkeys[current_id].operation = add, int(value)
                    case _: pass
            case "Test:", "divisible", "by", value:
                monkeys[current_id].test_modulus = int(value)
            case "If", test, "throw", "to", "monkey", id:
                test = True if test[:-1] == "true" else False
                monkeys[current_id].target_monkeys_id[test] = int(id)
            case _: pass

for i in range(20):
    for id, monkey in sorted(monkeys.items()):
        monkey.turn()


print(prod(
    [m.inspections_count
     for _, m in sorted(
         monkeys.items(),
         key=lambda x: x[1].inspections_count, reverse=True
     )[:2]]
))
