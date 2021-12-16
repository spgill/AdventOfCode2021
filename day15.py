#! /usr/bin/env python3
### vendor imports
import numpy as np
import numpy.typing as npt

### local imports
import utils


def getAdjacentCells(
    grid: npt.NDArray[np.int64],
    xy: tuple[int, int],
) -> list[tuple[tuple[int, int], np.int64]]:
    """Returns the value of all *valid* adjacent cells. Does not include diagnally adjacent cells."""
    x, y = xy
    maxY = grid.shape[1] - 1
    maxX = grid.shape[0] - 1

    if x > 0:
        yield ((x - 1, y), grid[y][x - 1])
    if x < maxX:
        yield ((x + 1, y), grid[y][x + 1])
    if y > 0:
        yield ((x, y - 1), grid[y - 1][x])
    if y < maxY:
        yield ((x, y + 1), grid[y + 1][x])


def findShortestPath(grid: npt.NDArray[np.int64]) -> int:
    """Use Dijkstra's algorithm to find the "safest" path through the grid"""
    # For part 1, we will be using Dijkstra's algorithm to find the "safest" path
    # through the grid.
    visited: npt.NDArray[np.bool_] = np.zeros(grid.shape, dtype=bool)
    distanceGrid: npt.NDArray[np.float64] = np.full(
        grid.shape, np.inf, dtype=float
    )

    # The origin and destination points
    origin = (0, 0)
    distanceGrid[origin] = 0
    destination = tuple(n - 1 for n in grid.shape)

    # We start calculating distances from the origin in the top left corner
    node = origin

    # Iterate through each unvisited cell in the grid and calculate distance
    # to neighbors
    while not visited[destination]:
        if not visited[node]:
            for neighborCoord, _ in getAdjacentCells(grid, node):
                if (
                    neighborDistance := (
                        distanceGrid[node] + grid[neighborCoord]
                    )
                ) < distanceGrid[neighborCoord]:
                    distanceGrid[neighborCoord] = neighborDistance
            visited[node] = True

        # The next node to visit the the most minimum un-visited node
        minimumNodes = np.where(
            np.logical_and(
                distanceGrid == np.amin(distanceGrid[np.invert(visited)]),
                np.invert(visited),
            )
        )
        node = (minimumNodes[0][0], minimumNodes[1][0])
        if node == destination:
            break

    return int(distanceGrid[destination])


@utils.part1
def part1(puzzleInput: str):
    # Parse the input into a grid of ints
    grid: npt.NDArray[np.int64] = np.array(
        [
            [int(n) for n in list(line)]
            for line in puzzleInput.strip().splitlines()
        ]
    )

    # For Part 1, we just find the shortest path through the exact grid given
    # in the input.
    utils.printAnswer(findShortestPath(grid))

    # Pass the original grid onto Part 2
    return grid


@utils.part2
def part2(_, grid: npt.NDArray[np.int64]):
    utils.printComputationWarning()

    # The first step in Part 2 is to construct the 5x expanded grid
    gridSizeX, gridSizeY = grid.shape
    expandedGrid: npt.NDArray[np.int64] = np.zeros(
        (gridSizeX * 5, gridSizeY * 5), dtype=np.int64
    )

    # We iterate through the values of the original grid, and transcribe them
    # (after incrementing them) to the other regions of the expanded grid.
    for y in range(gridSizeY):
        for x in range(gridSizeY):
            # Copy the small grid values to the upper left region of the expanded grid
            expandedGrid[(x, y)] = grid[(x, y)]

            # Apply incremented values to the other regions
            for expandY in range(5):
                for expandX in range(5):
                    if (expandX, expandY) == (0, 0):
                        continue
                    newX = x + expandX * gridSizeX
                    newY = y + expandY * gridSizeY
                    newValue = (grid[(x, y)] + expandY + expandX - 1) % 9 + 1
                    expandedGrid[(newX, newY)] = newValue

    # The solution for Part 2 is the shortest path through this new expanded grid
    utils.printAnswer(findShortestPath(expandedGrid))


utils.start()
