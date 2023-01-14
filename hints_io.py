from hints import HintsData
from board import Board
# constant value
maxInLines = 4


class invalidInputFile(Exception):
    def __init__(self):
        super().__init__("Input data in this file is in the wrong format")


class invalidDataLength(Exception):
    def __init__(self):
        super().__init__("The length of input data is incorrect")


def read_data_from_file(dir):
    f = open(dir, 'r')
    lines = f.read().splitlines()
    if len(lines) != maxInLines:
        raise invalidDataLength()
    tmpDim = len(lines[0].split(" "))
    if len(lines[1].split(" ")) != tmpDim or \
            len(lines[2].split(" ")) != tmpDim or \
            len(lines[3].split(" ")) != tmpDim:
        raise invalidDataLength()
    try:
        hints = HintsData(tmpDim,
                          [int(x) for x in lines[0].split(" ")],
                          [int(x) for x in lines[1].split(" ")],
                          [int(x) for x in lines[2].split(" ")],
                          [int(x) for x in lines[3].split(" ")])
    except ValueError:
        raise invalidInputFile()
    f.close()
    return hints


def write_data_to_file(dir, hints: HintsData, ans: Board):
    f = open(dir, 'w')
    f.write(f"Answer to the problem with board size of N = {hints.dim},")
    f.write(" and hints is as follows: ")
    f.write("\n[\n")
    f.writelines(f"{x} " for x in hints.topHint)
    f.write("\n")
    f.writelines(f"{x} " for x in hints.botHint)
    f.write("\n")
    f.writelines(f"{x} " for x in hints.rightHint)
    f.write("\n")
    f.writelines(f"{x} " for x in hints.leftHint)
    f.write("\n]\n\n")
    f.write("#"*20)
    f.write("\n")
    for row in ans.board:
        for cell in row:
            f.write(f"{cell} ")
        f.write("\n")
    f.write("#"*20)
    f.close()
