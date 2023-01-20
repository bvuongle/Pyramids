# [PIPR Project Z22] - Pyramids
![Python](https://img.shields.io/badge/python-v3.10-blue.svg)
## Description
There is an NxN board on which you can place pyramids with a height of 1 <= H <= N.\
The height informs you how many pyramids can be seen in a row from a given cell of the board. Each column and row of the board contains an indication of how many pyramids can be seen from a given place. In addition, N pyramids of different heights should be placed in each row and column.\
This program solves the problem of building pyramids on a board using [**backtracking algorithm**](https://en.wikipedia.org/wiki/Backtracking).
## Table of Contents
+ [Project Methodology](#project-methodology)
+ [Project Implementation](#project-implementation)
+ [Project Evaluation and Results](#project-evaluation-and-results)
+ [Installation and Setup](#installation-and-setup)
+ [Troubleshooting](#troubleshooting)

## Project Methodology
**Approach to the problem:** this problem can be understood simply by finding the configuration of the NxN board to satisfy two conditions:
1. This configuration is correct for the given conditions of the input data, which are indicators of how many pyramids can be seen from a given position.
2. This configuration is correct for the conditions that each row and each column contains N pyramids of different heights.

We can use **backtracking algorithm** to generate all possible configurations of the NxN board. Each cell in the board can take a value from 1 to N, or it can be understood that for a value of a cell there are N possible cases. There are a total of **N^2^** cells, resulting in the algorithm being able to **generate up to (N^N^)^2^ configurations.**

**For the first condition**, we can divide the above indicators into *4 types*:
1. **topHint:** Hint at the top of the board applies to the columns viewed from the top.
2. **botHint:** Hint at the bottom of the board applies to the columns viewed from the bottom.
3. **rightHint:** Hint on the right side of the board applies to rows viewed from the right.
4. **leftHint:** Hint on the left side of the board applies to rows viewed from the left.

**For the second condition**, we will look at the moment when the algorithm reaches cell (i, j) of the board. By default, cell(i, j) can take values from 1 to N, we call this set **fullSet**. We create two more sets, ***rowSet** - the set of current values on row i* and ***colSet** - the set of current values on column j*. When taking fullSet - rowSet - colSet, we get **remainSet** - set of values that cell(i, j) can actually take without violating the second condition. Because of this condition, the number of configurations that the algorithm can generate is significantly reduced to **N^1^(N-1)^2^(N-2)^3^...1^N^.**

For each board configuration created that satisfies the second condition, we will match it with the values of the four indicator types. If all match, we will return the correct configuration and stop the algorithm. (to avoid the algorithm continue to generate configuration and consume memory)

The algorithm can be further optimized when looking at the cases of indicators.\
When the indicator, for example of type topHint, in the second column, has a value of 1, so the value of the cell in the first row, the second column must have the value N, because there is only one visible pyramid from this position.

| hint:1 => | N | 1..N-1 | 1..N-1 | ... | 1..N-1 |
|-----------|---|--------|--------|-----|--------|

If the value of this indicator is N, then column 2 will definitely take the value (1, 2, 3, ..., N) as we need to arrange so that all pyramids can be seen from this position.

| hint:N => | 1 | 2 | 3 | ... | N |
|-----------|---|---|---|-----|---|

If the value of indicator (X) is in the range (2, N-1), we can also create conditions to ensure that the condition is satisfied, for example a pyramid of height N cannot be on the line 1, 2, 3 to N-X.

Call this conditional board **condBoard**, with each cell being **a list** containing the values that **cell(i, j)** can take, by default **this list** has an **initial value of [1, ..., N]**. Combined with the condition in the set **remainSet**, we say a cell(i, j) can take value X if X is present in remainSet and condBoard[i][j]
	
## Project Implementation
### Map of the project
+ `icon` - *Folder containing icons for GUI*
+ `input` - *Folder containing pre-prepared input data sets for testing*
+ `ui` - *Folder containing files saved from QtDesigner*
+ `test` - *Folder containing test files using pytest*
### `board.py`
Board class is used to store the data of a square board with a specified dimension, contains 2 attributes:

It also contains getter and setter methods for these parameters. Another important method is used to fill the cells in the "board" property with the value "value". This method will update the value of the "board" property and return None:

&emsp;&emsp;&emsp;&emsp;`(method) fillBoardWithValue(self: Self@Board, value: Any) -> None`

### `hints.py`
The HintsData class contains input data, which are indicators of how many pyramids can be seen from a given position, as mentioned above.




### `board_resolver.py`
### `condition_analysis.py`
### `main.py`

## Project Evaluation and Results
## Installation and Setup
`$ pip install -r requirements.txt`
## Troubleshooting
## Requirements
The documentation should include documentation of the most important functions including their arguments and return values. Additionally documentation should clarify how to run the program and in case there are some requirements they should be listed as well.

The algorithm will go to each cell from left to right, top to bottom, using a recursive method. As it reaches each cell, it tries to put values in that cell. When it reaches the last cell of the table, it will call the method to check the accuracy of the result. If the result is not correct, it will go back to the previous cell and try the new configuration.