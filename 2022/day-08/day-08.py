import numpy
from numpy.typing import NDArray


def part_one(trees_heights: NDArray[numpy.ubyte]) -> int:
    def normalize_slice(slice: NDArray[numpy.ubyte]) -> NDArray[numpy.ubyte]:
        if len(slice) == 0:
            return numpy.array([-1])
        return slice
    visible_trees = numpy.zeros(trees_heights.shape, dtype=numpy.bool_)

    for i, j in numpy.ndindex(trees_heights.shape):
        current = trees_heights[i, j]

        slices = [
            trees_heights[i, 0:j],  # left
            trees_heights[i, j+1:trees_heights.shape[1]],  # right
            trees_heights[0:i, j],  # top
            trees_heights[i+1:trees_heights.shape[0], j],  # bottom
        ]
        visible = [current > max(normalize_slice(slice)) for slice in slices]

        if any(visible):
            visible_trees[i, j] = True

    return numpy.count_nonzero(visible_trees)


def part_two(trees_heights: NDArray[numpy.uint]) -> int:
    scenic_scores = numpy.ones(trees_heights.shape, dtype=numpy.uint)
    for i, j in numpy.ndindex(trees_heights.shape):
        current = trees_heights[i, j]

        left_slice = numpy.flip(trees_heights[i, 0:j])
        right_slice = trees_heights[i, j+1:trees_heights.shape[1]]
        top_slice = numpy.flip(trees_heights[0:i, j])
        bottom_slice = trees_heights[i+1:trees_heights.shape[0], j]

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
        trees_heights = numpy.array([list(map(int, list(l.strip())))
                                    for l in file.readlines()], dtype=numpy.ubyte)
    print(part_one(trees_heights))
    print(part_two(trees_heights))


if __name__ == "__main__":
    main()
