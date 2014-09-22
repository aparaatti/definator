# -*- coding: utf-8 -*-
#
# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
import collections
import logging

from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from PyQt5.QtGui import QBrush, QColor, QPalette

from .qtdesigner.ui_QKeyList import Ui_Form


class KeyList(QWidget):
    """
    A table widget that can show groups of strings with chosen foreground and
    background color. Shows also a key for the table, which contains the group
    name with chosen colors for the group.

    Sends **signal_item_activated(str, str)** when item in the main table is
    double clicked. In the signal the first string contains the text of the
    clicked cell and the second one contains the name of the group that string
    belongs to.

    :param: parent, parent QObject of this QObject.
    """
    signal_item_activated = pyqtSignal(str, str)
    color_map = collections.OrderedDict()
    column_width = 150

    def __init__(self, parent=None):
        super().__init__(parent)

        self._items = list()
        self._item_dictionary = collections.OrderedDict()

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.tableWidget_2.setColumnCount(5)
        palette = self.ui.tableWidget_2.palette()
        palette.setColor(QPalette.Base, QColor("Gray"))
        palette.setColor(QPalette.HighlightedText, QColor("Black"))
        palette.setColor(QPalette.Highlight, QColor("White"))
        self.ui.tableWidget_2.setPalette(palette)
        palette.setColor(QPalette.Base, QColor("Black"))
        self.ui.keyTableWidget_2.setPalette(palette)

        self.ui.keyTableWidget_2.setRowCount(1)
        self.ui.keyTableWidget_2.setColumnCount(3)
        max_height = self.ui.labelKeys_2.size().height()*0.70
        self.ui.keyTableWidget_2.setMaximumHeight(max_height)
        self.ui.keyTableWidget_2.setMaximumWidth(
            self.ui.keyTableWidget_2.width()*3)
        self.ui.keyTableWidget_2.setRowHeight(0, max_height)
        self.ui.keyTableWidget_2.columnWidth(
            self.ui.keyTableWidget_2.width()//3)
        self.ui.keyTableWidget_2.setEnabled(False)

        self.ui.tableWidget_2.itemDoubleClicked.connect(self._item_activated)

    def add_item_group(self, group_name: str, fg_color: str, bg_color: str):
        """
        This method creates an item group for chosen name and sets foreground
        color and background color for it.

        :param group_name: name for group of strings
        :param fg_color: foreground color as a string, accepts same colors as
            QColor http://qt-project.org/doc/qt-5/QColor.html
        :param bg_color: background color as a string, accepts same colors as
            QColor http://qt-project.org/doc/qt-5/QColor.html
        """
        self.color_map[group_name] = [QColor(fg_color).name(),
                                      QColor(bg_color).name()]

    def update_item_group(self, group_name: str, items_str: list):
        """
        Updates the items for given group.

        :param group_name: string, name of the group. If colors for the group
            have not been given, default colors are used.
        :param items_str: list of strings
        """
        self._item_dictionary[group_name] = items_str

    def _update_key(self):
        """
        Updates the key. Run after the table has been (re)populated.
        """
        i = 0
        for key in self.color_map.keys():
            item = QTableWidgetItem(key)
            if self.color_map.get(key):
                item.setForeground(QBrush(QColor(self.color_map[key][0])))
                item.setBackground(QBrush(QColor(self.color_map[key][1])))

            self.ui.keyTableWidget_2.setItem(0, i, item)
            i += 1

    @pyqtSlot()
    def populate(self):
        """
        Populates the table with given string groups
        and sets the number of columns.
        """
        columns = self.ui.tableWidget_2.width() // 140
        logging.debug("columns on resize: " + str(columns))
        self._items.clear()
        self.ui.tableWidget_2.clear()
        self.ui.tableWidget_2.columnWidth(140)

        # We build a list of items and set the colors for item.
        for key in self._item_dictionary:
            for str_item in self._item_dictionary[key]:
                item = QTableWidgetItem(str_item)
                self._items.append(item)
                item.setForeground(QBrush(QColor(self.color_map[key][0])))
                item.setBackground(QBrush(QColor(self.color_map[key][1])))

        if len(self._items) == 0:
            return

        self.ui.tableWidget_2.setRowCount(len(self._items)//columns+1)
        self.ui.tableWidget_2.setColumnCount(columns)
        i = 0
        while i < columns:
            self.ui.tableWidget_2.setColumnWidth(i, 140)
            i += 1

        # We set the items to the table.
        row = 0
        col = 0
        for item in self._items:
            self.ui.tableWidget_2.setItem(row, col, item)
            if col+1 == columns:
                col = 0
                row += 1
            else:
                col += 1

        self._update_key()

    @pyqtSlot()
    def clear(self):
        """
        Clears the tableWidget and it's key.
        """
        self.ui.tableWidget_2.clear()
        for key in self._item_dictionary:
            self._item_dictionary[key] = []

    @pyqtSlot(QTableWidgetItem)
    def _item_activated(self, item: QTableWidgetItem):
        """
        When an item is activated in the table signal_item_activated containing
        the content string of the item and the group name is emitted.

        :param item: QTableWidget item from TableWidget
        """
        text = item.text()
        fg_color = item.foreground().color().name()
        bg_color = item.background().color().name()
        group_name = ""
        for key, value in self.color_map.items():
            logging.debug(key + " " + value[0] + " " + str(type(value[0]))
                          + " " + value[1])
            logging.debug(fg_color + " " + bg_color)
            if value[0] == fg_color and value[1] == bg_color:
                group_name = key
                break

        self.signal_item_activated.emit(text, group_name)

    def show(self):
        """
        This method hooks in to the super class show. When the widget is show
        the string table is repopulated
        """
        self.populate()
        super().show()

    def resizeEvent(self, event):
        self.populate()
        logging.debug("Width: " + str(self.ui.tableWidget_2.width()))
        super().resizeEvent(event)

