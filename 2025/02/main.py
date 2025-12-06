import re

input_string = input()
ranges = input_string.split(",")
ranges = (r.split("-") for r in ranges)
invalid_ids: list[int] = []
for lower, upper in ranges:
    for n in range(int(lower), int(upper) + 1):
        if re.fullmatch(r"(\d+)\1", str(n)):
            invalid_ids.append(n)
print(sum(invalid_ids))
