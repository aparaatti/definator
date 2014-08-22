from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import *

from ..data.term import Term
from .qtdesigner.ui_QTermDisplay import Ui_TermDisplay


class TermEditor(QWidget):
    stopEditing = pyqtSignal(bool)
    pass
