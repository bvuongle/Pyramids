class WrongDimension(Exception):
    def __init__(self) -> None:
        super().__init__("Dimension of this board is "
                         "different from the one provided.")


class NoSolutionError(Exception):
    def __init__(self):
        super().__init__(
            "This problem has no solution.\n"
            "Please try again by checking the input or resetting the board.")


class OutsideRange(Exception):
    def __init__(self) -> None:
        super().__init__(
            "Input data is out of the allowable range.\n"
            "It should be between 1 and board size."
                         )


class NonStandardChars(Exception):
    def __init__(self):
        super().__init__(
            "The input data contains non-standard characters.\n"
            "Input data can only be natural numbers."
                         )


class LengthFileIncorrect(Exception):
    def __init__(self):
        super().__init__(
            "The length of the input data contained in the file is incorrect."
            "\n(too short or too long for the standard)\n"
            "Please choose another file to continue.")


class InsufficientData(Exception):
    def __init__(self) -> None:
        super().__init__("The input data is not enough"
                         "to perform the operation.")
