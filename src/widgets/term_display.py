from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .qtdesigner.ui_QTermDisplay import *

class TermDisplay(QWidget, Ui_TermDisplay):
    def __init__(self, data, parent=None):
        super(TermDisplay, self).__init__(parent)
        self.__text = data
        self.__index = 0
        self.setupUi(self)

    def setContent(self, html):
        self.termDisplay.setContent(html)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = TermDisplay("kissa")
    form.show()
    app.exec()
