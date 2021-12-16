#! /usr/bin/env python3
### stdlib imports
import collections

### vendor imports
import more_itertools

### local imports
import utils


@utils.part1
def part1(puzzleInput: str):
    utils.printComputationWarning()

    # Parse the puzzle input into the polymer template and pair insertion rules as a dict
    inputLines = puzzleInput.strip().splitlines()
    template = inputLines[0]
    rules = {a: b for a, b in [line.split(" -> ") for line in inputLines[2:]]}

    # Start by creating a new counter and seeding it with the template element pairs
    moleculeCounter: collections.Counter[str] = collections.Counter()
    for elements in more_itertools.windowed(template, n=2):
        moleculeCounter["".join(elements)] += 1

    # Once again we're faced with performing transformations against an exponentially
    # growing list; a list whos elements' order and identity do not need to be preserved.
    # So once again, we'll resort to utilizing a "census" of sorts,
    # and performing transformations (in this case, "insertions") against it.
    # We will run this for 40 iterations so we can calculate answers to both
    # parts 1 and 2 in one go.
    samples: list[list[tuple[str, int]]] = []
    for _ in range(40):
        for pair, n in list(moleculeCounter.items()):
            if n > 0 and (atom := rules.get(pair, None)):
                a, b = list(pair)
                moleculeCounter[pair] -= n
                moleculeCounter[a + atom] += n
                moleculeCounter[atom + b] += n

        # Collect a sample of the element frequencies for each iteration
        elementCounter: collections.Counter[str] = collections.Counter()
        for (_, b), n in moleculeCounter.items():
            elementCounter[b] += n
        # Must make sure this first element of the original template is accounted for
        elementCounter[template[0]] += 1
        samples.append(elementCounter.most_common())

    # The answer for Part 1 is derived from the element frequencies after 10 iterations
    utils.printAnswer(samples[9][0][1] - samples[9][-1][1])

    # Pass the sample array onto Part 2
    return samples


@utils.part2
def part2(_, frequencies: list[list[tuple[str, int]]]):
    # The answer for Part 2 has already been found. It is derived from the
    # element frequencies after 40 iterations (e.g., the last iteration)
    utils.printAnswer(frequencies[-1][0][1] - frequencies[-1][-1][1])


utils.start()
