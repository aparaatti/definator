# -*- coding: utf-8 -*-
#
# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QApplication

from ..data.term import Term
from .qtdesigner.ui_QTermDisplay import Ui_TermDisplay


class TermDisplay(QWidget):
    startEditing = pyqtSignal(str, str)
    termSelected = pyqtSignal(str)

    def __init__(self, term: Term=Term(), parent=None):
        super().__init__(parent)
        self.ui = Ui_TermDisplay()
        self.__text = term
        self.__index = 0
        self.ui.setupUi(self)

    @pyqtSlot(Term)
    def set_current_term(self, term: Term):
        self.ui.contentWebView.setContent(term.term_as_html.encode('utf-8'))

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = TermDisplay()
    form.show()
    app.exec()
