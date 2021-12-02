#! /usr/bin/env python3
### local imports
import utils


@utils.part1
def part1(puzzleInput: str):
    # Parse the list of instructions in tuple pairs of a string and int
    instructions: list[tuple[str, int]] = [
        (line.split(" ")[0], int(line.split(" ")[1]))
        for line in puzzleInput.strip().splitlines()
    ]

    distance: int = 0
    depth: int = 0

    for direction, magnitude in instructions:
        if direction == "forward":
            distance += magnitude
        elif direction == "down":
            depth += magnitude
        elif direction == "up":
            depth -= magnitude

    utils.printAnswer(distance * depth)

    # Pass parsed instructions to part 2
    return instructions


@utils.part2
def part2(_, instructions: list[tuple[str, int]]):
    distance: int = 0
    depth: int = 0
    aim: int = 0

    for direction, magnitude in instructions:
        if direction == "forward":
            distance += magnitude
            depth += aim * magnitude
        elif direction == "down":
            aim += magnitude
        elif direction == "up":
            aim -= magnitude

    utils.printAnswer(distance * depth)


utils.start()
