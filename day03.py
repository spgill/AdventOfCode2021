#! /usr/bin/env python3
### stdlib imports
import collections
import copy

### local imports
import utils


@utils.part1
def part1(puzzleInput: str):
    # Convert the puzzle input to lines, and pivot these lines of bits to columns
    diagnostic = puzzleInput.strip().splitlines()
    diagnosticLength = len(diagnostic[0])
    diagnosticColumns = [
        "".join([line[x] for line in diagnostic])
        for x in range(diagnosticLength)
    ]

    # Run a character frequency analysis on each "column" and add the most/least
    # common character to the respective binary number
    gamma = ""
    epsilon = ""
    for column in diagnosticColumns:
        frequencies = collections.Counter(column).most_common()
        gamma += frequencies[0][0]
        epsilon += frequencies[1][0]

    # Parse these binary numbers and multiply them for the answer
    utils.printAnswer(int(gamma, 2) * int(epsilon, 2))

    # Pass the parsed diagnostics for part 2
    return diagnostic


@utils.part2
def part2(_, diagnostic: list[str]):
    diagnosticLength = len(diagnostic[0])

    # Iterate through each line filtering for the most/least common bit
    # to find each system's rating
    systemRatings = []
    for frequencyTarget in [0, 1]:
        filteredDiagnostics = copy.copy(diagnostic)
        for columnIndex in range(diagnosticLength):
            # Run a frequency analysis on this column to determine the target bit
            frequencies = collections.Counter(
                "".join([line[columnIndex] for line in filteredDiagnostics])
            ).most_common()
            targetBit = frequencies[frequencyTarget][0]

            # Slight wrinkle... If the character freqencies are the same,
            # use the tie breaker value
            if frequencies[0][1] == frequencies[1][1]:
                targetBit = ["1", "0"][frequencyTarget]

            # Filter the current diagnostic lines by this target bit
            filteredDiagnostics = [
                line
                for line in filteredDiagnostics
                if line[columnIndex] == targetBit
            ]

            # If there is only one number remaining, this is the system rating
            if len(filteredDiagnostics) == 1:
                systemRatings.append(filteredDiagnostics[0])
                break

    # Parse these binary system ratings and multiply them for the answer
    utils.printAnswer(int(systemRatings[0], 2) * int(systemRatings[1], 2))


utils.start()
