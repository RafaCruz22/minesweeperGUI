from Cell import *
from InputOutput import *
from random import randint


class Game():

    def __init__(self, size, NumOfMines):
        """ 
        size is the width and height of the board;
        NumOfMines is the number of the mines on the board;
        limitation: number of mines must be less than half of all the possible slots in the field"""

        assert NumOfMines < 0.5 * size * size

        self.field = [[Cell() for j in range(size)] for i in range(size)]

        self.numOfmines = NumOfMines
        self.mineList = []

        self.minesMarked = 0
        # the places that we marked as potential mine
        # the counter will be insreased only if the "marked mine" corresponds to the real bomb

        # generate the mines, put them into random places
        k = 0
        counter = 0
        while counter < self.numOfmines:

            x = randint(0, size-1)
            y = randint(0, size-1)

            if self.field[x][y] == '0':
                self.field[x][y].putMine()  # put the mine
                counter += 1  # increase the counter for the mines

                # adjust the numbers of the neighboring slots
                self.adjustCounters(x, y)

        # initialize input and output
        # I decided to have it in one instance, because of the graphics window
        # it will not be a lot of functions, so we can keep it as one class

        width = size
        height = size

        self.out = InputOutput(self.field, self.numOfmines, width, height)
        self.out.intro()

    def adjustCounters(self, x, y):

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

    def playGame(self):
        """ runs one game """

        goodToContinue = True

        self.out.infoBar()  # shows the information bar
        self.out.showBoard()  # show the current board

        while goodToContinue:

            result = self.playRound()  # play a round, get its result

            if result == False:  # we opened a bomb!
                self.out.announce(None)  # popup window with message of defeat
                self.out.showFullBoard()  # show rest of board with locked mine cells
                goodToContinue = False    # end game

            else:
                self.minesMarked = int(self.out.markedMines.get())
                if self.minesMarked == self.numOfmines:  # all bombs found!
                    self.out.showFullBoard()  # show full board with mines locked
                    # popup window with message of victory
                    self.out.announce('player')

                else:  # not all mines found so far, continue playing
                    pass

        # waits for window event to happen
        self.out.board.wait_visibility(window=self.out.board)

    def playRound(self):
        """ plays one round of the game, i.e. takes the input from the user,
        checks what happens, returns whether the game can be continued, or it is the end of the game """

        mineOrNoMine = self.out.getInput()  # either adjancey value or mine

        # its a mine so end game
        if mineOrNoMine == '9':
            return False
        else:  # not a mine continue game
            return True
