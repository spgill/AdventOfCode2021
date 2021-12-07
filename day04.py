#! /usr/bin/env python3
### stdlib imports
import re
import typing

### local imports
import utils


class BingoBoardObject(typing.TypedDict):
    complete: bool
    grid: list[list[int]]
    colCount: list[int]
    rowCount: list[int]


def getBoardWinOrder(
    drawnNumbers: list[int], boards: list[BingoBoardObject]
) -> typing.Generator[int, None, None]:
    # Iterate through all drawn numbers, and run "simulations" on all bingo boards
    for currentIndex, currentNumber in enumerate(drawnNumbers):
        allNumbers = drawnNumbers[: currentIndex + 1]
        for board in boards:
            for x in range(5):
                for y in range(5):
                    value = board["grid"][y][x]
                    if value == currentNumber:
                        board["colCount"][x] += 1
                        board["rowCount"][y] += 1

                        # If any of the rows or columns are now 5, we have a bingo
                        bingo = False
                        for col in board["colCount"]:
                            if col == 5:
                                bingo = True
                        for row in board["rowCount"]:
                            if row == 5:
                                bingo = True

                        # If bingo, calculate the answer
                        if bingo and not board["complete"]:
                            board["complete"] = True
                            sum = 0
                            for sumX in range(5):
                                for sumY in range(5):
                                    sumValue = board["grid"][sumY][sumX]
                                    if sumValue not in allNumbers:
                                        sum += sumValue
                            yield sum * currentNumber
                            break


@utils.part1
def part1(puzzleInput: str):
    # First line of the input is drawn numbers
    drawnNumbers = [int(n) for n in puzzleInput.splitlines()[0].split(",")]

    # Proceeding lines are groups of numbers representing boards
    boardGrids = [
        [
            [int(match) for match in re.findall(r"\d+", line)]
            for line in group.strip().splitlines()
        ]
        for group in puzzleInput.strip().split("\n\n")[1:]
    ]

    # Create dicts representing the boards and including row/column counts
    boardObjects: list[BingoBoardObject] = []
    for grid in boardGrids:
        boardObjects.append(
            {
                "grid": grid,
                "colCount": [0 for i in range(5)],
                "rowCount": [0 for i in range(5)],
                "complete": False,
            }
        )

    # The answer is the first board to win
    boardWins = list(getBoardWinOrder(drawnNumbers, boardObjects))
    utils.printAnswer(boardWins[0])
    return boardWins


@utils.part2
def part2(_, boardWins: list[str]):
    # We've already done the heavy lifting so the answer is just the last
    # board win.
    utils.printAnswer(boardWins[-1])


utils.start()
