from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .qtdesigner.ui_QTermLinker import *


class TermLinker(QWidget, Ui_TermLinker):

    linkTermClicked = pyqtSignal()
    unlinkTermClicked = pyqtSignal(str)

    """
    ToDo:
        -Lista näytetään webkitillä. Html generoidaan oliosta.
        -

    Signals do not pass current term, since the module doesn't need to know it.
    """

    def __init__(self, data: tuple, parent=None):
        super(TermLinker, self).__init__(parent)
        self.__data = data
        self.__index = 0
        self.setupUi(self)
        self.buttonLinkTerm.clicked.connect(self.__link_term)
        self.buttonUnlinkTerm.clicked.connect(self.__unlink_term)
        self.populateTableWidget(self.__data)

    def populateTableWidget(self, data):
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(len(data)//3+1)
        self.tableWidget.setItem(0, 0, QTableWidgetItem("Kissa"))
        #parent = self.tableWidget.parent()


    def __link_term(self):
        self.linkTermClicked.emit()

    def __unlink_term(self):
        self.unlinkTermClicked.emit("kizza")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = TermLinker("kissa")
    form.show()
    app.exec()
