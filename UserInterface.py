from tkinter import *
import platform
import tkinter


class UserInterface:
    """ handles all the graphics for minesweeper"""

    def __init__(self, board, numOfmines, width, height):
        """ width is the width of the graphics window, in pixels;
        height is the height of the graphics window, in pixels;
        board is the reference to the board from the game;
        """

        self.mineField = board
        self.mines = numOfmines
        self.size = width
        self.gameEnd = False
        self.os = platform.system() # gets the OS currently running

        # ----  Main Tkinter Frame  ------------------------------
        self.master = Tk()  # STARTS EVENT LOOP
        self.master.title("Minesweeper")
        self.master.iconbitmap("./assets/favicon.ico")
        self.master.resizable(False, False)
        self.master.withdraw()

        # ----  Main Frame  --------------------------------------
        self.mainFrame = LabelFrame(self.master)
        self.mainFrame.grid()

        # ----  Game Information Bar Frame  ----------------------
        self.barFrame = Frame(
            self.mainFrame,
            width=(width * 52),
            height=(height * 8.6),
            relief=RIDGE,
            borderwidth=6,
            bg='gray30')

        self.barFrame.grid(padx=10, pady=10)

        # -------  Reset Button  -----------------------------------
        self.resetButton = Button(self.barFrame)

        # -------  Images  ----------------------------------------
        self.images = [PhotoImage(file="./assets/smile1.png"),
                       PhotoImage(file="./assets/smile2.png"),
                       PhotoImage(file="./assets/smile3.png"),
                       PhotoImage(file="./assets/smile4.png"),
                       PhotoImage(file="./assets/flag.png"),
                       PhotoImage(file="./assets/mine.png")]

        # ----  Board Game Frame  ---------------------------------
        self.boardWidth = self.boardHeight = (width * 50)
        self.boardFrame = Frame(
            self.mainFrame,
            width=self.boardWidth,
            height=self.boardHeight,
            relief=RIDGE,
            borderwidth=6,
            bg='gray30')

        self.boardFrame.grid(padx=10, pady=10)

        # ----  Create A Canvas For The Board  ---------------------
        self.board = Canvas(
            self.boardFrame,
            width=self.boardWidth,
            height=self.boardHeight)

        self.board.grid()

        # ----  Variable To Return To Game Function  ----------------
        self.value = StringVar(self.master)  # adjanacey value of box clicked

        # number of mines marked initialized to numOfMines
        self.currentMines = StringVar(self.barFrame)
        self.currentMines.set(self.mines)

        # list of locked cell ids
        self.lockedList = []

        # keeps track of seconds passed
        self.timer = StringVar(self.barFrame)
        self.timer.set(0)

        # holds reference to .after() method
        self.after_id = None

        # set's first and last cell box on board
        self.firstBox, self.lastBox = None, None

        # ----  Activates Cell Button Binds ------------------------
        self.cellActive()

    def introWindow(self) -> None:
        """ a separate introduction to the game window with instructions """

        introWindow = Toplevel()  # new window for intro message
        introWindow.iconbitmap("./assets/favicon.ico")

        # doesn't allow the window to be resized
        introWindow.resizable(False, False)

        # string var object to set intro message
        introMessage = StringVar(introWindow)
        introText = Message(introWindow,
                            relief=RIDGE,
                            textvariable=introMessage,
                            borderwidth=6,
                            bg='gray30',
                            fg='snow',
                            font=("New Time Roman", 15, "bold", "italic"))  # Message widage
        
        # start button to begin minesweeper
        startButton = Button(
            introWindow,
            relief=RIDGE,
            text="Start Game")  # button to start game

        startButton.bind(
            "<Button-1>", lambda event: self.startGame(introWindow))

        introMessage.set(self.introMessages())
        introText.pack()
        startButton.pack()

    def introMessages(self) -> None:
        """ introduction message to player
        post: return the message """

        # message to show player
        message = ("Welcome To Minesweeper".rjust(60)
                   + "\nTo Play:"
                   + "\n** Left clicking a cell will show how many "
                   + "mines are adjacent to that cell."

                   + "\n\n** Right clicking a cell will lock the cell "
                   + "making the cell un-clickabe and displaying"
                   + " an Red Flag to show the cell is locked. Decreasing "
                   + "the amount of mines by 1.\n\t\t(Left Top Value in Game Window).\n"

                   + "\n** Double Right click a cell to unlock. Removing the flag and increase mine count."
                   + "\n** Click the smiley at anytime to reset the game."
                   + "\n" + "-" * 99

                   + "\nTo Win:"
                   + "\n** User must find all mines by placing a flag on a cell "
                   + "that they think holds a mine. If all cells are revealed "
                   + "and all mines are found, then the player wins the game.\n"
                   + "-->  Click Button below to Start Game  <--".rjust(65))

        return message  # returns the intro message

    def startGame(self, introWindow):
        """ starts the game """
        introWindow.destroy()   # destories the intro window
        self.master.deiconify()

    def gameBar(self) -> None:
        """ creates an bar containing the games information, ex. Label for mines marked,
        button to reset game, and label to keep track of time
        post: draws information bar on self.master"""

        # -----  Mine Marked Counter ----------------------------------------
        # creates marked mine label
        markedMineCount = Label(
            self.barFrame,
            textvariable=self.currentMines,
            relief=SUNKEN,
            font=20)

        markedMineCount.place(relx=.02, rely=.3, relwidth=.1, relheight=.5)

        # -------  Starts Button With Standard Image   --------------------------------------------------------
        # creates reset button
        self.resetButton['image'] = self.images[0]
        self.resetButton.place(relx=.43, rely=.15)
        self.resetButton.bind(
            '<Button-1>', lambda event: self.restoreGame(event, self.images[2]))
        # ^^ : binding event handle with button click to reset game

        # -------  Time Keeper  -------------------------------------------------------------------------------
        # creates label for time elapse
        timeKeeper = Label(
            self.barFrame,
            textvariable=self.timer,
            relief=SUNKEN,
            font=20)

        timeKeeper.place(relx=.877, rely=.3, relwidth=.1, relheight=.5)

    def createBoard(self) -> None:
        """ creates the entire board """
        self.drawLines()
        self.placeAdjacency()
        self.createCellBox()

    def drawLines(self) -> None:
        """creates harizonal and vertical line on the canvas"""

        # ---  Creates the lines for the board   -------------------------------------
        # creates harizonal lines on self.board
        for x in range(0, self.boardWidth, 50):
            self.board.create_line(
                x, 0, x, self.boardHeight, fill='black', width=2)

        # creates vertical line on self.board
        for y in range(0, self.boardHeight, 50):
            self.board.create_line(0, y, self.boardWidth,
                                   y, fill='black', width=2)

    def placeAdjacency(self) -> None:
        """ Places adjacency values on the canvas """

        # places adjacency values in center of check cell box
        row = 0  # cell box row
        column = 0  # cell box column
        for rowX in range(25, self.boardWidth, 50):  # row to place adjacency value
            # column to place adjacency value
            for columnY in range(25, self.boardWidth, 50):

                # retrives value at row = x ( from 25 to (self.height - 50))
                # column = y (from 25 to (self.height - 50))
                mineOnField = str(self.mineField[row][column])

                # creates the text objects and places them in center of each future box
                if mineOnField == '9':
                    self.mineField[row][column].visible = True

                    self.board.create_image(
                        rowX, columnY, image=self.images[5])

                else:
                    if mineOnField != "0":
                        self.board.create_text(rowX, columnY, text=mineOnField, font=(
                            "New Time Roman", 20, "italic"))

                column += 1
                if column == self.size:
                    column = 0

            row += 1
            if row == self.size:
                row = 0

    def createCellBox(self) -> None:

        columnDone = 0  # keeps track of how many coulmns have been created
        x1, x2 = 0, 50  # initial croods for creating cell box

        while(columnDone != self.size):
            y1, y2 = 0, 50
            rowDone = 0

            # true if rows created isn't equal to size of board
            while(rowDone != self.size):
                # creates all the cell boxes
                id = self.board.create_rectangle(
                    x1, y1, x2, y2,
                    fill='gray50',
                    outline='gray17',
                    width=2.5,
                    tags="boxes")

                # tags each box with adjacney value or mine if its a mine
                self.board.addtag_withtag(
                    f"{self.mineField[columnDone][rowDone]}", id)

                if self.mineField[columnDone][rowDone].isVisible():
                    # tags each box not a non-mine as visible
                    self.board.addtag_withtag("mine", id)

                # tags each cell box with its lock status at creation
                self.board.addtag_withtag(
                    f"{self.mineField[columnDone][rowDone].isLocked()}", id)

                # center coordinates of each box
                self.board.addtag_withtag(f"{x1 + 25},{y1 + 25}", id)

                # moves bottom right points of square which makes up the box
                y1 += 50  # y1 to next column point
                y2 += 50  # y2 to next column point

                rowDone += 1
            # moves top left points of square which makes up the box to next point
            x1 += 50
            x2 += 50

            columnDone += 1

        # assigns first and last cell box on board
        self.firstBox = self.board.find_withtag("boxes")[0]
        self.lastBox = self.board.find_withtag("boxes")[-1]

    def showCell(self, x : int , y : int, firstBox : tkinter, lastBox : tkinter) -> None:
        """shows the cell with coordinates x and y
        pre: mouse x coords , y mouse coords
        post: deletes the cell box click by user"""

        # assigns id of box that user clicked on
        boxx = self.board.find_closest(x, y)[0]

        self.startTimer()

        # visual indicator that a cell has been clicked
        self.resetButton["image"] = self.images[1]

        # makes sure user is clicking on a cellbox
        if boxx >= firstBox and boxx <= lastBox:

            # checks if cellbox user cliked is not in lockedList
            if boxx not in self.lockedList:

                # assigns the cellbox click adjancey value to value
                value = self.board.gettags(boxx)[1]

                # sets self.value i.e currect value of cellbox clicked
                self.value.set(value)

                # removes clicked cell box from self.board (canvas)
                self.board.delete(self.board.find_closest(x, y))

                # delete all adjacent 0's

        # resets infor frame button to default image
        self.resetButton.after(500, self.buttonImageToggle)

    def lock(self, x : int, y : int, firstBox : tkinter, lastBox : tkinter) -> None:
        """ event handler for locked cell when right clicked
        pre: mouse x croods , mouse y croods
        post: lock the cell and place X in the box """

        # allows for cell to be locked as long as the game hasn't ended
        # if not self.gameEnd:
        cellID = self.board.find_closest(x, y)[0]

        if cellID >= firstBox and cellID <= lastBox:

            # checks if clicked id is in list of locked boxes
            if cellID not in self.lockedList:
                # gets and splits the croods which is taged on each cell
                cellCoordinatesX, cellCoordinatesY = self.board.gettags(
                    cellID)[-2].split(",")

                # places a flag on cell user wants locked
                textID = self.board.create_image(
                    cellCoordinatesX,
                    cellCoordinatesY,
                    image=self.images[4])

                # cell not in locked list so append to list
                self.lockedList.append(textID)

                # self.lockedDict[f"{cellID}"] = textID

                # decrease self.mineMarked by 1
                mineCount = int(self.currentMines.get())
                self.currentMines.set(mineCount - 1)

    def unlock(self, x : int, y : int):
        """ event handler for unlocking cell when double right clicked
        pre: mouse x croods , mouse y croods
        post: unlocks the cell and removes X  """

        # game hasn't ended so allow unlocking of cell
        # if not self.gameEnd:
        cellID = self.board.find_closest(x, y)[0]
        if cellID in self.lockedList:
            self.board.delete(cellID)
            self.lockedList.remove(cellID)  # removes cell box

            # increase mine count by 1
            newMineCount = str(int(self.currentMines.get()) + 1)
            self.currentMines.set(newMineCount)  # changes mine count

    def cellValue(self) -> StringVar:
        """ get the input from the user;
        returns the coordinates and True (if a "keyboard" event, i.e. lock the cell, it is a potential bomb)
        otherwise False"""
        self.board.wait_variable(self.value)
        return self.value.get()  # return True if mine, False otherwise

    def buttonImageToggle(self):
        self.resetButton["image"] = self.images[0]

    def revealAllMines(self) -> None:
        '''Reveals all mines on the board'''

        # deletes all cells that are mines
        for id in self.board.find_withtag("mine"):
            self.board.delete(id)

    def startTimer(self) -> None:
        ''' starts game timer when user has clicked a cell or placed a flag'''
        if str(self.timer.get()) == '0':
            self.after_id = self.master.after(1, self.increaseTimer)

    def increaseTimer(self) -> None:
        ''' increases timer 1 second every second once timer has started'''
        seconds = (int(self.timer.get()) + 1)
        self.timer.set(seconds)
        self.after_id = self.master.after(1000, self.increaseTimer)

    def killTimer(self) -> None:
        '''stops the timer'''
        if self.after_id != None:
            self.master.after_cancel(self.after_id)
    
    def restoreGame(self, event: EventType, image: tkinter.PhotoImage) -> None:
        """ handles bar button being clicked
        pre: "<Button-1>", the image to display
        post: restarts game after"""

        event.widget["image"] = image   # displays the image in button
        event.widget.update()
        self.gameEnd = True
        self.killTimer()

        # # waits a seconds before restarting windows
        event.widget.after(1000)
        self.restartGame()

    def restartGame(self) -> None: 
        self.board.destroy()
        self.timer.set(0)
        self.value.set(None)

        # holds reference to .after() method
        self.after_id = None
        self.buttonImageToggle()
        
        # number of mines marked initialized to numOfMines
        self.currentMines.set(self.mines)

        self.lockedList.clear()  # list of locked cell ids

        self.board = Canvas(
            self.boardFrame,
            width=self.boardWidth,
            height=self.boardHeight)
        
        self.board.grid()
        self.createBoard()
        self.cellActive()
        self.printBoard() # for testing 

    def cellActive(self) -> None:  
        #  left click to reveal cell
        self.board.bind(
            "<Button-1>",
            lambda event: self.showCell(event.x, event.y, self.firstBox, self.lastBox))

        if self.os == "Darwin":
            # right click to place flag on cell
            self.board.bind(
                "<Button-2>",
                lambda event: self.lock(event.x, event.y, self.firstBox, self.lastBox))

            # double right click to remove flag
            self.board.bind(
                "<Double-Button-2>",
                lambda event: self.unlock(event.x, event.y)) 
        
        elif self.os == "Windows": 
            # right click to place flag on cell
            self.board.bind(
                "<Button-3>",
                lambda event: self.lock(event.x, event.y, self.firstBox, self.lastBox))

            # double right click to remove flag
            self.board.bind(
                "<Double-Button-3>",
                lambda event: self.unlock(event.x, event.y)) 
    
    def cellDeactivate(self) -> None:

        self.board.unbind("<Button-1>")
        self.board.unbind("<Button-2>")
        self.board.unbind("<Button-3>")

    def printBoard(self) -> None:
        """ prints the board to the console"""

        # prints the boards to console
        print()
        for i in range(0, self.size):
            row = ""
            for j in range(0, self.size):
                row += str(self.mineField[j][i]) + '  '

            print("\t", row)
