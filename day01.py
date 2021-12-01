#! /usr/bin/env python3
### vendor imports
import more_itertools

### local imports
import utils


def countIncreasingNumbers(numbers: list[int]) -> int:
    """Method to count the number of times a number, in a list, increases over the previous entry."""
    count: int = 0
    for i, n in enumerate(numbers[1:]):
        if n > numbers[i]:
            count += 1
    return count


@utils.part1
def part1(puzzleInput: str):
    numbers = [int(line) for line in puzzleInput.strip().splitlines()]
    # Just count the increasing numbers in the series
    count = countIncreasingNumbers(numbers)
    utils.printAnswer(1, str(count))
    return numbers


@utils.part2
def part2(_, numbers: list[int]):
    # Create a list of sums of numbers in a moving 3-number window
    movingSums = [
        sum(window) for window in more_itertools.windowed(numbers, n=3)
    ]
    count = countIncreasingNumbers(movingSums)
    utils.printAnswer(2, str(count))


utils.start()
