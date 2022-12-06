from collections import deque


def count_chars_before_marker(sequence: str, marker_length: int) -> int:
    window = deque(sequence[:marker_length], maxlen=marker_length)
    counter = marker_length
    while len(set(window)) < marker_length:
        window.append(sequence[counter])
        counter += 1
    return counter


def part_one(sequence: str) -> int:
    return count_chars_before_marker(sequence, 4)


def part_two(sequence: str) -> int:
    return count_chars_before_marker(sequence, 14)


def main() -> None:
    with open("input.txt", "r") as file:
        sequence = file.readline().strip()
    print(part_one(sequence))
    print(part_two(sequence))


if __name__ == "__main__":
    main()
