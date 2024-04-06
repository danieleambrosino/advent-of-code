import fileinput

chunks = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}
opening_chars = [k for k in chunks.keys()]
closing_chars = [v for v in chunks.values()]
points = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}
illegal_chars: list[str] = []
with fileinput.input() as file:
    for line in file:
        expected_closing_chars: list[str] = []
        for char in line:
            if char in opening_chars:
                expected_closing_chars.append(chunks[char])
            elif char in closing_chars:
                if char != expected_closing_chars.pop():
                    illegal_chars.append(char)
                    break
print(sum(points[c] for c in illegal_chars))
