#! /usr/bin/env python3
### stdlib imports
import pathlib

### local imports
import utils


@utils.part1
def part1(puzzleInput: str):
    # Parse the coordinate pairs from the puzzle input
    coordList = [
        [
            tuple(int(coord) for coord in pair.split(","))
            for pair in line.split(" -> ")
        ]
        for line in puzzleInput.strip().splitlines()
    ]

    # Dictionary containing lookups for coordinate hits
    part1Grid: dict[tuple[int, int], int] = {}
    part2Grid: dict[tuple[int, int], int] = {}

    # Iterate through each line pair and mark each coordinate the line passes through
    for (startX, startY), (endX, endY) in coordList:
        xMod = -1 if endX < startX else 1
        xRange = range(startX, endX + xMod, xMod)

        yMod = -1 if endY < startY else 1
        yRange = range(startY, endY + yMod, yMod)

        # For horizontal and vertical lines, it's sufficient to simply loop through the coordinates
        if startX == endX or startY == endY:
            for x in xRange:
                for y in yRange:
                    part1Grid[(x, y)] = part1Grid.get((x, y), 0) + 1
                    part2Grid[(x, y)] = part2Grid.get((x, y), 0) + 1

        # For diagonal lines (45 deg only) we can assume the x and y ranges are equal in length
        else:
            for i, x in enumerate(xRange):
                y = yRange[i]
                part2Grid[(x, y)] = part2Grid.get((x, y), 0) + 1

    # If the draw option is enabled, create visualization images
    if utils.getOption("draw"):
        from PIL import Image

        maxX, maxY = 0, 0

        for (startX, startY), (endX, endY) in coordList:
            maxX = max(startX, endX, maxX)
            maxY = max(startY, endY, maxY)

        for i, grid in enumerate([part1Grid, part2Grid]):
            canvas = Image.new("RGB", (maxX + 1, maxY + 1))

            for coord, count in grid.items():
                canvas.putpixel(
                    coord, (255, 0, 0) if count > 1 else (255, 255, 255)
                )

            canvas.save(pathlib.Path.cwd() / f"day05.part{i + 1}.png")

    # The answer is the number of grid coordinates with more than one line
    utils.printAnswer(len([item for item in part1Grid.items() if item[1] > 1]))

    # Pass the part 2 answer to its solution function
    return len([item for item in part2Grid.items() if item[1] > 1])


@utils.part2
def part2(_, answer: int):
    # Part 1 counted the overlapping points for diagonal lines as well,
    # so we can just print the answer
    utils.printAnswer(answer)


utils.start()
