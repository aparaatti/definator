from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QListWidgetItem
from PyQt5.QtGui import QColor, QBrush

from .qtdesigner.ui_QStrBrowser import Ui_QStrBrowser


class StrBrowser(QWidget):
    str_selected = pyqtSignal(str)
    listUpdated = pyqtSignal()
    list_is_empty = pyqtSignal()

    def __init__(self, title: str="Str Browser", parent=None):
        #Load QWidget
        super(StrBrowser, self).__init__(parent)
        self._current_str = ""
        self._mark_color = ["White", "Black"]
        self._default_colors = ["Black", "White"]
        self._marked_items = list()
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
        if string and string in self._str_2_item.keys():
            self.ui.listWidget.setCurrentItem(self._str_2_item[string])

    def mark_str(self, string: str):
        item = self._str_2_item[string]
        print("marked")
        item.setForeground(QBrush(QColor(self._mark_color[0])))
        item.setBackground(QBrush(QColor(self._mark_color[1])))
        self._marked_items.append(item)

    def unmark(self):
        for item in self._marked_items:
            item.setForeground(QBrush(QColor(self._default_colors[0])))
            item.setBackground(QBrush(QColor(self._default_colors[1])))
        self._marked_items.clear()

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

    @property
    def mark_color(self):
        return self._mark_color

    @mark_color.setter
    def mark_color(self, str_colors: list):
        if len(str_colors) < 2:
            return
        if QColor(str_colors[0]).isValid() and QColor(str_colors[1]).isValid:
            self._mark_color[0] = str_colors[0]
            self._mark_color[1] = str_colors[1]
