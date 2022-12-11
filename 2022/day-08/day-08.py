from numpy import (array, bool_, count_nonzero, flip, ndindex, ones, ubyte,
                   uint, zeros)
from numpy.typing import NDArray


def part_one(trees: NDArray[ubyte]) -> int:
    visible_trees = zeros(trees.shape, dtype=bool_)

    for i, j in ndindex(trees.shape):
        current = trees[i, j]

        slices = [
            trees[i, 0:j],  # left
            trees[i, j+1:trees.shape[1]],  # right
            trees[0:i, j],  # top
            trees[i+1:trees.shape[0], j],  # bottom
        ]
        visible = [current > max(slice) if len(slice) > 0 else True
                   for slice in slices]

        if any(visible):
            visible_trees[i, j] = True

    return count_nonzero(visible_trees)


def part_two(trees: NDArray[uint]) -> int:
    scenic_scores = ones(trees.shape, dtype=uint)

    for i, j in ndindex(trees.shape):
        current = trees[i, j]

        left_slice = flip(trees[i, 0:j])
        right_slice = trees[i, j+1:trees.shape[1]]
        top_slice = flip(trees[0:i, j])
        bottom_slice = trees[i+1:trees.shape[0], j]

        for slice in left_slice, right_slice, top_slice, bottom_slice:
            if len(slice) == 0:
                continue
            counter = 0
            for tree in slice:
                counter += 1
                if tree >= current:
                    break
            scenic_scores[i, j] *= counter
    return scenic_scores.max()


def main() -> None:
    with open("input.txt", "r") as file:
        trees = array([list(map(int, list(l.strip())))
                       for l in file.readlines()], dtype=ubyte)
    print(part_one(trees))
    print(part_two(trees))


if __name__ == "__main__":
    main()
