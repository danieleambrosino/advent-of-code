import main


def test_count_zeroes() -> None:
    with open("test-input.txt") as file:
        rotations = main.parse_rotations(file)
    assert main.count_zeroes(50, rotations) == 3


def test_count_total_encountered_zeroes() -> None:
    with open("test-input.txt") as file:
        rotations = main.parse_rotations(file)
    assert main.count_total_encountered_zeroes(50, rotations) == 6
