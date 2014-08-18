from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

from .qtdesigner.ui_QTermList import *


class TermList(QWidget, Ui_QTermList):
    termChanged = pyqtSignal(str, str)
    addTermPressed = pyqtSignal()

    def __init__(self, parent=None):
        #Load QWidget
        super(TermList, self).__init__(parent)

        #Setup widgets from Ui_QTermList (qtdesigner made ui):
        self.setupUi(self)
        self.lineEdit.setEnabled(False)

        #Data:
        self.populate_list_view(("New", "Old"))
        self.listWidget.itemDoubleClicked.connect(self.__change_term)

    def populate_list_view(self, str_tuple: tuple):
        for row, name in enumerate(str_tuple):
            self.listWidget.insertItem(row, name)

    def register_add_term_listener(self, method):
        self.buttonAddTerm.clicked.connect(method)

    def __change_term(self):
        self.termChanged.emit("TermList", self.listWidget.currentItem().text())

    def current_term(self):
        return self.listWidget.currentItem().text()

    def set_current_term(self, term):
        for item in self.listWidget.items():
            if item.text == term:
                self.listWidget.setCurrentItem(item)
                break

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    form = TermList()
    form.show()
    app.exec()
