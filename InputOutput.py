from tkinter import *
import time
import os


class InputOutput:
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

        self.master = Tk()  # STARTS EVENT LOOP
        self.master.title("Minesweeper")
        self.master.iconbitmap("./assets/favicon.ico")
        self.master.resizable(False, False)

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

        # -------  Quit Button  -----------------------------------
        self.quitButton = Button(self.barFrame)

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

        self.lockedList = []  # list of locked cell ids: list limited to number of mines in field
        self.lockedDict = dict()  # dictionary of "X" textId & locked cell ids (to remove "X")

        # keeps track of seconds passed
        self.startTimer = StringVar(self.barFrame)
        self.startTimer.set(0)

    def intro(self):
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

        startButton = Button(
            introWindow,
            relief=RIDGE,
            text="Start Game")  # button to start game

        startButton.bind(
            "<Button-1>", lambda event: self.startGame(introWindow))

        introMessage.set(self.introMessages())
        introText.pack()
        startButton.pack()

    def introMessages(self):
        """ introduction message to player
        post: return the message """

        # message to show player
        message = ("Welcome To Minesweeper".rjust(60)
                   + "\nTo Play:"
                   + "\n** Left clicking a cell will show how many "
                   + "mines are adjacent to the cell."

                   + "\n\n** Right clicking a cell will lock the cell "
                   + "making the cell un-clickabe and displaying"
                   + " an 'X' to show the cell is locked. Decreasing "
                   + "the amount of mines by 1.\n\t\t(Left Top Value in Game Window).\n"

                   + "\n** Double Right click a cell to unlock."
                   + "\n** Click the smiley at anytime to quit game."
                   + "\n" + "-" * 99

                   + "\nTo Win:"
                   + "\n** User must find all the mines by locking a cell "
                   + "that they think hold a mine. If all cells    are revealed "
                   + "and all mines are found, then the player wins the game"
                   + " and a message will display to winner\n\n"
                   + "-->  Click Button below to Start Game  <--".rjust(65))

        return message  # returns the intro message

    def startGame(self, introWindow):
        """ starts the game """
        self.master.deiconify()  # draws the minesweeper game window
        introWindow.destroy()   # destories the intro window

    def infoBar(self):
        """ creates an bar containing the games information, ex. Label for mines marked,
        button to quit game, and label to keep track of time
        post: draws bar on self.master"""

        # -----  Mine Marked Counter ----------------------------------------
        # creates marked mine label
        mineMarkedCount = Label(
            self.barFrame,
            textvariable=self.currentMines,
            relief=SUNKEN,
            font=20)

        mineMarkedCount.place(relx=.02, rely=.3, relwidth=.1, relheight=.5)

        # -------  Starts Button With Standard Image   --------------------------------------------------------
        # creates quit button
        self.quitButton['image'] = self.images[0]
        self.quitButton.place(relx=.43, rely=.15)
        self.quitButton.bind(
            '<Button-1>', lambda event: self.quit(event, self.images[2]))
        # ^^ : binding event handle with button click to quit game

        # -------  Time Keeper  -------------------------------------------------------------------------------
        # creates label for time elapse
        timeCount = Label(
            self.barFrame,
            textvariable=self.startTimer,
            relief=SUNKEN,
            font=20)

        timeCount.place(relx=.877, rely=.3, relwidth=.1, relheight=.5)

        self.printBoard()

    def quit(self, event, image):
        """ handles bar button being clicked
        pre: "<Button-1>", the image to display
        post: destory's self.master ending game after five milliseconds """

        event.widget["image"] = image   # displays the image in button
        event.widget.update()

        # waiting a five seconds before destorying windows
        event.widget.after(5000)
        os.abort()

    def buttonImageToggle(self):
        self.quitButton["image"] = self.images[0]

    def showBoard(self):
        """ creates the entire board, first lines horizontal then vertical lines, then
            place adjacency value in center of each box, finally creates the cell boxes
            top left (x1,y1) & bottom right (x2,y2) tagging each object created with:
            1. adjacency vlaue,
            2. visible box or not (mine not visible),
            3. is box is locked or not """

        # ---  Creates the lines for the board   -------------------------------------
        # creates harizonal lines on self.board
        for x in range(0, self.boardWidth, 50):
            self.board.create_line(
                x, 0, x, self.boardHeight, fill='black', width=2)

        # creates vertical line on self.board
        for y in range(0, self.boardHeight, 50):
            self.board.create_line(0, y, self.boardWidth,
                                   y, fill='black', width=2)

        # ---  Places The Adjacency Values On The Board   -----------------------------
        # places adjacency values in center of check cell box
        row = 0  # cell box row
        column = 0  # cell box column
        for rowX in range(25, self.boardWidth, 50):  # row to place adjacency value
            # column to place adjacency value
            for columnY in range(25, self.boardWidth, 50):

                # retrives value at row = x ( from 25 to (self.height - 50))
                # column = y (from 25 to (self.height - 50))
                mineOnField = str(self.mineField[row][column])

                # if value is not '9' adjancey value then set self.visible to True
                if mineOnField != '9':
                    self.mineField[row][column].visible = True

                # creates the text objects and places them in center of each future box
                if mineOnField == '9':

                    self.board.create_image(
                        rowX, columnY, image=self.images[5])

                else:
                    self.board.create_text(rowX, columnY, text=mineOnField, font=(
                        "New Time Roman", 20, "italic"))

                column += 1
                if column == self.size:
                    column = 0

            row += 1
            if row == self.size:
                row = 0

        # ---  Creates The Cell Boxes ---------------------------------------------------
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

                # tags each box not a non-mine as visible
                self.board.addtag_withtag(
                    f"{self.mineField[columnDone][rowDone].isVisible()}", id)

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

    def announce(self, winner):
        """ announces whether the player has won or lost """

        window = Toplevel()  # new window for winner message
        window.iconbitmap("./assets/favicon.ico")
        window.resizable(False, False)

        msg = StringVar(window)

        message = Label(window,
                        relief=RIDGE,
                        textvariable=msg,
                        width=20,
                        height=17,
                        borderwidth=6,
                        bg='gray30',
                        font=("New Time Roman", 20, "bold", "italic"))  # Message widget

        message.pack()  # packs to winner window

        # sets the text to display in label
        if winner == 'player':
            msg.set("\n!! YOU HAVE WON !!" * 15)
        else:
            msg.set("\n!! YOU HAVE LOST !!" * 15)

    def showCell(self, x, y, firstBox, lastBox):
        """shows the cell with coordinates x and y
        pre: mouse x coords , y mouse coords
        post: deletes the cell box click by user"""

        # assigns id of box that user clicked on
        boxx = self.board.find_closest(x, y)[0]

        # visual indicator that a cell has been clicked
        self.quitButton["image"] = self.images[1]

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
        self.quitButton.after(200, self.buttonImageToggle)

    def lock(self, x, y, firstBox, lastBox):
        """ event handler for locked cell when right clicked
        pre: mouse x croods , mouse y croods
        post: lock the cell and place X in the box """

        # allows for cell to be locked as long as the game hasn't ended
        if not self.gameEnd:
            cellID = self.board.find_closest(x, y)[0]

            if cellID >= firstBox and cellID <= lastBox:

                # checks if clicked id is in list of locked boxes
                if cellID not in self.lockedList:
                    # gets and splits the croods which is taged on each cell
                    cellCoordinatesX, cellCoordinatesY = self.board.gettags(
                        cellID)[-2].split(",")

                    # displays a flag on the cell box user wants locked
                    textID = self.board.create_image(
                        cellCoordinatesX,
                        cellCoordinatesY,
                        image=self.images[4])

                    # cell not in locked list so append to list
                    self.lockedList.append(textID)

                    # self.lockedDict[f"{cellID}"] = textID

                    # decrease self.mineMarked by 1
                    mineCount = int(self.currentMines.get())
                    self.currentMines.set(str(mineCount - 1))

    def unlock(self, x, y):
        """ event handler for unlocking cell when double right clicked
        pre: mouse x croods , mouse y croods
        post: unlocks the cell and removes X  """

        # game hasn't ended so allow unlocking of cell
        if not self.gameEnd:
            cellID = self.board.find_closest(x, y)[0]
            if cellID in self.lockedList:
                self.board.delete(cellID)
                self.lockedList.remove(cellID)  # removes cell box

                # increase mine count by 1
                newMineCount = str(int(self.currentMines.get()) + 1)
                self.currentMines.set(newMineCount)  # changes mine count

    def getInput(self):
        """ get the input from the user;
        returns the coordinates and True (if a "keyboard" event, i.e. lock the cell, it is a potential bomb)
        otherwise False"""

        # get's first and last cell box on board
        firstBox = self.board.find_withtag("boxes")[0]
        lastBox = self.board.find_withtag("boxes")[-1]

        # left click to reveal cell
        self.board.bind(
            "<Button-1>",
            lambda event: self.showCell(event.x, event.y, firstBox, lastBox))

        # right click to place flag on cell
        self.board.bind(
            "<Button-3>",
            lambda event: self.lock(event.x, event.y, firstBox, lastBox))

        # double right click to remove flag
        self.board.bind(
            "<Double-Button-3>",
            lambda event: self.unlock(event.x, event.y))

        # waits for user to click on a unlocked cell
        self.board.wait_variable(self.value)

        return self.value.get()  # return True no mine, false if mine

    def printBoard(self):
        """ prints the board to the console"""

        # prints the boards to console
        print()
        for i in range(0, self.size):
            row = ""
            for j in range(0, self.size):
                row += str(self.mineField[j][i]) + '  '

            print("\t", row)

    def showFullBoard(self):
        # game has ended do not allow locking of cells
        self.gameEnd = True

        # gameover so disable clicking on boxes
        # boxes left are mines
        self.board.unbind("<Button-1>")

        # deletes all cell's that are not mines
        boxList = self.board.find_withtag("True")
        for id in boxList:
            self.board.delete(id)
