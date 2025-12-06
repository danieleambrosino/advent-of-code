from main import (
    sum_invalid_ids_in_ranges,
    invalid_ids_in_range,
    invalid_ids_in_range_v2,
    parse_ranges,
)


def test_invalid_ids_in_range() -> None:
    assert list(invalid_ids_in_range(11, 22)) == [11, 22]
    assert list(invalid_ids_in_range(95, 115)) == [99]
    assert list(invalid_ids_in_range(998, 1012)) == [1010]
    assert list(invalid_ids_in_range(1188511880, 1188511890)) == [1188511885]
    assert list(invalid_ids_in_range(222220, 222224)) == [222222]
    assert list(invalid_ids_in_range(1698522, 1698528)) == []
    assert list(invalid_ids_in_range(446443, 446449)) == [446446]
    assert list(invalid_ids_in_range(38593856, 38593862)) == [38593859]


def test_invalid_ids_in_range_v2() -> None:
    assert list(invalid_ids_in_range_v2(11, 22)) == [11, 22]
    assert list(invalid_ids_in_range_v2(95, 115)) == [99, 111]
    assert list(invalid_ids_in_range_v2(998, 1012)) == [999, 1010]
    assert list(invalid_ids_in_range_v2(1188511880, 1188511890)) == [1188511885]
    assert list(invalid_ids_in_range_v2(222220, 222224)) == [222222]
    assert list(invalid_ids_in_range_v2(1698522, 1698528)) == []
    assert list(invalid_ids_in_range_v2(446443, 446449)) == [446446]
    assert list(invalid_ids_in_range_v2(38593856, 38593862)) == [38593859]
    assert list(invalid_ids_in_range_v2(565653, 565659)) == [565656]
    assert list(invalid_ids_in_range_v2(824824821, 824824827)) == [824824824]
    assert list(invalid_ids_in_range_v2(2121212118, 2121212124)) == [2121212121]


def test_v1() -> None:
    with open("test-input.txt") as file:
        ranges = parse_ranges(file)
    assert sum_invalid_ids_in_ranges(invalid_ids_in_range, ranges) == 1227775554


def test_v2() -> None:
    with open("test-input.txt") as file:
        ranges = parse_ranges(file)
    assert sum_invalid_ids_in_ranges(invalid_ids_in_range_v2, ranges) == 4174379265
