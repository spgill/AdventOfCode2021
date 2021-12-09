#! /usr/bin/env python3
### local imports
import utils


def simulateFishPopulation(census: dict[int, int], days: int) -> int:
    # Iterate through each day of the simulation and simulate the lifecycle of the fishies
    for _ in range(days):
        spawn = census[0]
        for i in range(8):
            census[i] = census[i + 1]
        census[6] += spawn
        census[8] = spawn

    # Return the size of the population after simulation
    return sum([value for _, value in census.items()])


@utils.part1
def part1(puzzleInput: str):
    # Parse the input into an array of ints
    fishInput = [int(n) for n in puzzleInput.strip().split(",")]

    # Because iterating over an enormous (and exponentially growing) list is SLOW
    # and the unique identity of each fish is not important, we can break this
    # down into a census count and use that for the simulation.
    census: dict[int, int] = {n: fishInput.count(n) for n in range(9)}

    # The answer for Part 1 is the size of the population after 80 days
    utils.printAnswer(simulateFishPopulation(census, 80))

    # Pass the (mutated) census onto the next part where it will be simulated for longer
    return census


@utils.part2
def part2(_, census: dict[int, int]):
    # Part 1 simulated the fish population for 80 days, and for Part 2 we will
    # simulate it for a further 176 days (for a total of 256 days)
    utils.printAnswer(simulateFishPopulation(census, 176))


utils.start()
