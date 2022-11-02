from Cell import *
from UserInterface import *
from random import randint


class Engine():

    def __init__(self, size: int, NumOfMines: int) -> None:
        """
        size is the width and height of the board;
        NumOfMines is the number of the mines on the board;
        limitation: number of mines must be less than half of all the possible slots in the field"""

        assert NumOfMines < 0.5 * size * size

        self.field = [[Cell() for j in range(size)] for i in range(size)]

        self.size = size
        self.numOfMines = NumOfMines

        self.placeMine(size)  # place mine on board

        # initialize input and UIput
        self.UI = UserInterface(
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
                counter += 1                # increase mines count

                # adjust the adjucency values of the neighboring slots
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
        self.UI.introWindow()  # created window with intro message
        self.UI.gameBar()      # shows the information bar
        self.UI.createBoard()  # creates the minesweeper board
        self.UI.printBoard()   # print board to console

        while True:
            if self.UI.gameEnd:
                self.resetMinesandCells()

            mine = self.playRound()          # play a round, get its result
                
            markedMines = abs((int(self.UI.currentMines.get()) - self.numOfMines))

            if mine or markedMines == self.numOfMines:
                self.UI.killTimer()
                    
                # disable clicking on the board.
                self.UI.cellDeactivate()
                self.UI.revealAllMines()  # reveal all mine cells

    def playRound(self) -> bool:
        """ plays one round
        post: returns True if user has clicked on mine, False otherwise"""
        return True if self.UI.cellValue() == '9' else False

    def resetMinesandCells(self) -> None:
        try:
            # self.UI.board.unbind("<Button-1>")
            self.field.clear()
            self.UI.mineField.clear()
            self.field = self.UI.mineField = [[Cell() for j in range(self.size)] for i in range(self.size)]
            self.UI.gameEnd = False
            self.placeMine(self.size)  # place mine on board
    
        except:
            print('\n--> reset not successful \nSomething went wrong')