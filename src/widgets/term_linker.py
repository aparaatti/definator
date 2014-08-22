# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .qtdesigner.ui_QTermLinker import *


class TermLinker(QWidget):

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
        self.ui = Ui_TermLinker();
        self.ui.setupUi(self)
        self.ui.buttonLinkTerm.clicked.connect(self.__link_term)
        self.ui.buttonUnlinkTerm.clicked.connect(self.__unlink_term)
        self.populateTableWidget(self.__data)

    def populateTableWidget(self, data):
        self.ui.tableWidget.setColumnCount(3)
        self.ui.tableWidget.setRowCount(len(data)//3+1)
        self.ui.tableWidget.setItem(0, 0, QTableWidgetItem("Kissa"))
        #parent = self.tableWidget.parent()


    def __link_term(self):
        self.ui.linkTermClicked.emit()

    def __unlink_term(self):
        self.ui.unlinkTermClicked.emit("kizza")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = TermLinker("kissa")
    form.show()
    app.exec()
