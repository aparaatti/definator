from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QListWidgetItem
from PyQt5.QtGui import QColor, QBrush, QKeySequence

from .qtdesigner.ui_QStrBrowser import Ui_QStrBrowser
from .key_press_eater import KeyPressEater


class StrBrowser(QWidget):

    """
    This module can show a list of strings sorted alphabetically in increasing order, add and remove strings from
    the shown list, mark strings in it and filter shown strings based on a string entered in an input field shown above
    the list view.

    Module sends signal_undo_event or signal_redo_event when standard undo or redo key combination is
    pressed while string list view or filter input text field is focused.

    """
    str_selected = pyqtSignal(str)
    list_is_empty = pyqtSignal()

    signal_undo_event = pyqtSignal()
    signal_redo_event = pyqtSignal()

    def __init__(self, title: str="Str Browser", parent=None):
        #Load QWidget
        super(StrBrowser, self).__init__(parent)
        self._selected_str = ""
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

        #Hook into undo/redo of term_editor
        self.eventFilter = KeyPressEater(QKeySequence.Undo, self)
        self.eventFilter2 = KeyPressEater(QKeySequence.Redo, self)
        self.ui.listWidget.installEventFilter(self.eventFilter)
        self.ui.listWidget.installEventFilter(self.eventFilter2)
        self.ui.lineEdit.installEventFilter(self.eventFilter)
        self.ui.lineEdit.installEventFilter(self.eventFilter2)

    @pyqtSlot(str)
    def _filter(self, string):
        if string == "":
            self.set_list(list(self._str_2_item.keys()))
        else:
            filtered_list = [filtered_string for filtered_string
                             in self._str_2_item.keys()
                             if filtered_string.lower().startswith(string.lower())]
            self.ui.listWidget.clear()
            for string in filtered_list:
                self._add_a_str(string)

    def set_list(self, str_list: list):
        """
        This method sets the the list of strings to be shown.

        :param str_list: a list that contains str objects
        """
        self.ui.listWidget.clear()
        for string in str_list:
            self._add_a_str(string)

    def get_list(self):
        """
        This returns a str list of currently shown string list.

        :return: a list containing str objects
        """
        return list(self._str_2_item.keys())

    def _add_a_str(self, string: str):
        self._str_2_item[string] = QListWidgetItem(string, self.ui.listWidget)
        self.ui.listWidget.sortItems()

    def _str_selected(self):
        if self.ui.listWidget.currentItem() is not None:
            self._selected_str = self.ui.listWidget.currentItem().text()
            self.str_selected.emit(self._selected_str)
        else:
            self.list_is_empty.emit()

    def set_current_str(self, string: str):
        """
        This method sets the currently selected string.

        :param string: string to highlight
        """
        if self._selected_str == string:
            return
        if string and string in self._str_2_item.keys():
            self.ui.listWidget.setCurrentItem(self._str_2_item[string])
            self._selected_str = string

    def mark_str(self, string: str):
        """
        This method marks the given string in the list.

        :param string: str to highlight
        """
        item = self._str_2_item[string]
        item.setForeground(QBrush(QColor(self._mark_color[0])))
        item.setBackground(QBrush(QColor(self._mark_color[1])))
        self._marked_items.append(item)

    def unmark_all(self):
        """
        This method unmarks all the marked strings.
        """
        for item in self._marked_items:
            item.setForeground(QBrush(QColor(self._default_colors[0])))
            item.setBackground(QBrush(QColor(self._default_colors[1])))
        self._marked_items.clear()

    def add_a_str(self, string: str):
        """
        This method adds a string to be displayed in the list.

        :param string: string to remove
        """
        self._add_a_str(string)

    def rem_a_str(self, string: str):
        """
        This method removes a string from the shown list. The currently selected string is
        set to the first string in the shown list.

        :param string: string to remove
        """
        self.ui.listWidget.takeItem(
            self.ui.listWidget.indexFromItem(self._str_2_item.pop(string)).row())
        if self.ui.listWidget.count() > 0:
            self.ui.listWidget.setCurrentRow(0)
        self._str_selected()

    @property
    def selected_str(self):
        """
        This property has the currently chosen string.

        :return: str
        """
        return self._selected_str

    @property
    def mark_color(self):
        """
        This property returns the colors used in marking a string.

        :return: list containing names of the colors as a string.
        """
        return self._mark_color

    @mark_color.setter
    def mark_color(self, str_colors: list):
        """
        This property sets the color of the marked strings in the list.

        :param str_colors: list that has the foreground color in cell [0] and
            background color in [1]. Possible colors are the ones that QColor object
            can take http://qt-project.org/doc/qt-5/QColor.html
        """
        if len(str_colors) < 2:
            return
        if QColor(str_colors[0]).isValid() and QColor(str_colors[1]).isValid:
            self._mark_color[0] = str_colors[0]
            self._mark_color[1] = str_colors[1]

    def _trigger_event(self, sequence: QKeySequence):
        if sequence is QKeySequence.Undo:
            self.signal_undo_event.emit()

        if sequence is QKeySequence.Redo:
            self.signal_redo_event.emit()
