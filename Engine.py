from Cell import *
from InputOutput import *
from random import randint


class Engine():

    def __init__(self, size: int, NumOfMines: int) -> None:
        """
        size is the width and height of the board;
        NumOfMines is the number of the mines on the board;
        limitation: number of mines must be less than half of all the possible slots in the field"""

        assert NumOfMines < 0.5 * size * size

        self.field = [[Cell() for j in range(size)] for i in range(size)]

        self.numOfMines = NumOfMines
        self.minesMarked = None

        self.placeMine(size)  # place mine on board

        # initialize input and output
        self.out = InputOutput(
            self.field,
            self.numOfMines,
            width=size,
            height=size)

    def placeMine(self, size: int) -> None:
        # generate the mines, put them into random places
        counter = 0
        while counter < self.numOfMines:

            x = randint(0, size-1)
            y = randint(0, size-1)

            if self.field[x][y] == '0':
                self.field[x][y].putMine()  # put the mine
                counter += 1  # increase the counter for the mines

                # adjust the numbers of the neighboring slots
                self.adjustCounters(x, y)

    def adjustCounters(self, x: int, y: int) -> None:

        n = len(self.field)

        if x > 0:

            # slot to the left
            self.field[x-1][y].increment()

            if y > 0:  # slot to the left top
                self.field[x-1][y-1].increment()

            if y < n-1:  # slot to the left bottom
                self.field[x-1][y+1].increment()

        if y > 0:  # slot above
            self.field[x][y-1].increment()

        if y < n-1:  # slot below
            self.field[x][y+1].increment()

        if x < n-1:

            # slot to the right
            self.field[x+1][y].increment()

            if y > 0:  # slot to the right top
                self.field[x+1][y-1].increment()

            if y < n-1:  # slot to the right bottom
                self.field[x+1][y+1].increment()

    def playGame(self) -> None:
        """ runs the game """

        self.out.intro()
        self.out.infoBar()  # shows the information bar
        self.out.createBoard()  # creates the minesweeper board
        self.out.printBoard()  # print board to console

        while True:

            result = self.playRound()  # play a round, get its result

            if not result:  # we opened a bomb!
                self.out.announce("lost")  # window with defeat message
                self.out.killTimer()
                break  # end game

            else:
                # player wins if flags are on mines or all nonmine boxes are revealed
                self.minesMarked = abs(
                    (int(self.out.currentMines.get()) - self.numOfMines))

                if self.minesMarked == self.numOfMines:  # all bombs found!
                    self.out.announce('player')  # window with victory message
                    self.out.killTimer()
                    break  # end game

        self.out.showFullBoard()  # reveal all mine cells

        # # keeps main window from closing out
        self.out.board.wait_window(window=self.out.master)

    def playRound(self) -> bool:
        """ plays one round
        post: returns False if user has not clicked on mine, True otherwise"""
        return False if self.out.getInput() == '9' else True
