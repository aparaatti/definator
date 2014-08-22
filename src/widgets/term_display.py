from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from ..data.term import Term
from .qtdesigner.ui_QTermDisplay import Ui_TermDisplay


class TermDisplay(QWidget):
    startEditing = pyqtSignal(str, str)
    termSelected = pyqtSignal(str)

    def __init__(self, term: Term=Term(), parent=None):
        super(TermDisplay, self).__init__(parent)
        self.ui = Ui_TermDisplay()
        self.__text = term
        self.__index = 0
        self.ui.setupUi(self)

    @pyqtSlot(Term)
    def set_current_term(self, term: Term):
        self.ui.contentWebView.setContent(term.term_as_html)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = TermDisplay()
    form.show()
    app.exec()
