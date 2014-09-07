from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QListWidgetItem

from .qtdesigner.ui_QStrBrowser import Ui_QStrBrowser


class StrBrowser(QWidget):
    str_selected = pyqtSignal(str)
    listUpdated = pyqtSignal()
    list_is_empty = pyqtSignal()

    def __init__(self, title: str="Str Browser", parent=None):
        #Load QWidget
        super(StrBrowser, self).__init__(parent)
        self._current_str = ""
        self._str_2_item = {}
        self.ui = Ui_QStrBrowser()

        #Setup widgets from Ui_QStrBrowser (qtdesigner made ui):
        self.ui.setupUi(self)
        self.ui.str_box.setTitle(title)

        #Signals and slots:
        self.ui.listWidget.itemActivated.connect(self._str_selected)
        self.ui.listWidget.setSortingEnabled(True)
        self.ui.lineEdit.textChanged.connect(self._filter)

    @pyqtSlot(str)
    def _filter(self, string):
        if string == "":
            self.set_list(list(self._str_2_item.keys()))
        else:
            filtered_list = [filtered_string for filtered_string
                             in self._str_2_item.keys()
                             if filtered_string.startswith(string)]
            self.ui.listWidget.clear()
            for string in filtered_list:
                self._add_a_str(string)

    def set_list(self, str_list: list):
        self.ui.listWidget.clear()
        for string in str_list:
            self._add_a_str(string)

    def get_list(self):
        return list(self._str_2_item.keys())

    def _add_a_str(self, string: str):
        self._str_2_item[string] = QListWidgetItem(string, self.ui.listWidget)
        self.ui.listWidget.sortItems()

    def _str_selected(self):
        if self.ui.listWidget.currentItem() is not None:
            self._current_str = self.ui.listWidget.currentItem().text()
            self.str_selected.emit(self._current_str)
        else:
            self.list_is_empty.emit()

    def set_current_str(self, string: str):
        if self._current_str == string:
            return
        #items = self.ui.listWidget.items()
        #print(str(items) + " " + type(items))
        print(str(self.ui.listWidget.mimeTypes()))
        self.ui.listWidget.setCurrentItem(self._str_2_item[string])

    def mark_str(self, string: str):
        #TODO this
        pass

    def add_a_str(self, string: str):
        self._add_a_str(string)
        self.mark_str(string)

    def rem_a_str(self, string: str):
        self.ui.listWidget.takeItem(
            self.ui.listWidget.indexFromItem(self._str_2_item.pop(string)).row())
        if self.ui.listWidget.count() > 0:
            self.ui.listWidget.setCurrentRow(0)
        self._str_selected()

    @property
    def current_str(self):
        return self._current_str
