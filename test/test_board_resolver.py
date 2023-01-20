from board_resolver import BoardResolver
from hints import HintsData
from exception import NoSolutionError
from pytest import raises
import mock


def test_init_board_resolver():
    hints = HintsData(4,
                      [3, 0, 1, 0], [0, 0, 0, 0],
                      [0, 0, 4, 0], [0, 3, 0, 0])
    resolver = BoardResolver(hints)
    assert resolver.flag == 0
    assert resolver.curBrd.board == [[0, 0, 0, 0],
                                     [0, 0, 0, 0],
                                     [0, 0, 0, 0],
                                     [0, 0, 0, 0]]
    assert resolver.condBrd.board == \
        [[[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]],
         [[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]],
         [[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]],
         [[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]]]
    assert resolver.hints == hints


def test_hints_setter():
    resolver = BoardResolver()
    assert resolver.hints.dim == 0
    resolver.hints = HintsData(4,
                               [3, 0, 1, 0], [0, 0, 0, 0],
                               [0, 0, 4, 0], [0, 3, 0, 0])
    assert resolver.hints.dim == 4


def test_resolver_solvable():
    hints = HintsData(4,
                      [3, 0, 1, 0], [0, 0, 0, 0],
                      [0, 0, 4, 0], [0, 3, 0, 0])
    prob = BoardResolver(hints)
    prob.resolver()
    assert prob.flag == 1
    assert prob.curBrd.board == [[2, 1, 4, 3],
                                 [3, 4, 2, 1],
                                 [1, 2, 3, 4],
                                 [4, 3, 1, 2]]


def test_resolver_not_solvable_cond_trigger():
    hints = HintsData(4, [2, 2], [0, 0], [0, 0], [0, 0])
    prob = BoardResolver(hints)
    with raises(NoSolutionError):
        prob.condBrd.analyzeBasicCond(prob.hints)
    with raises(NoSolutionError):
        prob.resolver()


def test_resolver_not_solvable_flag_trigger():
    hints = HintsData(4, [2, 0], [2, 0], [0, 0], [0, 0])
    prob = BoardResolver(hints)
    with raises(NoSolutionError):
        prob.resolver()
    assert prob.flag == 0


def test_file_not_found():
    prob = BoardResolver()
    prob.flag = 1
    with raises(FileNotFoundError):
        prob.saveData("")


def test_saveData():
    content = "Answer to the problem with board size of "\
              "N = 4, and hints is as follows: \n"\
              "[\n3 0 1 0\n0 0 0 0\n0 0 4 0\n0 3 0 0\n]"\
              "\n\n####################\n"\
              "2 1 4 3\n3 4 2 1\n1 2 3 4\n4 3 1 2\n"\
              "####################"
    hints = HintsData(4,
                      [3, 0, 1, 0], [0, 0, 0, 0],
                      [0, 0, 4, 0], [0, 3, 0, 0])
    prob = BoardResolver(hints)
    assert prob.saveData("fake_dir") is None and prob.flag == 0
    prob.resolver()
    with mock.patch('builtins.open', mock.mock_open()) as mocker:
        prob.saveData("fake_dir")
        mocker.assert_called_once_with("fake_dir", "w")
        mocker().write.assert_called_once_with(content)
