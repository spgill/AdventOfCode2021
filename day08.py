#! /usr/bin/env python3
### local imports
import utils

"""
  0:      1:      2:      3:      4:       5:      6:      7:      8:      9:
 aaaa    ....    aaaa    aaaa    ....     aaaa    aaaa    aaaa    aaaa    aaaa
b    c  .    c  .    c  .    c  b    c   b    .  b    .  .    c  b    c  b    c
b    c  .    c  .    c  .    c  b    c   b    .  b    .  .    c  b    c  b    c
 ....    ....    dddd    dddd    dddd     dddd    dddd    ....    dddd    dddd
e    f  .    f  e    .  .    f  .    f   .    f  e    f  .    f  e    f  .    f
e    f  .    f  e    .  .    f  .    f   .    f  e    f  .    f  e    f  .    f
 gggg    ....    gggg    gggg    ....     gggg    gggg    ....    gggg    gggg
  6       2       5       5       4        5       6       3       7       6
"""

abet = "abcdefg"


@utils.part1
def part1(puzzleInput: str):
    # Parse the seven segment signal diagrams from the puzzle input into usable data
    signalGroups: list[list[list[frozenset[str]]]] = [
        [
            [frozenset(subGroup) for subGroup in group.split(" ")]
            for group in line.split(" | ")
        ]
        for line in puzzleInput.strip().splitlines()
    ]

    # For Part 1, we simply count the unique output signals
    count: int = 0
    for _, outputs in signalGroups:
        for segments in outputs:
            if len(segments) in [2, 3, 4, 7]:
                count += 1
    utils.printAnswer(count)

    # Pass the parsed puzzle input to Part 2
    return signalGroups


@utils.part2
def part2(_, signalGroups: list[list[list[frozenset[str]]]]):
    answer: int = 0

    # For each line in the input, we will need to deduce the correct
    # signal wiring configuration
    for inputSignals, outputSignals in signalGroups:
        allSignals = [*inputSignals, *outputSignals]
        known: dict[int, frozenset[str]] = {n: "" for n in range(10)}
        signalMap: dict[str, str] = {s: "" for s in abet}

        # Find the obvious (unique) digits first:
        for signal in allSignals:
            if len(signal) == 2:
                known[1] = signal
            elif len(signal) == 3:
                known[7] = signal
            elif len(signal) == 4:
                known[4] = signal
            elif len(signal) == 7:
                known[8] = signal

        # We can combine 4 and 7 to find the G wire
        fourAndSeven = known[4].union(known[7])
        for signal in allSignals:
            if len(diff := signal.difference(fourAndSeven)) == 1:
                signalMap["g"] = list(diff)[0]
                break

        # We can use this new G wire to derive the 9 pattern
        known[9] = fourAndSeven.union({signalMap["g"]})

        # We can use the difference of 8 and 1 to find 6
        eightLessOne = known[8].difference(known[1])
        for signal in allSignals:
            signalLessOne = signal.difference(known[1])
            if len(signal) == 6 and signalLessOne == eightLessOne:
                known[6] = signal
                break

        # We can use 6 to find 5 and the E wire
        for signal in allSignals:
            if len(signal) == 5 and len(known[6].intersection(signal)) == 5:
                known[5] = signal
                break
        signalMap["e"] = list(known[6].difference(known[5]))[0]

        # We know 9 and 6 so we can now easily deduce 0
        for signal in allSignals:
            if len(signal) == 6 and signal != known[9] and signal != known[6]:
                known[0] = signal

        # We know 5 and the E wire, so we can determine 2 and 3
        for signal in allSignals:
            if len(signal) == 5 and signal != known[5]:
                if signalMap["e"] in signal:
                    known[2] = signal
                else:
                    known[3] = signal

        # Decode the output numerals
        reverseLookup: dict[frozenset[str], int] = {
            s: n for n, s in known.items()
        }
        output = ""
        for signal in outputSignals:
            output += str(reverseLookup[signal])
        answer += int(output)

    utils.printAnswer(answer)


utils.start()
