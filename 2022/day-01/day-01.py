#!/usr/bin/env python3
def part_one() -> int:
    best_elf_calories = current_elf_calories = 0

    with open("input.txt", "r") as input_file:
        for item_calories in input_file:
            if item_calories != "\n":
                current_elf_calories += int(item_calories)
                continue
            if current_elf_calories > best_elf_calories:
                best_elf_calories = current_elf_calories
            current_elf_calories = 0

    return best_elf_calories


def part_two() -> int:
    best_elves_calories = [0] * 3
    threshold = current_elf_calories = 0

    with open("input.txt", "r") as input_file:
        for item_calories in input_file:
            if item_calories != "\n":
                current_elf_calories += int(item_calories)
                continue
            if current_elf_calories > threshold:
                best_elves_calories[best_elves_calories.index(
                    threshold)] = current_elf_calories
                threshold = min(best_elves_calories)
            current_elf_calories = 0

    return sum(best_elves_calories)


def main() -> None:
    print(part_one())
    print(part_two())


if __name__ == "__main__":
    main()
