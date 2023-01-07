from hints import HintsData
import copy
# constant value
maxInLines = 5


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
    data = HintsData()
    data.dim = len(f[1].split(" "))
    if len(f[2].split(" ")) != data.dim or \
            len(f[3].split(" ")) != data.dim or \
            len(f[4].split(" ")) != data.dim:
        raise invalidDataLength()
    try:
        data.topView = copy.deepcopy([int(x) for x in f[1].split(" ")])
        data.botView = copy.deepcopy([int(x) for x in f[2].split(" ")])
        data.rightView = copy.deepcopy([int(x) for x in f[3].split(" ")])
        data.leftView = copy.deepcopy([int(x) for x in f[4].split(" ")])
    except ValueError:
        raise invalidInputFile()
    return data


def write_data_to_file(dir, ans):
    f = open(dir, 'w')
    for row in ans:
        for cell in row:
            f.write(f"{cell} ")
        f.write("\n")
