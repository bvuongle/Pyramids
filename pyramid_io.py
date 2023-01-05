from libs import *
from global_value import *


class invalidInputFile(Exception):
    def __init__(self) -> None:
        super().__init__("Input data in this file is in the wrong format")


def read_data_from_file(dir):
    f = open(dir, 'r').read().splitlines()
    global N, topView, botView, rightView, leftView
    if(len(f) != maxInLines):
        raise invalidInputFile()
    try:
        N = int(f[0])
    except ValueError:
        raise invalidInputFile()
    # Kiem tra xem co the convert qua int khong?
    topView = copy.deepcopy([int(x) for x in f[1].split(" ")])
    botView = copy.deepcopy([int(x) for x in f[2].split(" ")])
    rightView = copy.deepcopy([int(x) for x in f[3].split(" ")])
    leftView = copy.deepcopy([int(x) for x in f[4].split(" ")])
    

def write_data_to_file(dir, ans):
    f = open(dir, 'w')
    for row in ans:
        for cell in row:
            f.write(f"{cell} ")
        f.write("\n")

