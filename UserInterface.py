from tkinter import *
import platform


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
        self.topBound = []
        self.bottomBound = []

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
                       PhotoImage(file="./assets/mine.png"),
                       PhotoImage(file="./assets/box.png")]

        # ----  Board Game Frame  ---------------------------------
        self.boardWidth = self.boardHeight = (width * 50)
        self.boardFrame = Frame(
            self.mainFrame,
            relief=RIDGE,
            borderwidth=6,
            bg='gray30')

        self.boardFrame.grid(padx=5, pady=5)
        
        # ----  Create A Canvas For The Board  ---------------------
        self.board = Canvas(
            self.boardFrame,
            width=self.boardWidth - 3,
            height=self.boardHeight - 3)

        self.board.grid(padx=5, pady=5)

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
        lineLen = 99 if self.os == "Windows" else 89
        # message to show player
        message = ("-" * lineLen + "\n"
                +"Welcome To Minesweeper".rjust(lineLen - 10)
                + "\n" + "-" * lineLen

                + "\nTo Play:"
                + "\n* Left-clicking a cell will show how many "
                + "mines are adjacent to that cell."

                + "\n* Right-clicking a cell will lock the cell "
                + "making the cell un-clickable and displaying a "
                + "Red Flag to show the cell is locked. Also decreasing "
                + "the number of mines by 1." 
                
                +"\n* Mine count is kept in the box to the left of "
                +"the smiley button."
                
                +"\n* Time lapsed is kept in the box to the right of " 
                +"the smiley button."

                + "\n* Double Right-click a cell to unlock. It will remove the " 
                +"placed flag and increase the mine count."
                + "\n* Click the smiley at any time to reset the game."
                
                + "\n\nTo Win:"
                + "\n* The player must find all mines by placing a flag on a "
                + "cell that they think holds a mine. The player wins the game "
                + "if all cells are revealed and all mines are found."
                + "\n" + "-" * lineLen + "\n"
                + "-->  Click the button below to start the game  <--".rjust(lineLen - 2)
                + "\n" + "-" * lineLen)

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
        
        # ---  Creates the lines for the board   ----------------------
        # creates top, bottom, left, and right board lines
        boarderLines = [[0,0,500,0], [0,500,500,500], [0,0,0,500], [500,0,500,500]]
        for coords in boarderLines:
            x1 , y1 = coords[0] , coords[1]
            x2 , y2 = coords[2] , coords[3]
            self.board.create_line(x1, y1, x2, y2, fill='black', width=10)

        # creates harizonal lines on self.board
        for x in range(0, self.boardWidth,50):
            self.board.create_line(x, 0, x, self.boardHeight, fill='black', width=2)

        # creates vertical line on self.board
        for y in range(0, self.boardHeight,50):
            self.board.create_line(0, y, self.boardWidth, y, fill='black', width=1)

    def placeAdjacency(self) -> None:
        """ Places adjacency values on the canvas """

        # places adjacency values in center of check cell box
        row, column = 0 , 0 # cell box row , column
        for rowX in range(25, self.boardWidth, 50):  # row to place adjacency value
            # column to place adjacency value
            for columnY in range(25, self.boardWidth, 50):

                mineOnField = str(self.mineField[row][column])

                # creates the text objects and places them in center of each future box
                if mineOnField == '9':
                    self.mineField[row][column].visible = True

                    self.board.create_image(rowX, columnY, image=self.images[5])

                elif mineOnField != "0":
                    self.board.create_text(rowX, columnY, text=mineOnField, font=(
                        "Helvetica", 20, "italic"))

                column += 1
                if column == self.size: column = 0

            row += 1
            if row == self.size: row = 0

    def createCellBox(self) -> None:
        ''' Creates the cells on the board and tags each cell with 
        adjacency values, if its a mine, if the cell is clocked, 
        and it's coordination '''

        x1 = 25 # initial croods for creating cell box
        for x in range(10):
            y1 = 25
            # true if rows created isn't equal to size of board
            for y in range(10):
                # creates all the cell boxes
                id = self.board.create_image(
                    x1, y1,
                    image=self.images[6],
                    tags="boxes")

                # tags each box with adjacney value or mine if its a mine
                self.board.addtag_withtag(
                    f"{self.mineField[x][y]}", id)

                if self.mineField[x][y].isVisible():
                    # tags each box not a non-mine as visible
                    self.board.addtag_withtag("mine", id)

                # tags each cell box with its lock status at creation
                self.board.addtag_withtag(
                    f"{self.mineField[x][y].isLocked()}", id)

                # center coordinates of each box
                self.board.addtag_withtag(f"{x1},{y1}", id)

                y1 += 50 
            x1 += 50

        # assigns first and last cell box on board
        self.firstBox = self.board.find_withtag("boxes")[0]
        self.lastBox = self.board.find_withtag("boxes")[-1]

        self.createBounds() # creates the top & bottom bounds

    def createBounds(self) -> None: 
        ''' creates the upper and lower bounder for revealing cells recursively '''
        upperBound = self.firstBox
        lowerBound = self.lastBox

        for x in range(10):
            self.topBound.append(upperBound)
            self.bottomBound.append(lowerBound)
            upperBound += 10
            lowerBound -= 10

    def showCell(self, x : int , y : int, firstBox : Canvas.create_rectangle, lastBox : Canvas.create_rectangle) -> None:
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
                # assigns the cellbox click adjancey value to self.value
                self.value.set(self.board.gettags(boxx)[1])

                self.revealMore(boxx)
        
        if self.value.get() != '9':
            # resets infor frame button to default image
            self.resetButton.after(500, self.buttonImageDefault)

    def revealMore(self, cellBox : id) -> None:
        ''' recursively reveals neiborging cell that have 0 adjancecy 
        along with a line of adjacent cells'''

        # assures cellBox exist
        if cellBox in self.board.find_withtag("boxes"):
            cellValue = int(self.board.gettags(cellBox)[1])
            
            if self.board.gettags(cellBox)[-1] == "locked":
                return

            if cellValue == 0 and self.board.gettags(cellBox)[-1] != "locked": 
                self.board.delete(cellBox) # reveals the cell
                self.revealMore(cellBox - 10) # check left
                self.revealMore(cellBox + 10) # check right

                if cellBox not in self.topBound:    
                    self.revealMore(cellBox - 1)  # check up
                    self.revealMore(cellBox - 11) # check upLeft
                    self.revealMore(cellBox + 9) # check upRight
                
                if cellBox not in self.bottomBound:     
                    self.revealMore(cellBox + 1)  # check down
                    self.revealMore(cellBox - 9)  # check downLeft
                    self.revealMore(cellBox + 11)  # check downRight

            if cellValue != 9: 
                self.board.delete(cellBox) # reveals the cell
                return 

    def lock(self, x : int, y : int, firstBox : Canvas.create_rectangle, lastBox : Canvas.create_rectangle) -> None:
        """ event handler for locked cell when right clicked
        pre: mouse x croods , mouse y croods
        post: lock the cell and place X in the box """

        # retrieves the cell ID that user has clicked on
        cellID = self.board.find_closest(x, y)[0]
        
        if cellID >= firstBox <= lastBox:
            if cellID not in self.lockedList:
                # retrieve and splits the croods which is taged on each cell
                coordX, coordY = self.board.gettags(cellID)[3].split(",")

                # places a flag on the cell the user clicked to be locked
                flagID = self.board.create_image(coordX, coordY,
                    image=self.images[4],
                    tags=cellID)

                # cell not in locked list; append to list
                self.lockedList.append(flagID)

                # self.lockedDict[f"{cellID}"] = textID
                
                # adds a lock tag to the cell 
                self.board.addtag_withtag(f"{flagID}", cellID)
                self.board.addtag_withtag("locked", cellID)
                
                # decrease self.mineMarked by 1
                mineCount = int(self.currentMines.get())
                self.currentMines.set(mineCount - 1)

    def unlock(self, x : int, y : int):
        """ event handler for unlocking cell when double right clicked
        pre: mouse x croods , mouse y croods
        post: unlocks the cell and removes X  """

        # game hasn't ended so allow unlocking of cell
        flagID = self.board.find_closest(x, y)[0]

        if flagID in self.lockedList:
            cellID = self.board.gettags(flagID)[-2]

            self.board.delete(flagID)   
            self.lockedList.remove(flagID)  # removes cell box

            # removes the "locked" tag from cell
            self.board.dtag(cellID, "locked")
            self.board.dtag(cellID, f"{flagID}")

            # increase mine count by 1
            newMineCount = str(int(self.currentMines.get()) + 1)
            self.currentMines.set(newMineCount)  # changes mine count

    def cellValue(self) -> StringVar:
        """ get the input from the user;
        returns the coordinates and True (if a "keyboard" event, i.e. lock the cell, it is a potential bomb)
        otherwise False"""
        self.board.wait_variable(self.value)
        return self.value.get()  # return True if mine, False otherwise

    def buttonImageDefault(self):
        ''' sets smiley button to it's default image'''
        self.resetButton["image"] = self.images[0]

    def buttonImageLost(self): 
        ''' sets smiley button to a losing image'''
        self.resetButton["image"] = self.images[3]

    def revealAllMines(self) -> None:
        '''Reveals all mines on the board'''

        # deletes all cells that are mines
        for id in self.board.find_withtag("mine"):
            if self.board.gettags(id)[-1] != "locked":
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
    
    def restoreGame(self, event: EventType, image: PhotoImage) -> None:
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
        '''Restarts game, resets all values to intital state and recreated the board'''
        self.board.destroy()
        self.timer.set(0)
        self.value.set(None)

        # holds reference to .after() method
        self.after_id = None
        self.buttonImageDefault()
        
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
        '''Activates the  mouse click binding depending on operating system.'''

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
        ''' deactivates all mouse click bindings'''

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

            print("   ", row)
        print()