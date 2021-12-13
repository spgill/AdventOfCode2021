#! /usr/bin/env python3
### stdlib imports
import re

### vendor imports
from advent_of_code_ocr import convert_6
import numpy

### local imports
import utils


@utils.part1
def part1(puzzleInput: str):
    # Parse the puzzle input into a coordinates array and list of fold instructions
    coordsInput, foldsInput = puzzleInput.strip().split("\n\n")
    coords: list[tuple[int, int]] = [
        tuple(int(n) for n in line.split(","))
        for line in coordsInput.strip().splitlines()
    ]
    folds: list[tuple[str, int]] = [
        (pair.split("=")[0], int(pair.split("=")[1]))
        for pair in re.findall(r"[xy]=\d+", foldsInput)
    ]

    # Create a new array and populate it with the coordinates
    sizeX = max(c[0] for c in coords) + 1
    sizeY = max(c[1] for c in coords) + 1
    matrix = numpy.zeros((sizeY, sizeX))
    for x, y in coords:
        matrix[y][x] = 1

    # Iterate though each fold instruction and apply it to the matrix
    for i, (foldAxis, foldCoord) in enumerate(folds):
        numpyAxis = int(foldAxis == "x")
        a, _, b = numpy.split(matrix, [foldCoord, foldCoord + 1], numpyAxis)

        # If b isn't the same shape as a, we need to do transpose it onto an
        # array of the same shape as a.
        if b.shape != a.shape:
            transpo = numpy.zeros(a.shape)
            transpo[: b.shape[0], : b.shape[1]] = b
            b = transpo

        # Flip b and apply it onto a
        matrix = a + numpy.flip(b, numpyAxis)

        # The answer to Part 1 is the number of visible dots after ONLY ONE FOLD
        if i == 0:
            utils.printAnswer(numpy.count_nonzero(matrix))

    # Return the completed matrix to Part 2
    return matrix


@utils.part2
def part2(_, matrix: numpy.ndarray):
    # Part 1 did the heavy lifting of completing all the folds, we just need to
    # print the graphic to the console.
    messageLines = []
    for row in matrix:
        line = ""
        for n in row:
            if n > 0:
                line += "█"
            else:
                line += " "
        messageLines.append(line)
    message = "\n" + "\n".join(messageLines)

    # Attempt to convert the message to plaintext. Conversion doesn't work
    # on the example problems.
    try:
        message = convert_6(message[1:], fill_pixel="█", empty_pixel=" ")
    except ValueError:
        utils.printWarning("Could not convert ASCII characters to plaintext")

    utils.printAnswer(message)


utils.start()
