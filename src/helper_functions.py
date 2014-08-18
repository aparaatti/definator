from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

def MakeActionHelper(self, text, helpText, Qshortcut, iconPath=None):
    """ Idea from "Rapid GUI Programming with Python and Qt" by Mark Summerfield
        Published:  Jun 2008
        Publisher:  Prentice Hall """
    if iconPath is not None:
        Action = QAction(QIcon(iconPath), text, self)
    else:
        Action = QAction(text, self)
    Action.setShortcut(QKeySequence.New)
    Action.setToolTip(helpText)
    Action.setStatusTip(helpText)        
    return Action
    
class NotImplementedException(Exception):
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)
