from main import joltage, joltage_v2, total_joltage, total_joltage_v2


def test_joltage() -> None:
    assert joltage("987654321111111") == 98
    assert joltage("811111111111119") == 89
    assert joltage("234234234234278") == 78
    assert joltage("818181911112111") == 92


def test_joltage_v2() -> None:
    assert joltage_v2("987654321111111", 12) == 987654321111
    assert joltage_v2("811111111111119", 12) == 811111111119
    assert joltage_v2("234234234234278", 12) == 434234234278
    assert joltage_v2("818181911112111", 12) == 888911112111


def test_total_joltage() -> None:
    assert (
        total_joltage(
            [
                "987654321111111",
                "811111111111119",
                "234234234234278",
                "818181911112111",
            ]
        )
        == 357
    )


def test_total_joltage_v2() -> None:
    assert (
        total_joltage_v2(
            [
                "987654321111111",
                "811111111111119",
                "234234234234278",
                "818181911112111",
            ]
        )
        == 3121910778619
    )
