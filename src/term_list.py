from PyQt5.QtWidgets import QWidget, QMessageBox

from qtdesigner.ui_QTermList import *


class TermList(QWidget, Ui_QTermList):
    def __init__(self, parent=None):
        #Load QWidget
        super(TermList, self).__init__(parent)

        #Setup widgets from Ui_QTermList (qtdesigner made ui):
        self.setupUi(self)

        #Data:
        self.populate_list_view(("New", "Old"))

    def populate_list_view(self, str_tuple: tuple):
        for row, name in enumerate(str_tuple):
            self.listWidget.insertItem(row, name)

    def register_add_term_listener(self, method):
        self.buttonAddTerm.clicked.connect(method)

    def register_term_selected_listener(self, method):
        self.listWidget.itemDoubleClicked.connect(method)

    def selected(self):
        item = self.sender()
        #print(dir(self.sender()))
        #print(item.currentItem().text())
        QMessageBox.information(self,item.currentItem().text(), item.currentItem().text())


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    form = TermList()
    form.show()
    app.exec()
