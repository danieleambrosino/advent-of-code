import fileinput
from functools import reduce

chunks = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}
opening_chars = [k for k in chunks.keys()]
closing_chars = [v for v in chunks.values()]
points = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


def missing_chars_to_score(missing_chars: list[str]) -> int:
    return reduce(lambda acc, x: 5*acc + points[x], missing_chars, 0)


scores: list[int] = []
with fileinput.input() as file:
    for line in file:
        expected_closing_chars: list[str] = []
        for char in line:
            if char in opening_chars:
                expected_closing_chars.append(chunks[char])
            elif char in closing_chars:
                if char != expected_closing_chars.pop():
                    expected_closing_chars.clear()
                    break
        if len(expected_closing_chars) > 0:
            scores.append(
                missing_chars_to_score(
                    list(reversed(expected_closing_chars))
                )
            )

print(sorted(scores)[len(scores)//2])
