from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import *

from ..data.term import Term
from .qtdesigner.ui_QTermDisplay import Ui_TermDisplay


class TermEditor(QWidget):
    stopped_editing = pyqtSignal(bool)
    stopped_editing_new_term = pyqtSignal(Term)
    pass
