#! /usr/bin/env python3
### stdlib imports
import copy

### local imports
import utils


def getNeighbors(
    grid: list[list[int]],
    coords: tuple[int, int],
) -> list[tuple[int, int], int]:
    """Returns the value of all *valid* adjacent (incl. diagonal) octopi."""
    originX, originY = coords
    sizeY = len(grid) - 1
    sizeX = len(grid[0]) - 1
    for y in [-1, 0, 1]:
        for x in [-1, 0, 1]:
            if x == 0 and y == 0:
                continue
            if (
                (originX == 0 and x == -1)
                or (originX == sizeX and x == 1)
                or (originY == 0 and y == -1)
                or (originY == sizeY and y == 1)
            ):
                continue
            cellX = originX + x
            cellY = originY + y
            yield (cellX, cellY)


def flashOctopus(grid: list[list[int]], coords: tuple[int, int]):
    """Flash this octopus and recursively increment (and flash) neighboring octopi."""
    x, y = coords

    # If this octopus has already been flashed (via a previous recursive pass),
    # we can return immediately
    if grid[y][x] == -1:
        return

    # Mark current grid cell as flashed
    grid[y][x] = -1

    # Look through neighboring cells and increment them. Flashing when necessary.
    for neighborCoords in getNeighbors(grid, coords):
        neighborX, neighborY = neighborCoords
        value = grid[neighborY][neighborX]
        if value >= 9:
            flashOctopus(grid, neighborCoords)
        elif value >= 0:
            grid[neighborY][neighborX] = value + 1


def simulateOneStep(grid: list[list[int]]) -> int:
    """Simulate one step of the octopi grid and return the number of flashes seen."""
    flashes: int = 0

    # The first task is to go through and increment the base energy level of every octopus
    for y in range(10):
        for x in range(10):
            grid[y][x] = grid[y][x] + 1

    # Next task is to go through the grid and flash any octopi with high
    # enough energy levels. This is recursive
    for y in range(10):
        for x in range(10):
            if grid[y][x] > 9:
                flashOctopus(grid, (x, y))

    # The last task is to go through and count all of the flashes from this
    # simulation step. Also use this opportunity to reset flashed octopi
    # to a state of 0
    for y in range(10):
        for x in range(10):
            if grid[y][x] == -1:
                flashes += 1
                grid[y][x] = 0

    return flashes


@utils.part1
def part1(puzzleInput: str):
    # Parse the puzzle input into a grid of ints
    inputGrid = [
        [int(n) for n in list(line)]
        for line in puzzleInput.strip().splitlines()
    ]
    grid = copy.deepcopy(inputGrid)

    # Variable number of steps to simulate
    steps = int(utils.getOption("steps") or 100)

    flashes: int = 0

    # Simulate the octopus grid for however many steps specified, via multiple passes
    for i in range(steps):
        flashes += simulateOneStep(grid)

    # The answer is the total number of flashes after 100 steps
    utils.printAnswer(flashes)

    # Return the original (unaltered) copy of the grid for Part 2 to work with
    return inputGrid


@utils.part2
def part2(_, grid: list[list[int]]):
    # This part is simple. Simulate the grid until all octopi flash in unison.
    i = 1
    while True:
        flashes = simulateOneStep(grid)
        if flashes == 100:
            utils.printAnswer(i)
            exit()
        i += 1


utils.start()
