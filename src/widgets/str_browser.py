from PyQt5.QtCore import pyqtSignal, QMimeData
from PyQt5.QtWidgets import QWidget

from .qtdesigner.ui_QStrBrowser import Ui_QStrBrowser


class StrBrowser(QWidget):
    strSelected = pyqtSignal(str)
    listUpdated = pyqtSignal()

    def __init__(self, parent=None):
        #Load QWidget
        super(StrBrowser, self).__init__(parent)
        self._current_str = ""
        self.str_list = []
        self.ui = Ui_QStrBrowser()

        #Setup widgets from Ui_QStrBrowser (qtdesigner made ui):
        self.ui.setupUi(self)
        self.ui.lineEdit.setEnabled(False)
        self.ui.lineEdit.hide()

        #Data:
        self.set_list(["New", "Old"])
        self._populate_list_view()
        self.ui.listWidget.itemDoubleClicked.connect(self.__str_selected)
        self.listUpdated.connect(self.ui.listWidget.clear)

    @property
    def current_str(self):
        return self._current_str

    def set_list(self, str_list: list):
        self.str_list = str_list
        self.listUpdated.emit()
        self._populate_list_view()

    def _populate_list_view(self):
        for row, string in enumerate(self.str_list):
            self.ui.listWidget.insertItem(row, string)

    def __str_selected(self):
        self._current_str = self.ui.listWidget.currentItem().text()
        self.strSelected.emit(self._current_str)

    def set_current_str(self, string: str):
        if self._current_str == string:
            return
        for item in self.ui.listWidget.items(QMimeData()):
            if item.text == string:
                self.ui.listWidget.setCurrentItem(item)
                break

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    form = StrBrowser()
    form.show()
    app.exec()
