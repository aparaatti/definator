from PyQt5.QtWidgets import *
from PyQt5.QtGui import QStandardItemModel

from qtdesigner.ui_QTermList import *

class TermList(QWidget, Ui_QTermList):
    
    def __init__(self, parent=None):
        #Load QWidget
        super(TermList, self).__init__(parent)

        #Setup widgets from Ui_QTermList (qtdesigner made ui):
        self.setupUi(self)
        self.register_add_term_listener(self.addTerm)

        #Data:
        self.populate_list_view(("New", "Old"))

    def populate_list_view(self, str_tuple: tuple):
        """
        :type self: TermList
        """
        for row, name in enumerate(str_tuple):
            self.listWidget.insertItem(row,name)

    def register_add_term_listener(self, methodName):
        self.buttonAddTerm.clicked.connect(methodName)

    def addTerm(self):
        self.listWidget.insertItem(0,"Kissa")

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = TermList()
    form.show()
    app.exec()
