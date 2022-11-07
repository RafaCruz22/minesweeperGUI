from Cell import *
from UserInterface import *
from random import randrange


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
        self.mine = None

        self.placeMine(size)  # place mine on board

        # initialize input and UIput
        self.UI = UserInterface(
            self.field,
            self.numOfMines,
            width=size,
            height=size)

    def placeMine(self, size: int) -> None:
        # puts mine at puesdo random places
        counter = 0
        while counter < self.numOfMines:
            
            x = randrange(0, size-1)
            y = randrange(0, size-1)

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

            winner = self.checkWin()
            
            if self.mine or winner: # or mines == lockedTag:
                self.UI.killTimer()
                self.UI.cellDeactivate()    # disable clicking on the board.
                self.UI.revealAllMines()    # reveal all mine cells

                if self.mine is True:
                    self.UI.buttonImageLost()
                else:
                    self.UI.buttonImageWinner()

                self.UI.master.wait_window(self.UI.board)

            # markedMines = abs((int(self.UI.currentMines.get()) - self.numOfMines))
            # if len(self.UI.board.find_withtag("boxes")) >= 11:
            self.mine = self.playRound() # play a round, get its result


    def checkWin(self): 
        mines = self.UI.board.find_withtag("mine")
        cells = self.UI.board.find_withtag("boxes")
        lockedTag = self.UI.lockedDict.values()

        if len(lockedTag) == 10 and len(cells) == 10:
            for mine in mines: 
                if mine not in lockedTag:
                    return False
            
            return True
        
        return False


    def playRound(self) -> bool:
        """ plays one round
        post: returns True if user has clicked on mine, False otherwise"""
        return True if self.UI.cellValue() == '9' else False

    def resetMinesandCells(self) -> None:
        try:
            self.field.clear()
            self.UI.mineField.clear()
            self.field = self.UI.mineField = [[Cell() for j in range(self.size)] for i in range(self.size)]
            self.UI.gameEnd = False
            self.placeMine(self.size)  # place mine on board
    
        except:
            print('\n--> reset not successful \nSomething went wrong')