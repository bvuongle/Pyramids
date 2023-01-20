# [PIPR Project Z22] - Pyramids
![Python](https://img.shields.io/badge/python-v3.10-blue.svg)
## **Description**
There is an NxN board on which you can place pyramids with a height of 1 <= H <= N.\
The height informs you how many pyramids can be seen in a row from a given cell of the board. Each column and row of the board contains an indication of how many pyramids can be seen from a given place. In addition, N pyramids of different heights should be placed in each row and column.\
This program solves the problem of building pyramids on a board using [**backtracking algorithm**](https://en.wikipedia.org/wiki/Backtracking).
## Table of Contents
+ [Project Methodology](#project-methodology)
+ [Project Implementation](#project-implementation)
+ [Project Evaluation and Results](#project-evaluation-and-results)
+ [How to use GUI?](#how-to-use-gui)
+ [What if I don't like using the GUI?](#what-if-i-dont-like-using-the-gui)
+ [Troubleshooting](#troubleshooting)

## **Project Methodology**
**Approach to the problem:** this problem can be understood simply by finding the configuration of the NxN board to satisfy two conditions:
1. This configuration is correct for the given conditions of the input data, which are indicators of how many pyramids can be seen from a given position.
2. This configuration is correct for the conditions that each row and each column contains N pyramids of different heights.

We can use **backtracking algorithm** to generate all possible configurations of the NxN board. Each cell in the board can take a value from 1 to N, or it can be understood that for a value of a cell there are N possible cases. There are a total of **N<sup>2</sup>** cells, resulting in the algorithm being able to **generate up to N<sup>N<sup>2</sup></sup> configurations.**

**For the first condition**, we can divide the above indicators into *4 types*:
1. **topHint:** Hint at the top of the board applies to the columns viewed from the top.
2. **botHint:** Hint at the bottom of the board applies to the columns viewed from the bottom.
3. **rightHint:** Hint on the right side of the board applies to rows viewed from the right.
4. **leftHint:** Hint on the left side of the board applies to rows viewed from the left.

**For the second condition**, we will look at the moment when the algorithm reaches cell (i, j) of the board. By default, cell(i, j) can take values from 1 to N, we call this set **fullSet**. We create two more sets, ***rowSet** - the set of current values on row i* and ***colSet** - the set of current values on column j*. When taking fullSet - rowSet - colSet, we get **remainSet** - set of values that cell(i, j) can actually take without violating the second condition. Because of this condition, the number of configurations that the algorithm can generate is significantly reduced to:

**N<sup>1</sup>(N-1<sup>2</sup>(N-2)<sup>3</sup>...1<sup>N</sup>.**

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
	
## **Project Implementation**
### Map of the project
+ `.sphinx` - *Folder containing data to generate documentation from sphinx*
+ `docs` - *Folder containing documentation (in HTML) and test coverage report (in HTML)*
+ `icon` - *Folder containing icons for GUI*
+ `input` - *Folder containing pre-prepared input data sets for testing*
+ `pyramids` - *Folder containing source code for the project*
+ `test` - *Folder containing test files using pytest*
+ `ui` - *Folder containing files saved from QtDesigner*

### Documentation
Documentation for the project, describing the functionality and composition of the methods can be found [here](docs/documentation/index.html).

Note: If the link doesn't work, you can find the documentation at docs/documentation/index.html

Note: You can create new documentation file with the following command:

sphinx-build -b html ./.sphinx ./docsGen

New documentation file will be locate in /docsGen/index.html

### The core of the project
+ Backtracking algorithm

This method will go to each cell from left to right, top to bottom, using a recursive method. As it reaches each cell, it tries to put values in that cell. When it reaches the last cell of the table, it will call the method to check the accuracy of the result. If the result is not correct, it will go back to the previous cell and try the new configuration.
```python
def backtracking(self, row: int, col: int):
        if row == self.curBrd.dim-1 and col > self.curBrd.dim-1:
            if self.checkResultWithCond():
                self.flag = 1
                return self.curBrd
            else:
                return None
        if row < self.curBrd.dim-1 and col > self.curBrd.dim-1:
            row += 1
            col = 0
        remSet = set(self.getRow(self.curBrd.board, row)).union(
            set(self.getCol(self.curBrd.board, col)))
        for value in range(1, self.curBrd.dim+1):
            if value in self.condBrd.board[row][col] and value not in remSet:
                self.curBrd.board[row][col] = value
                self.backtracking(row, col+1)
                if self.flag == 1:
                    return self.curBrd
                self.curBrd.board[row][col] = 0
```

+ Result check method

This method splits the existing configuration data and contrasts it with the input data to ensure that the correct result is found.
```python
def checkResultWithCond(self) -> bool:
        for idx in range(0, self.hints.dim):
            topCond = self.hints.topHint[idx]
            botCond = self.hints.botHint[idx]
            rightCond = self.hints.rightHint[idx]
            leftCond = self.hints.leftHint[idx]

            tmpRow = []
            for row in range(0, self.curBrd.dim):
                tmpRow.append(self.curBrd.board[row][idx])
            visibleTop = self.numVisiblePyramids(tmpRow)
            visibleBot = self.numVisiblePyramids(tmpRow[::-1])

            tmpCol = []
            for col in range(0, self.curBrd.dim):
                tmpCol.append(self.curBrd.board[idx][col])
            visibleRight = self.numVisiblePyramids(tmpCol)
            visibleLeft = self.numVisiblePyramids(tmpCol[::-1])

            if (visibleTop != topCond and topCond != 0) or \
                    (visibleBot != botCond and botCond != 0) or \
                    (visibleRight != rightCond and rightCond != 0) or \
                    (visibleLeft != leftCond and leftCond != 0):
                return False
            else:
                continue
        return True
```

## **Project Evaluation and Results**
The algorithm is evaluated by writing tests using the pytest library. The results of the evaluation show that the algorithm works as designed with the reliability of the test set evaluated on the coverage index (which is 100%).\
Information about coverage reports can be found [here](docs/coverage/index.html).

## **Requirements**
The project requires some external libraries to be installed, which can be easily done via the command:
```python
$ pip install -r requirements.txt
```

## **How to use GUI?**
At the command line, navigate to the pyramids directory, then use the command:
```python
python main.py
```
At the main interface, you can select Start to get started right away. Or you can read the user manual in the Help section. In addition, you can learn about project information in the About section.

At the problem solving interface, select the size of the board you want in the **Board Size** section. Then you can enter hint values directly into the 4 board top, bottom, right, left of the center board, hit enter to confirm the value. After making sure the input data is correct, press **Run**, the problem results will be displayed in the center board. Press **Reset** to reset the board and solve another problem.

If you are tired of typing everything, you can import the input file using the **Open...** button, the data will show up in the GUI for you. If you want to show the answer to the math problem to your friends, the program will have a **Save** button for you, the data file after successfully saved will be displayed.

## **What if I don't like using the GUI?** 
You can run the program without using the GUI via the command:
```python
python main.py -i [input_file] -o [output_file]
```

## **Troubleshooting**
During use, the program may report some errors and I still don't know why it happened.
When opening a file or saving a file, after you select a file, even if the program loads successfully, it will ask you to select the file again, this will repeat 3 times. Rest assured after 3 times like that it will work properly :).\
It seems to only happen when you run the program from the command line, on Visual Studio Code everything is normal. In addition, running the program on the command line will not display the icon. \
**This is not a bug, this is a feature.** :o

*Author: Binh Vuong Le Duc - 20/01/2023*


