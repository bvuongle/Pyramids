import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from condition_analysis import CondBoard  # noqa: E402
from hints import HintsData  # noqa: E402
from exception import NoSolutionError, InsufficientData  # noqa: E402
from pytest import raises  # noqa: E402


def test_init_condBrd():
    condBrd = CondBoard(3)
    assert condBrd.dim == 3
    assert condBrd.board == [[[1, 2, 3], [1, 2, 3], [1, 2, 3]],
                             [[1, 2, 3], [1, 2, 3], [1, 2, 3]],
                             [[1, 2, 3], [1, 2, 3], [1, 2, 3]]]


def test_topCond_case_01N():
    condBrd = CondBoard(3)
    topHint = [0, 0, 0]
    condBrd.topCond(topHint)
    assert condBrd.board == [[[1, 2, 3], [1, 2, 3], [1, 2, 3]],
                             [[1, 2, 3], [1, 2, 3], [1, 2, 3]],
                             [[1, 2, 3], [1, 2, 3], [1, 2, 3]]]
    topHint = [0, 1, 3]
    condBrd.topCond(topHint)
    assert condBrd.board == [[[2], [3], [1]],
                             [[1, 3], [1], [2]],
                             [[1, 2], [1, 2], [3]]]


def test_topCond_case_range2N():
    condBrd = CondBoard(5)
    topHint = [0, 4, 0, 0, 0]
    condBrd.topCond(topHint)
    assert condBrd.board == \
        [[[1, 2, 3, 4, 5], [1, 2], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5]],  # noqa: E501
         [[1, 2, 3, 4, 5], [1, 2, 3, 4], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5]],  # noqa: E501
         [[1, 2, 3, 4, 5], [1, 2, 3, 4], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5]],  # noqa: E501
         [[1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5]],  # noqa: E501
         [[1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5]]]  # noqa: E501


def test_topCond_error():
    condBrd1 = CondBoard(3)
    topHint = [0, 0]
    with raises(InsufficientData):
        condBrd1.topCond(topHint)

    topHint = [1, 0, 1]
    assert condBrd1.noSolutionCheck(topHint) is False
    with raises(NoSolutionError):
        condBrd1.topCond(topHint)

    condBrd2 = CondBoard(5)
    topHint = [1, 5, 0, 0, 5]
    assert condBrd2.noSolutionCheck(topHint) is False
    with raises(NoSolutionError):
        condBrd2.topCond(topHint)


def test_botCond():
    condBrd1 = CondBoard(3)
    botHint = [0, 0, 0]
    condBrd1.botCond(botHint)
    assert condBrd1.board == [[[1, 2, 3], [1, 2, 3], [1, 2, 3]],
                              [[1, 2, 3], [1, 2, 3], [1, 2, 3]],
                              [[1, 2, 3], [1, 2, 3], [1, 2, 3]]]
    botHint = [0, 1, 3]
    condBrd1.botCond(botHint)
    assert condBrd1.board == [[[1, 2], [1, 2], [3]],
                              [[1, 3], [1], [2]],
                              [[2], [3], [1]]]
    condBrd2 = CondBoard(5)
    botHint = [0, 4, 0, 0, 0]
    condBrd2.botCond(botHint)
    assert condBrd2.board == \
        [[[1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5]],  # noqa: E501
         [[1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5]],  # noqa: E501
         [[1, 2, 3, 4, 5], [1, 2, 3, 4], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5]],  # noqa: E501
         [[1, 2, 3, 4, 5], [1, 2, 3, 4], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5]],  # noqa: E501
         [[1, 2, 3, 4, 5], [1, 2], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5]]]  # noqa: E501


def test_botCond_error():
    condBrd1 = CondBoard(3)
    botHint = [0, 0]
    with raises(InsufficientData):
        condBrd1.botCond(botHint)

    botHint = [1, 0, 1]
    with raises(NoSolutionError):
        condBrd1.botCond(botHint)

    condBrd2 = CondBoard(5)
    botHint = [1, 5, 0, 0, 5]
    with raises(NoSolutionError):
        condBrd2.topCond(botHint)


