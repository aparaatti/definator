# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from ..data.term import Term
from .qtdesigner.ui_QTermLinks import Ui_QTermLinks


class TermLinks(QWidget):

    linkTermClicked = pyqtSignal()
    unlinkTermClicked = pyqtSignal(str)

    """
    ToDo:
        -Lista näytetään webkitillä. Html generoidaan oliosta.
        -

    Signals do not pass current term, since the module doesn't need to know it.
    """

    def __init__(self, parent=None):
        super(TermLinks, self).__init__(parent)
        self._items = []
        self.__index = 0
        self.ui = Ui_QTermLinks()
        self.ui.setupUi(self)
        self.ui.buttonLinkTerm.clicked.connect(self.__link_term)
        self.ui.buttonUnlinkTerm.clicked.connect(self.__unlink_term)
        self.display_mode()

    def populateTableWidget(self, thingList: list):
        self._items.clear()
        self.ui.tableWidget.setColumnCount(3)
        self.ui.tableWidget.setRowCount(len(thingList)//3+1)
        for thing in thingList:
            self._items.append(QTabWidgetItem(thins, self.ui.tableWidget))

    @pyqtSlot(Term)
    def set_current_term(self, term: Term):
        self._items = term.related_terms
        self.populateTableWidget()

    @pyqtSlot()
    def edit_mode(self):
        self.ui.buttonUnlinkTerm.show()
        self.ui.buttonLinkTerm.show()

    @pyqtSlot()
    def display_mode(self):
        self.ui.buttonUnlinkTerm.hide()
        self.ui.buttonLinkTerm.hide()

    @pyqtSlot()
    def __link_term(self):
        self.ui.linkTermClicked.emit()

    @pyqtSlot()
    def __unlink_term(self):
        self.ui.unlinkTermClicked.emit()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = TermLinker("kissa")
    form.show()
    app.exec()


        #TODO Tästä tulee oma moduulinsa "String linker", sillä edit mode, jossa
        # voi lisätä linkkejä
        #self.ui.verticalLayout.addLayout(link_button_layout)
        #link_button_layout = QHBoxLayout()
        #self.link_terms_button = QPushButton("Link terms", self)
        #self.unlink_terms_button = QPushButton("Unlink terms", self)
        #link_button_layout.addWidget(self.link_terms_button)
        #link_button_layout.addWidget(self.unlink_terms_button)
        ## end
