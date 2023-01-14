from hints import HintsData
# constant value
maxInLines = 4


class invalidInputFile(Exception):
    def __init__(self):
        super().__init__("Input data in this file is in the wrong format")


class invalidDataLength(Exception):
    def __init__(self):
        super().__init__("The length of input data is incorrect")


def read_data_from_file(dir):
    f = open(dir, 'r').read().splitlines()
    if len(f) != maxInLines:
        raise invalidDataLength()
    tmpDim = len(f[0].split(" "))
    if len(f[1].split(" ")) != tmpDim or \
            len(f[2].split(" ")) != tmpDim or \
            len(f[3].split(" ")) != tmpDim:
        raise invalidDataLength()
    try:
        hints = HintsData(tmpDim,
                          [int(x) for x in f[0].split(" ")],
                          [int(x) for x in f[1].split(" ")],
                          [int(x) for x in f[2].split(" ")],
                          [int(x) for x in f[3].split(" ")])
    except ValueError:
        raise invalidInputFile()
    return hints


def write_data_to_file(dir, ans):
    f = open(dir, 'w')
    for row in ans:
        for cell in row:
            f.write(f"{cell} ")
        f.write("\n")
