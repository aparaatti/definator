import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

def make_action_helper(self, text, help_text, Qshortcut, icon_path=None):
    """ Idea from "Rapid GUI Programming with Python and Qt" by Mark Summerfield
        Published:  Jun 2008
        Publisher:  Prentice Hall """
    if icon_path is not None:
        Action = QAction(QIcon(icon_path), text, self)
    else:
        Action = QAction(text, self)
    Action.setShortcut(QKeySequence.New)
    Action.setToolTip(help_text)
    Action.setStatusTip(help_text)
    return Action

