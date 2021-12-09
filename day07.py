#! /usr/bin/env python3
### local imports
import utils


def burnCost(x: int, y: int) -> int:
    return abs(x - y)


def advancedBurnCost(x: int, y: int) -> int:
    n = burnCost(x, y)
    return (n * (n + 1)) // 2


@utils.part1
def part1(puzzleInput: str):
    # Parse the horizontal position ints from the puzzle input
    positions = [int(n) for n in puzzleInput.strip().split(",")]

    # Iterate through the the various possible alignment points and calculate
    # the total movement cost for each submarine therein
    costs = [
        sum([burnCost(n, target) for n in positions])
        for target in range(min(positions), max(positions) + 1)
    ]

    # The answer is the alignment point with the lowest total cost
    utils.printAnswer(min(costs))

    # Pass the parsed positions to Part 2
    return positions


@utils.part2
def part2(_, positions: list[int]):
    # Similar to Part 1, we will iterate through each alignment option,
    # but this time we will use the more complicated fuel usage algorithm
    costs = [
        sum([advancedBurnCost(n, target) for n in positions])
        for target in range(min(positions), max(positions) + 1)
    ]

    # Once again, the answer is the lowest total cost
    utils.printAnswer(min(costs))


utils.start()
