#! /usr/bin/env python3
### vendor imports
import bitstring
import numpy
import typing

### local imports
import utils


class Packet(typing.TypedDict):
    v: int
    t: int
    sub: list["Packet"]
    val: typing.Optional[int]


def parsePacketStructure(data: bitstring.BitStream) -> Packet:
    version: int = data.read(3).uint
    typeId: int = data.read(3).uint

    # Type ID 4 is literal int. These are stored in groups of 5 bits
    if typeId == 4:
        intStream = bitstring.BitStream()
        while True:
            chunk = data.read(5)
            intStream.insert(chunk[1:])
            if chunk[0] == 0:
                break
        return {"v": version, "t": typeId, "val": intStream.uint, "sub": []}

    # Else, this is an operator packet
    else:
        subPacketType: bool = data.read(1).bool
        subPackets: list[Packet] = []

        # Sub-packet type 1 consumes a specified number of packets
        if subPacketType:
            for _ in range(data.read(11).uint):
                subPackets.append(parsePacketStructure(data))

        # Sub-packet type 0 consumes a specific number of bits and read all
        # packets contained within.
        else:
            subPacketLength = data.read(15).uint
            subPacketData = data.read(subPacketLength)
            while subPacketData.pos < subPacketLength:
                subPackets.append(parsePacketStructure(subPacketData))

        # Parse the sub packets
        return {"v": version, "t": typeId, "val": None, "sub": subPackets}


def summatePacketVersions(packet: Packet) -> int:
    """Recursively summate all packet version numbers."""
    return packet["v"] + sum(summatePacketVersions(p) for p in packet["sub"])


def executePacket(packet: Packet) -> int:
    """Iterate through packet structure, executing all instructions."""
    typeId = packet["t"]

    # Type ID 4 is literal int, return it immediately
    if typeId == 4:
        return packet["val"]

    subpacketValues = [executePacket(p) for p in packet["sub"]]

    if typeId == 0:
        return sum(subpacketValues)

    elif typeId == 1:
        return int(numpy.prod(subpacketValues))

    elif typeId == 2:
        return min(subpacketValues)

    elif typeId == 3:
        return max(subpacketValues)

    elif typeId == 5:
        return int(subpacketValues[0] > subpacketValues[1])

    elif typeId == 6:
        return int(subpacketValues[0] < subpacketValues[1])

    elif typeId == 7:
        return int(subpacketValues[0] == subpacketValues[1])


@utils.part1
def part1(puzzleInput: str):
    # Parse the puzzle input from hex into a bit stream
    inputPacketData = bitstring.BitStream(hex=puzzleInput.strip())

    # Recursively parse the packet datastream into objects
    packet = parsePacketStructure(inputPacketData)

    # The answer to Part 1 is the sum of all packet versions
    utils.printAnswer(summatePacketVersions(packet))

    # Pass the packet onto Part 2
    return packet


@utils.part2
def part2(_, packet: Packet):
    # For Part 2, we need to recurse through the packets and execute their instructions
    utils.printAnswer(executePacket(packet))


utils.start()
