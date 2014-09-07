# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from ..data.term import Term
from .qtdesigner.ui_QTermLinks import Ui_QTermLinks


class TermLinker(QWidget):

    linkTermsClicked = pyqtSignal()
    unlinkTermsClicked = pyqtSignal()

    """
    Signals do not pass current term, since the module doesn't need to know it.
    """

    def __init__(self, parent=None):
        super(TermLinker, self).__init__(parent)
        self._items = []
        self.__index = 0
        self.ui = Ui_QTermLinks()
        self.ui.setupUi(self)
        self.edit_mode()
        self.ui.tableWidget.setColumnCount(5)

        self.ui.buttonLinkTerm.clicked.connect(self._link_term)
        self.ui.buttonUnlinkTerm.clicked.connect(self._unlink_term)
        #self.ui.verticalLayout.size
        #self.ui.tableWidget.resizeEvent.connect(self.reset_columns_and_rows)
        #self.ui.tableWidget.cellActivated.connect(self._term_selected)

    def _populate_TableWidget(self, str_list: list):
        self._items.clear()
        self.ui.tableWidget.clear()
        for string in str_list:
            self._items.append(QTableWidgetItem(string))

        self.ui.tableWidget.setRowCount(len(str_list)//5+1)
        row = 0
        col = 0
        for item in self._items:
            self.ui.tableWidget.setItem(row, col, item)
            col += 1
            if col > 4:
                col = 0
                row += 1

    @pyqtSlot(Term)
    def set_current_term(self, term: Term):
        self._populate_TableWidget(term.related_terms)

    @pyqtSlot()
    def edit_mode(self):
        self.ui.buttonUnlinkTerm.show()
        self.ui.buttonLinkTerm.show()

    @pyqtSlot()
    def display_mode(self):
        self.ui.buttonUnlinkTerm.hide()
        self.ui.buttonLinkTerm.hide()

    @pyqtSlot()
    def _link_term(self):
        self.linkTermsClicked.emit()

    @pyqtSlot()
    def _unlink_term(self):
        self.unlinkTermsClicked.emit()

    @pyqtSlot()
    def reset_columns_and_rows(self):
        print("resize")
