class Cell:

  def __init__(self,value = '0'):
    self.value = '0' 
    
    # use char since it takes only one byte, wereas int will take at least 4 bytes.
    # '0' stands for 0 bombs around
    # '1' stands for 1 bomb around
    # '2' stands for 2 bombs around
    # ...
    # '8' stands for 8 bombs around
    # '9' stands for the bomb in this place

    self.visible  = False # if False, don't show the cell
    # otherwise, show it
 
    self.locked = False # we can mark a cell as a potential bomb to lock
    # from accidental clicking on it

  def getValue(self):
    """ returns the value of the cell/slot as a char """

    return self.value

  def show(self):
    """ make the cell/slot visible to the player """

    self.visible = True

  def increment(self):
    """ increase the cell's value by 1 """

    self.value = chr(ord(self.value)+1)

  def __str__(self):
    """ display the value of the cell """

    return self.value

  def __eq__(self,other):
    """ compares two cell objects for equality;
      other is supposed to be a string/char"""

    return self.value == other

  def putMine(self):

    self.value = '9'

  def lockUnlock(self):
    """ changes the state from Locked to Unlocked and vice versa """

    self.locked = True if self.locked == False else False

  def isLocked(self):
    """ returns True if the cell is locked, and False otherwise """

    return self.locked

  def isVisible(self):

    return True if self.visible == True else False

  def isMine(self):

    return True if self.value == '9' else False

  def setVisible(self,visible):
    self.visible = visible

