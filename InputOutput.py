from tkinter import *
import time


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
        self.master.resizable(False, False)

        # ----  Main Frame  -----------------------------------------------------------------------------------------------------------------------
        self.mainFrame = LabelFrame(self.master)
        self.mainFrame.grid()

        # ----  Game Information Bar Frame  -------------------------------------------------------------------------------------------------------
        self.barWidth = (width * 52)
        self.barHeight = (height * 8.6)
        self.barFrame = Frame(self.mainFrame, width=self.barWidth,
                              height=self.barHeight, relief=RIDGE, borderwidth=6, bg='gray30')
        self.barFrame.grid(padx=10, pady=10)

        # ----  Board Game Frame  -----------------------------------------------------------------------------------------------------------------
        self.boardWidth = self.boardHeight = (width * 50)
        self.boardFrame = Frame(self.mainFrame, width=self.boardWidth,
                                height=self.boardHeight, relief=RIDGE, borderwidth=6, bg='gray30')
        self.boardFrame.grid(padx=10, pady=10)

        # ----  Create A Canvas For The Board  ----------------------------------------------------------------------------------------------------
        self.board = Canvas(
            self.boardFrame, width=self.boardWidth, height=self.boardHeight)
        self.board.grid()

        # ----  Variable To Return To Game Function  ----------------------------------------------------------------------------------------------
        self.value = StringVar(self.master)  # adjanacey value of box clicked
        # number of mines marked initialized to numOfMines
        self.markedMines = StringVar(self.barFrame)
        self.lockedList = []  # list of locked cell ids: list limited to number of mines in field
        self.lockedDict = dict()  # dictionary of "X" textId & locked cell ids (to remove "X")
        # keeps track of seconds passed
        self.startTimer = StringVar(self.barFrame)
        self.startTimer.set(0)

    def intro(self):
        """ a separate introduction to the game window with instructions """

        self.master.withdraw()  # keeps the game window from being drawn
        introWindow = Toplevel()  # new window for intro message
        # doesn't allow the window to be resized
        introWindow.resizable(False, False)

        # string var object to set intro message
        introMessage = StringVar(introWindow)
        introText = Message(introWindow, relief=RIDGE,
                            textvariable=introMessage)  # Message widage
        introText["borderwidth"] = 6  # makes border width 6
        introText["bg"] = 'gray30'   # makes background color gray
        introText["fg"] = "snow"
        # sets the messsages font, size, and style
        introText["font"] = ("New Time Roman", 15, "bold", "italic")

        startButton = Button(introWindow, relief=SUNKEN,
                             text="Start Game")  # button to start game
        # handles the button being clicked
        startButton.bind(
            "<Button-1>", lambda event: self.startGame(event, introWindow))
        # sets the messages to the string var assigned at start of function
        introMessage.set(self.introMessages())

        # packs both widgets
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

    def startGame(self, event, introWindow):
        """ starts the game """
        self.master.deiconify()  # draws the minesweeper game window
        introWindow.destroy()   # destories the intro window

    def infoBar(self):
        """ creates an bar containing the games information, ex. Label for mines marked,
        button to quit game, and label to keep track of time 
        post: draws bar on self.master"""

        # -----  Mine Marked Counter --------------------------------------------------------------------------
        # creates marked mine label
        mineMarkedCount = Label(self.barFrame, height=4,
                                textvariable=self.markedMines)
        mineMarkedCount['relief'] = SUNKEN
        mineMarkedCount['font'] = 20
        mineMarkedCount.place(relx=.02, rely=.3, relwidth=.1, relheight=.5)
        # sets the number of mines marked, count starts at total mines
        self.markedMines.set(0)

        # -------  Quit Button  -------------------------------------------------------------------------------
        button_normal = PhotoImage(file="./assets/icon.gif")  # standard image
        button_quitClick = PhotoImage(file="./assets/icon_2.gif")  # quit image
        button_click = PhotoImage(
            file="./assets/icon_click.gif")  # click box image

        # -------  Starts Button With Standard Image   --------------------------------------------------------
        # creates quit button
        quitButton = Button(self.barFrame, image=button_normal)
        quitButton.photo = button_normal
        quitButton.place(relx=.43, rely=.15)
        quitButton.bind(
            '<Button-1>', lambda event: self.doubleClickToQuit(event, button_quitClick))
        # ^^ : binding event handle with double button click to quit game

        # -------  Time Keeper  -------------------------------------------------------------------------------
        # creates label for time elapse
        timeCount = Label(self.barFrame, textvariable=self.startTimer)
        timeCount['relief'] = RAISED
        timeCount.place(relx=.877, rely=.3, relwidth=.1, relheight=.5)

        self.printBoard()

    def doubleClickToQuit(self, event, image):
        """ handles bar button being clicked 
        pre: "<Button-1>", the image to display 
        post: destory's self.master ending game after a few milliseconds """

        button = event.widget
        button["image"] = image   # displays the image in button
        button.update_idletasks()
        button.unbind_all(event)
        # waiting a few miliseconds before calling closeAll()
        button.after(10000)
        self.closeAll()

    def showCell(self, x, y):
        """shows the cell with coordinates x and y 
        pre: mouse x coords , y mouse coords
        post: deletes the cell box click by user"""

        # gets list of object ids created with tag "boxes"
        # assigns id of the first cell box created
        firstBox = self.board.find_withtag("boxes")[0]
        # assigns id of last cell box created
        lastBox = self.board.find_withtag("boxes")[-1]
        # assigns id of box that user clicked on
        boxx = self.board.find_closest(x, y)[0]

        # makes sure user is clicking on a cellbox
        if boxx >= firstBox and boxx <= lastBox:
            # checks if cellbox user cliked is in lockedList
            # if it is do not delete the cellbox
            if boxx not in self.lockedList:

                # assigns the cellbox click adjancey value to value
                value = self.board.gettags(boxx)[1]
                # sets self.value i.e currect value of cellboxed clicked
                self.value.set(value)
                # removes clicked cell box from self.board (canvas)
                self.board.delete(self.board.find_closest(x, y))

    def showBoard(self):
        """ creates the entire board, first lines horizontal then vertical lines, then 
            place adjacency value in center of each box, finally creates the cell boxes
            top left (x1,y1) & bottom right (x2,y2) tagging each object created with: 
            1. adjacency vlaue, 
            2. visible box or not (mine not visible), 
            3. is box is locked or not """

        # ---  Creates the lines for the board   --------------------------------------------------------------
        # creates harizonal lines on self.board
        for x in range(0, self.boardWidth, 50):
            self.board.create_line(
                x, 0, x, self.boardHeight, fill='black', width=2)

        # creates vertical line on self.board
        for y in range(0, self.boardHeight, 50):
            self.board.create_line(0, y, self.boardWidth,
                                   y, fill='black', width=2)

        # ---  Places The Adjacency Values On The Board   --------------------------------------------------------------
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
                self.board.create_text(rowX, columnY, text=mineOnField, font=(
                    "New Time Roman", 20, "italic"))

                column += 1  # go to next column
                if column == self.size:  # column equals the size of board
                    column = 0  # column complete reset or next row

            row += 1  # row completed reset for next row
            if row == self.size:  # row completed equal the size of board
                row = 0  # reset row counter to 0 for new row

        # ---  Creates The Cell Boxes -------------------------------------------------------------------------------
        columnDone = 0  # keeps track of how many coulmns have been created
        x1, x2 = 0, 50  # initial croods for creating cell box
        # true if columns created isn't equal to size of board
        while(columnDone != self.size):
            # initial y croods for cell box (bottom right point of square)
            y1, y2 = 0, 50
            rowDone = 0  # keeps track of rows created
            # true if rows created isn't equal to size of board
            while(rowDone != self.size):
                # creates all the cell boxes
                id = self.board.create_rectangle(
                    x1, y1, x2, y2, fill='gray50', outline='gray17', width=2.5, tags="boxes")
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

                rowDone += 1  # for each row completed increace by 1

            # moves top left points of square which makes up the box
            x1 += 50  # x1 to next row point
            x2 += 50  # x2 to next row point

            columnDone += 1  # for each column created increase by 1

    def announceWin(self):
        """ announces the win """
        # create popup window displaying that a player has won

        winnerWindow = Toplevel()  # new window for winner message
        # makes the winner message widget the top widget
        winnerWindow.lower(belowThis=None)
        # doesn't allow the window to be resized
        winnerWindow.resizable(False, False)

        winnerMSG = StringVar(winnerWindow)
        winnerMessage = Label(winnerWindow, relief=RIDGE,
                              textvariable=winnerMSG)  # Message widget
        winnerMessage["width"] = 40   # sets width of winnerMessage Label
        winnerMessage["height"] = 18  # sets height of winnerMessage Label
        winnerMessage["borderwidth"] = 6  # makes border width 6
        winnerMessage["bg"] = 'gray30'   # makes background color gray
        # sets the messsages font, size, and style
        winnerMessage["font"] = ("New Time Roman", 20, "bold", "italic")

        winnerMessage.pack()  # packs to winner window

        # sets the text to display in label
        winnerMSG.set("\n!! YOU HAVE WON !!" * 15)

    def announceDefeat(self):
        """ announced the defeat """
        # create popup window displaying that player has lost

        defeatWindow = Toplevel()  # new window for lossing message
        # makes the defeat message widget the top widget
        defeatWindow.lower(belowThis=None)
        # doesn't allow the window to be resized
        defeatWindow.resizable(False, False)

        defeatMSG = StringVar(defeatWindow)
        defeatMessage = Label(defeatWindow, relief=RIDGE,
                              textvariable=defeatMSG)  # Message widget
        defeatMessage["width"] = 40   # sets width of defeatMessage Label
        defeatMessage["height"] = 18  # sets height of defeatMessage Label
        defeatMessage["borderwidth"] = 6  # makes border width 6
        defeatMessage["bg"] = 'gray30'   # makes background color gray
        # sets the messsages font, size, and style
        defeatMessage["font"] = ("New Time Roman", 20, "bold", "italic")

        defeatMessage.pack()  # packs to defeat window

        # sets the text to display in label
        defeatMSG.set("\n!! YOU HAVE LOST !!" * 15)

    def closeAll(self):
        """ closes the graphics window """

        return self.master.destroy()

    def lock(self, x, y):
        """ event handler for locked cell when right clicked
        pre: mouse x croods , mouse y croods 
        post: lock the cell and place X in the box """

        firstBox = self.board.find_withtag(
            "boxes")[0]  # id of first box created
        lastBox = self.board.find_withtag(
            "boxes")[-1]  # id of last box created

        # allows for cell to be locked as long as the game hasn't ended
        if self.gameEnd == False:
            cellID = self.board.find_closest(
                x, y)[0]  # user clicked cell box id
            # checks if id clicked is in list of created boxes
            if cellID >= firstBox and cellID <= lastBox:
                # checks if clicked id is in list of locked boxes
                # true as long as id is in locked list and self.minesMarked !> self.mines
                if cellID not in self.lockedList and len(self.lockedList) != self.mines:
                    # only places "X" if the cell box is a mine
                    if self.board.gettags(cellID)[1] == "9":
                        # displays an "X" on the cell box user wants locked
                        # gets and splits the croods which is taged on each cell
                        lockTextCroods = self.board.gettags(
                            cellID)[-2].split(",")
                        textID = self.board.create_text(lockTextCroods[0], lockTextCroods[1], text="x", font=(
                            "New Time Roman", 50, "italic"), tags="x")
                        # cell not in locked list so append to list
                        self.lockedList.append(cellID)
                        self.lockedDict[f"{cellID}"] = textID
                        # decrease self.mineMarked by 1
                        newMineCount = str(int(self.markedMines.get()) + 1)
                        # set value to self.markedMines
                        self.markedMines.set(newMineCount)

    def unlock(self, x, y):
        """ event handler for unlocking cell when double right clicked
        pre: mouse x croods , mouse y croods 
        post: unlocks the cell and removes X  """

        firstBox = self.board.find_withtag(
            "boxes")[0]  # id of first box created
        lastBox = self.board.find_withtag(
            "boxes")[-1]  # id of last box created

        # game hasn't ended so allow unlocking of cell
        if self.gameEnd == False:

            # if self.board.find_closest(x,y)
            cellID = self.board.find_closest(
                x, y)[0]  # user clicked cell box id

            # checks if clicked id is in list of locked boxes
            # true as long as id is in locked list and self.minesMarked !> self.mines
            if cellID >= firstBox and cellID <= lastBox:
                # if the clicked cell box is in cell box list
                if cellID in self.lockedList:
                    self.board.delete(self.lockedDict[f"{cellID}"])
                    self.lockedList.remove(cellID)  # remove cell box
                    # increase mine count by 1
                    newMineCount = str(int(self.markedMines.get()) - 1)
                    self.markedMines.set(newMineCount)  # changes mine count

    def getInput(self):
        """ get the input from the user;
        returns the coordinates and True (if a "keyboard" event, i.e. lock the cell, it is a potential bomb)
        otherwise False"""

        # click button 1 to show cell
        # show cell binding
        self.board.bind(
            "<Button-1>", lambda event: self.showCell(event.x, event.y))
        # click button 3 to lock cell
        # locks cell binding
        self.board.bind(
            "<Button-3>", lambda event: self.lock(event.x, event.y))
        # double click button 3 to unlock cell
        # unlock cell binding
        self.board.bind("<Double-Button-3>",
                        lambda event: self.unlock(event.x, event.y))

        # waits for cell value to be updated (Call to self.showCell(mouse.x,mouse.y))
        # waits for user to click on a unlocked cell
        self.board.wait_variable(self.value)

        return self.value.get()  # return True no mine, false if mine

    def printBoard(self):
        """ prints the board to the console"""

        # prints the boards to console
        for i in range(0, self.size):
            row = ""
            for j in range(0, self.size):
                row += str(self.mineField[j][i]) + '  '

            print(row)

        print("\n\n")

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
