def joltage(bank: str) -> int:
    first_digit = max(bank[:-1])
    second_digit = max(bank[bank.find(first_digit) + 1 :])
    return int(f"{first_digit}{second_digit}")


def joltage_v2(bank: str, length: int) -> int:
    digits: list[str] = []
    lower = 0
    upper = len(bank) - length + 1
    for _ in range(length):
        digit = max(bank[lower:upper])
        digits.append(digit)
        position = bank[lower:upper].find(digit) + lower
        lower = position + 1
        upper += 1
    return int("".join(digits))


def total_joltage(banks: list[str]) -> int:
    return sum(joltage(bank) for bank in banks)

def total_joltage_v2(banks: list[str]) -> int:
    return sum(joltage_v2(bank, 12) for bank in banks)

def main() -> None:
    with open("input.txt") as file:
        banks = [line.strip() for line in file.readlines()]
    print(total_joltage(banks))
    print(total_joltage_v2(banks))


if __name__ == "__main__":
    main()
