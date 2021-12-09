#! /usr/bin/env python3
### stdlib imports
from functools import reduce

### local imports
import utils


def getAdjacentValues(
    grid: list[list[int]],
    coords: tuple[int, int],
) -> list[tuple[tuple[int, int], int]]:
    """Returns the value of all *valid* adjacent cells. Does not include diagnally adjacent cells."""
    x, y = coords
    sizeY = len(grid) - 1
    sizeX = len(grid[0]) - 1

    adjacent: list[int] = []
    if x > 0:
        adjacent.append(((x - 1, y), grid[y][x - 1]))
    if x < sizeX:
        adjacent.append(((x + 1, y), grid[y][x + 1]))
    if y > 0:
        adjacent.append(((x, y - 1), grid[y - 1][x]))
    if y < sizeY:
        adjacent.append(((x, y + 1), grid[y + 1][x]))

    return adjacent


def discoverBasin(
    grid: list[list[int]],
    coords: tuple[int, int],
    traversed: set[tuple[int, int]] = None,
) -> set[tuple[int, int]]:
    """Recursively traverse the grid looking for every cell of a 'basin'."""
    if traversed is None:
        traversed = set()
    traversed.add(coords)
    for adjacentCoords, adjacentValue in getAdjacentValues(grid, coords):
        if adjacentCoords in traversed or adjacentValue == 9:
            continue
        discoverBasin(grid, adjacentCoords, traversed)
    return traversed


@utils.part1
def part1(puzzleInput: str):
    # Parse the puzzle input into a grid
    grid = [
        [int(n) for n in list(line)]
        for line in puzzleInput.strip().splitlines()
    ]

    # Iterate through each location on the grid and find the "low" points,
    # which is to say points that are lower than all adjacent neighboring cells
    lowPoints: list[tuple[int, int, int]] = []
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            value = grid[y][x]
            if value < min([v[1] for v in getAdjacentValues(grid, (x, y))]):
                lowPoints.append(((x, y), value))

    # The answer is the sum of these low points + length
    utils.printAnswer(sum([lp[1] for lp in lowPoints]) + len(lowPoints))

    # Pass the list of low points to Part 2
    return lowPoints


@utils.part2
def part2(puzzleInput: str, lowPoints: list[tuple[tuple[int, int], int]]):
    # Parse the puzzle input into a grid
    grid = [
        [int(n) for n in list(line)]
        for line in puzzleInput.strip().splitlines()
    ]

    # Iterate through the low points discovered in Part 1, and calculate the size
    # of the basins they reside in.
    basinSizes: list[int] = [
        len(discoverBasin(grid, coords)) for coords, _ in lowPoints
    ]

    # The answer is the largest three basins' areas multiplied
    utils.printAnswer(
        reduce(lambda x, y: x * y, sorted(basinSizes, reverse=True)[:3])
    )


utils.start()
