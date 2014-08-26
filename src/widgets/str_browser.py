from PyQt5.QtCore import pyqtSignal, QMimeData
from PyQt5.QtWidgets import QWidget

from .qtdesigner.ui_QStrBrowser import Ui_QStrBrowser


class StrBrowser(QWidget):
    str_selected = pyqtSignal(str)
    listUpdated = pyqtSignal()

    def __init__(self, parent=None):
        #Load QWidget
        super(StrBrowser, self).__init__(parent)
        self._current_str = ""
        self.str_dict = {}
        self.ui = Ui_QStrBrowser()

        #Setup widgets from Ui_QStrBrowser (qtdesigner made ui):
        self.ui.setupUi(self)
        self.ui.lineEdit.setEnabled(False)
        self.ui.lineEdit.hide()

        #Data:
        self.set_list(list())
        self._populate_list_view()
        self.ui.listWidget.itemDoubleClicked.connect(self.__str_selected)
        self.listUpdated.connect(self.ui.listWidget.clear)

    @property
    def current_str(self):
        return self._current_str

    def set_list(self, str_list: list):
        for item in str_list:
            self.str_dict[item] = 0

        self.listUpdated.emit()
        self._populate_list_view()

    def _populate_list_view(self):
        string_list = list(self.str_dict.keys())
        string_list.sort()
        self.ui.listWidget.clear()
        for row, string in enumerate(string_list):
            self.ui.listWidget.insertItem(row, string)
            self.str_dict[string] = row

    def __str_selected(self):
        self._current_str = self.ui.listWidget.currentItem().text()
        self.str_selected.emit(self._current_str)

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
        self.str_dict[string] = 0
        self._populate_list_view()
        self.mark_str(string)

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    form = StrBrowser()
    form.show()
    app.exec()
