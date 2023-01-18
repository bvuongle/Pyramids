import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hints import HintsData  # noqa: E402
from exception import NonStandardChars, LengthFileIncorrect  # noqa: E402
from exception import OutsideRange  # noqa: E402
import mock  # noqa: E402
from pytest import raises  # noqa: E402


def test_init_hints():
    newHints = HintsData(dim=2,
                         topHint=[0, 0],
                         botHint=[1, 1],
                         rightHint=[0, 0],
                         leftHint=[2, 2])
    assert newHints.dim == 2
    assert newHints.topHint == [0, 0]
    assert newHints.botHint == [1, 1]
    assert newHints.rightHint == [0, 0]
    assert newHints.leftHint == [2, 2]


def test_init_hints_error_length():
    with raises(LengthFileIncorrect):
        assert HintsData(dim=2,
                         topHint=[0, 0],
                         botHint=[1, 1, 3],
                         rightHint=[2, 2],
                         leftHint=[3, 3]) == LengthFileIncorrect()
    assert HintsData(dim=9,
                     topHint=[1],
                     botHint=[1],
                     rightHint=[1],
                     leftHint=[1]).dim == 1


def test_init_hints_error_chars():
    with raises(NonStandardChars):
        assert HintsData(dim=1,
                         topHint=['a'],
                         botHint=[1],
                         rightHint=[1],
                         leftHint=[1]).dim == NonStandardChars()


def test_init_hints_error_out_range():
    with raises(OutsideRange):
        assert HintsData(dim=1,
                         topHint=[0, 0],
                         botHint=[1, 1],
                         rightHint=[2, 2],
                         leftHint=[3, 3]).dim == OutsideRange()


def test_set_hints_data():
    newHints = HintsData()
    dim = 2
    top = [0, 0]
    bot = [1, 1]
    right = [2, 2]
    left = [0, 0]
    newHints.dim = dim
    newHints.topHint = top
    newHints.botHint = bot
    newHints.rightHint = right
    newHints.leftHint = left
    assert newHints.dim == 2
    assert newHints.topHint == [0, 0]
    assert newHints.botHint == [1, 1]
    assert newHints.rightHint == [2, 2]
    assert newHints.leftHint == [0, 0]
    assert id(newHints.topHint) != id(top)
    assert id(newHints.botHint) != id(bot)
    assert id(newHints.rightHint) != id(right)
    assert id(newHints.leftHint) != id(left)


def test_read_fr_file():
    newHints = HintsData()
    mocker = mock.mock_open(read_data="0 0\n1 1\n2 2\n0 0\n")
    with mock.patch('builtins.open', mocker):
        newHints.getData('fake_dir')
    assert newHints.dim == 2
    assert newHints.topHint == [0, 0]
    assert newHints.botHint == [1, 1]
    assert newHints.rightHint == [2, 2]
    assert newHints.leftHint == [0, 0]


def test_read_fr_file_error_length():
    newHints = HintsData()
    mocker = mock.mock_open(read_data="")
    with mock.patch('builtins.open', mocker):
        with raises(LengthFileIncorrect):
            assert newHints.getData('fake_dir') == LengthFileIncorrect()

    mocker = mock.mock_open(read_data="1\n1\n1\n1\n1\n")
    with mock.patch('builtins.open', mocker):
        with raises(LengthFileIncorrect):
            assert newHints.getData('fake_dir') == LengthFileIncorrect()

    mocker = mock.mock_open(read_data="1 2 3\n1\n1\n1\n")
    with mock.patch('builtins.open', mocker):
        with raises(LengthFileIncorrect):
            assert newHints.getData('fake_dir') == LengthFileIncorrect()


def test_read_fr_file_error_chars():
    newHints = HintsData()
    mocker = mock.mock_open(read_data="0 0\n1 1\n2 a\n3 3\n")
    with mock.patch('builtins.open', mocker):
        with raises(NonStandardChars):
            assert newHints.getData('fake_dir') == NonStandardChars()


def test_read_fr_file_error_out_range():
    newHints = HintsData()
    mocker = mock.mock_open(read_data="0 0\n1 1\n2 2\n3 3\n")
    with mock.patch('builtins.open', mocker):
        with raises(OutsideRange):
            assert newHints.getData('fake_dir') == OutsideRange()
