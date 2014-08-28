from PyQt5.QtCore import pyqtSignal, QMimeData
from PyQt5.QtWidgets import QWidget, QListWidgetItem

from .qtdesigner.ui_QStrBrowser import Ui_QStrBrowser


class StrBrowser(QWidget):
    str_selected = pyqtSignal(str)
    listUpdated = pyqtSignal()
    list_is_empty = pyqtSignal()

    def __init__(self, parent=None):
        #Load QWidget
        super(StrBrowser, self).__init__(parent)
        self._current_str = ""
        self.str_2_item = {}
        self.ui = Ui_QStrBrowser()

        #Setup widgets from Ui_QStrBrowser (qtdesigner made ui):
        self.ui.setupUi(self)
        self.ui.lineEdit.setEnabled(False)
        self.ui.lineEdit.hide()

        #Data:
        self.set_list(list())
        self.ui.listWidget.itemClicked.connect(self._str_selected)
        self.ui.listWidget.setSortingEnabled(True)
        self.listUpdated.connect(self.ui.listWidget.clear)

    @property
    def current_str(self):
        return self._current_str

    def set_list(self, str_list: list):
        self.ui.listWidget.clear()
        for row, string in enumerate(str_list):
            self.str_2_item[string] = \
                QListWidgetItem(string, self.ui.listWidget)

        self.ui.listWidget.sortItems()
        self.listUpdated.emit()

    def _str_selected(self):
        if self.ui.listWidget.currentItem() is not None:
            self._current_str = self.ui.listWidget.currentItem().text()
            self.str_selected.emit(self._current_str)
        else:
            self.list_is_empty.emit()

    def set_current_str(self, string: str):
        if self._current_str == string:
            return
        for item in self.ui.listWidget.items(QMimeData()):
            if item.text == string:
                self.ui.listWidget.setCurrentItem(item)
                break

    def mark_str(self, string: str):
        pass

    def add_a_str(self, string: str):
        self.str_2_item[string] = QListWidgetItem(string, self.ui.listWidget)
        self.ui.listWidget.sortItems()
        self.mark_str(string)

    def rem_a_str(self, string: str):
        self.ui.listWidget.takeItem(
            self.ui.listWidget.indexFromItem(self.str_2_item.pop(string)).row())
        if self.ui.listWidget.count() > 0:
            self.ui.listWidget.setCurrentRow(0)
        self._str_selected()


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    form = StrBrowser()
    form.show()
    app.exec()