def test_rightCond():
    condBrd1 = CondBoard(3)
    rightHint = [0, 0, 0]
    condBrd1.rightCond(rightHint)
    assert condBrd1.board == [[[1, 2, 3], [1, 2, 3], [1, 2, 3]],
                              [[1, 2, 3], [1, 2, 3], [1, 2, 3]],
                              [[1, 2, 3], [1, 2, 3], [1, 2, 3]]]
    rightHint = [0, 1, 3]
    condBrd1.rightCond(rightHint)
    assert condBrd1.board == [[[2], [1, 3], [1, 2]],
                              [[3], [1], [1, 2]],
                              [[1], [2], [3]]]
    condBrd2 = CondBoard(5)
    rightHint = [0, 4, 0, 0, 0]
    condBrd2.rightCond(rightHint)
    assert condBrd2.board == \
        [[[1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5]],  # noqa: E501
         [[1, 2], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5]],  # noqa: E501
         [[1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5]],  # noqa: E501
         [[1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5]],  # noqa: E501
         [[1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5]]]  # noqa: E501


def test_rightCond_error():
    condBrd1 = CondBoard(3)
    rightHint = [0, 0]
    with raises(InsufficientData):
        condBrd1.rightCond(rightHint)

    rightHint = [1, 0, 1]
    with raises(NoSolutionError):
        condBrd1.rightCond(rightHint)

    condBrd2 = CondBoard(5)
    rightHint = [1, 5, 0, 0, 5]
    with raises(NoSolutionError):
        condBrd2.rightCond(rightHint)


def test_leftCond():
    condBrd1 = CondBoard(3)
    leftHint = [0, 0, 0]
    condBrd1.leftCond(leftHint)
    assert condBrd1.board == [[[1, 2, 3], [1, 2, 3], [1, 2, 3]],
                              [[1, 2, 3], [1, 2, 3], [1, 2, 3]],
                              [[1, 2, 3], [1, 2, 3], [1, 2, 3]]]
    leftHint = [0, 1, 3]
    condBrd1.leftCond(leftHint)
    assert condBrd1.board == [[[1, 2], [1, 3], [2]],
                              [[1, 2], [1], [3]],
                              [[3], [2], [1]]]
    condBrd2 = CondBoard(5)
    leftHint = [0, 4, 0, 0, 0]
    condBrd2.leftCond(leftHint)
    assert condBrd2.board == \
        [[[1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5]],  # noqa: E501
         [[1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2]],  # noqa: E501
         [[1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5]],  # noqa: E501
         [[1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5]],  # noqa: E501
         [[1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5]]]  # noqa: E501


def test_leftCond_no_sol():
    condBrd1 = CondBoard(3)
    leftHint = [0, 0]
    with raises(InsufficientData):
        condBrd1.leftCond(leftHint)

    leftHint = [1, 0, 1]
    with raises(NoSolutionError):
        condBrd1.leftCond(leftHint)

    condBrd2 = CondBoard(5)
    leftHint = [1, 5, 0, 0, 5]
    with raises(NoSolutionError):
        condBrd2.leftCond(leftHint)


def test_rem_Redundant_Cond():
    condBrd = CondBoard(3)
    condBrd.board = [[[1, 2, 3], [1, 2, 3], [1, 2, 3]],
                     [[1, 2, 3], [3],       [1, 2, 3]],
                     [[1, 2, 3], [1, 2, 3], [1, 2, 3]]]
    condBrd.remRedundantCond()
    assert condBrd.board == [[[1, 2, 3], [1, 2], [1, 2, 3]],
                             [[1, 2], [3], [1, 2]],
                             [[1, 2, 3], [1, 2], [1, 2, 3]]]


def test_all_analysis():
    condBrd = CondBoard(4)
    hints = HintsData(4,
                      [3, 0, 1, 0],
                      [0, 0, 0, 0],
                      [0, 0, 4, 0],
                      [0, 3, 0, 0])
    condBrd.analyzeBasicCond(hints)
    assert condBrd.board == [[[2], [1, 3], [4], [1, 3]],
                             [[3], [1, 4], [1, 2], [1, 2]],
                             [[1], [2], [3], [4]],
                             [[4], [1, 3], [1, 2], [1, 2, 3]]]
