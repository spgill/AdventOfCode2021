#! /usr/bin/env python3
### stdlib imports
from collections import deque
import statistics

### local imports
import utils

# Constants
openingBrackets = ["(", "[", "{", "<"]
closingBrackets = [")", "]", "}", ">"]
errorScores = {")": 3, "]": 57, "}": 1197, ">": 25137}
completionScores = {"(": 1, "[": 2, "{": 3, "<": 4}


@utils.part1
def part1(puzzleInput: str):
    # Parse the puzzle input into lines
    puzzleLines = puzzleInput.strip().splitlines()

    # Iterate through each line and look for illegal characters. Use these
    # illegal closing characters to compute the error checking score.
    score: int = 0
    corruptedLines: list[int] = []
    for i, line in enumerate(puzzleLines):
        stack: deque[str] = deque()
        for char in line:
            if char in openingBrackets:
                stack.append(char)
            else:
                previous = stack.pop()
                if closingBrackets.index(char) != openingBrackets.index(
                    previous
                ):
                    corruptedLines.append(i)
                    score += errorScores[char]
                    break

    # The score is the answer
    utils.printAnswer(score)

    # Remove the corrupted lines from the input and pass them to Part 2
    [puzzleLines.pop(i) for i in reversed(corruptedLines)]
    return puzzleLines


@utils.part2
def part2(_, incompleteLines: list[str]):
    # Iterate through the incomplete lines and figure out which opening
    # brackets have not been closed. Use this to generate a score for each line.
    scores: list[int] = []
    for line in incompleteLines:
        lineScore: int = 0
        stack: deque[str] = deque()

        # First create a stack and remove opening brackets as they are closed.
        # This gives us a list of brackets that remain to be closed
        for char in line:
            if char in openingBrackets:
                stack.append(char)
            else:
                stack.pop()

        # Iterate through the un-closed brackets and tally the score
        lineScore: int = 0
        for char in reversed(list(stack)):
            lineScore *= 5
            lineScore += completionScores[char]

        scores.append(lineScore)

    # The answer is the median score
    utils.printAnswer(statistics.median(sorted(scores)))


utils.start()
