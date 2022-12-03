#!/usr/bin/env python3
from enum import Enum


class Choice(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


choices: dict[int, Choice] = {
    c.value: c for c in Choice.__members__.values()
}


class Outcome(Enum):
    DRAW = 0
    FIRST = 1
    SECOND = 2


outcomes: dict[int, Outcome] = {
    v.value: v for v in Outcome.__members__.values()
}


points_by_outcome: dict[Outcome, int] = {
    Outcome.SECOND: 0,
    Outcome.DRAW: 3,
    Outcome.FIRST: 6,
}


def part_one() -> int:
    def earned_points(me: Choice, opponent: Choice) -> int:
        def outcome(first: Choice, second: Choice) -> Outcome:
            return outcomes[(first.value - second.value) % 3]

        return me.value + points_by_outcome[outcome(me, opponent)]

    letter_map: dict[str, Choice] = {
        "A": Choice.ROCK,
        "X": Choice.ROCK,
        "B": Choice.PAPER,
        "Y": Choice.PAPER,
        "C": Choice.SCISSORS,
        "Z": Choice.SCISSORS,
    }

    total_score = 0
    with open("input.txt", "r") as input_file:
        for match in input_file:
            opponent, me = [letter_map[c.strip()]
                            for c in match.split(maxsplit=2)]
            total_score += earned_points(me, opponent)

    return total_score


def part_two() -> int:
    def earned_points(opponent: Choice, outcome: Outcome) -> int:
        def choice_by_outcome(opponent: Choice, outcome: Outcome) -> Choice:
            return choices[(opponent.value + outcome.value - 1) % 3 + 1]

        return choice_by_outcome(opponent, outcome).value \
            + points_by_outcome[outcome]

    letter_map: dict[str, Choice | Outcome] = {
        "A": Choice.ROCK,
        "B": Choice.PAPER,
        "C": Choice.SCISSORS,
        "X": Outcome.SECOND,
        "Y": Outcome.DRAW,
        "Z": Outcome.FIRST,
    }

    total_score = 0
    with open("input.txt", "r") as input_file:
        for match in input_file:
            opponent, outcome = [letter_map[m.strip()]
                                 for m in match.split(maxsplit=2)]
            total_score += earned_points(opponent, outcome)

    return total_score


def main():
    print(part_one())
    print(part_two())


if __name__ == "__main__":
    main()
