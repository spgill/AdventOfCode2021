"""
This module provides helper functions for Advent of Code solutions.
"""
### stdlib imports
import copy
import typing

### vendor imports
from colorama import Fore, Style
import typer


# Global variables
_quietMode: bool = False
_part1SolutionFunc: typing.Optional[typing.Callable] = None
_part2SolutionFunc: typing.Optional[typing.Callable] = None
_solutionOptions: dict[str, typing.Union[str, bool]] = {}


def getOption(key: str) -> typing.Union[str, bool, None]:
    """Get the value of a CLI solution option. If not defined, will return `None`."""
    return _solutionOptions.get(key, None)


def part1(func: typing.Callable[[str], typing.Any]):
    """
    Decorator to wrap around the solution method for Part 1.

    The first (and only) positional argument is the puzzle input.

    Return value is passed onto the solution function for Part 2.

    Example;
    ```
    @utils.part1
    def solutionOne(data: str):
        answer = math.sqrt(len(data))
        utils.printAnswer(str(answer))
        return answer
    ```
    """
    global _part1SolutionFunc
    _part1SolutionFunc = func
    return func


def part2(func: typing.Callable[[str, typing.Any], None]):
    """
    Decorator to wrap around the solution method for Part 2.

    The first positional argument is the puzzle input. The second argument is
    the return value from Part 1's solution function.

    Example;
    ```
    @utils.part2
    def solutionTwo(data: str, previous: int):
        answer = previous * math.pi
        utils.printAnswer(str(answer))
    ```
    """
    global _part2SolutionFunc
    _part2SolutionFunc = func
    return func


def _cli(
    input: typer.FileBinaryRead = typer.Argument(
        ..., help="Puzzle input file. Use '-' to read from STDIN."
    ),
    quiet: bool = typer.Option(
        False,
        "-q",
        "--quiet",
        help="Enabled quiet mode. Suppresses messages and warnings. Errors will still be written to STDERR.",
    ),
    part2: bool = typer.Option(
        True, help="Execute the Part 2 solution. Part 1 will ALWAYS execute."
    ),
    option: list[str] = typer.Option(
        [],
        "-o",
        "--option",
        help="Provide an execution option to the solution methods. Syntax is '--option KEY=VALUE' or '--option FLAG' for a boolean flag. Available execution options should be documented in the solution script itself.",
    ),
):
    """Internal method for executing the puzzle solutions."""
    # First we need to read and decode the puzzle input.
    inputData: str = input.read().decode()

    # Next, we should parse out any key=value options
    for entry in option:
        entrySplit = entry.split("=")
        key = entrySplit[0]
        value = True if len(entrySplit) == 1 else entrySplit[1]
        _solutionOptions[key] = value

    global _quietMode, _part1SolutionFunc, _part2SolutionFunc
    _quietMode = quiet

    # Run the part 1 solution
    if _part1SolutionFunc is None:
        printError("No solution method for Part 1 was defined!")
    printMessage("Part 1 solution is executing...")
    part1Result: typing.Any = _part1SolutionFunc(copy.copy(inputData))

    # Run the part 2 solution if desired and it exists
    if part2:
        printMessage("")
        if _part2SolutionFunc is None:
            printWarning("No solution method for Part 2 was defined!")
        else:
            printMessage("Part 2 solution is executing...")
            _part2SolutionFunc(copy.copy(inputData), part1Result)


def start():
    """This method will start the Typer CLI."""
    typer.run(_cli)


def printMessage(message: str) -> None:
    if not _quietMode:
        typer.echo(message)


def printAnswer(value: typing.Any) -> None:
    """Print the solution to Part `part` of the puzzle"""
    if _quietMode:
        typer.echo(f"{value}")
    else:
        typer.echo(f"{Fore.GREEN}Answer:{Style.RESET_ALL} {value}")


def printWarning(message: str) -> None:
    """Print a warning message."""
    printMessage(f"{Fore.YELLOW}Warning:{Style.RESET_ALL} {message}")


def printComputationWarning() -> None:
    """Print a warning about computation time."""
    printWarning("It may take awhile to compute answers...")


def printComputationWarningWithPrompt() -> None:
    """
    Print a warning about computation time,
    prompting the user to continue.
    """
    if not _quietMode:
        typer.confirm(
            f"{Fore.YELLOW}Warning:{Style.RESET_ALL} "
            "It may take a very long while to compute answers. Continue?",
            default=True,
            abort=True,
        )


def printError(message: str) -> None:
    """Print an error in red and abort execution"""
    typer.echo(f"{Fore.RED}Error: {Style.RESET_ALL}{message}", err=True)
    exit(1)
