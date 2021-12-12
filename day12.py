#! /usr/bin/env python3
### stdlib imports
import copy

### local imports
import utils


def traverseCave(
    graph: dict[str, set[str]],
    current: str,
    history: list[str] = None,
    allowRepeats: bool = False,
):
    # Initialize the history list
    if history is None:
        history = []

    # Create a copy of the history, to maintain immutability between branches
    history = copy.copy(history)

    # Add current segment to the path
    history.append(current)

    # If this is the end, immediately return
    if current == "end":
        return 1

    # Look through the available paths for branching. Summate return values.
    tally: int = 0
    for cave in graph[current]:
        passAllowRepeats = allowRepeats
        if cave.islower() and cave in history:
            if passAllowRepeats:
                passAllowRepeats = False
            else:
                continue
        tally += traverseCave(graph, cave, history, passAllowRepeats)
    return tally


@utils.part1
def part1(puzzleInput: str):
    # Parse the input lines lines and build a graph linking each node together
    pairs = [line.split("-") for line in puzzleInput.strip().splitlines()]
    graph: dict[str, set[str]] = {}
    for a, b in pairs:
        graph.setdefault(a, set()).add(b)
        # Don't link any node back to start
        if a != "start":
            graph.setdefault(b, set()).add(a)

    # The answer is the total number of traversable paths. Discovered recursively.
    utils.printAnswer(traverseCave(graph, "start"))

    # Pass the graph on to Part 2
    return graph


@utils.part2
def part2(_, graph: dict[str, set[str]]):
    # The answer for this part is the same as Part 1, except that a _single_ small
    # cave may be visited twice.
    utils.printAnswer(traverseCave(graph, "start", allowRepeats=True))


utils.start()
