import numpy


def get_accessible_rolls(grid: numpy.ndarray) -> list[tuple[int, int]]:
    rows, cols = grid.shape
    positions: list[tuple[int, int]] = []
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != "@":
                continue
            neighborhood = grid[
                max(0, r - 1) : min(rows, r + 2), max(0, c - 1) : min(cols, c + 2)
            ]
            if len(neighborhood[neighborhood == "@"]) <= 4:
                positions.append((r, c))
    return positions


def count_accessible_rolls(grid: numpy.ndarray) -> int:
    return len(get_accessible_rolls(grid))


def remove_accessible_rolls(
    grid: numpy.ndarray,
    accessible_rolls: list[tuple[int, int]],
) -> None:
    for r, c in accessible_rolls:
        grid[r, c] = "."

def remove_all_accessible_rolls(grid: numpy.ndarray) -> int:
    count = 0
    while True:
        accessible_rolls = get_accessible_rolls(grid)
        if not accessible_rolls:
            break
        count += len(accessible_rolls)
        remove_accessible_rolls(grid, accessible_rolls)
    return count


def main() -> None:
    with open("input.txt") as file:
        grid = numpy.array([list(line) for line in file.read().strip().splitlines()])
    print(count_accessible_rolls(grid))
    print(remove_all_accessible_rolls(grid))


if __name__ == "__main__":
    main()
