# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
import collections

from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from PyQt5.QtGui import QBrush, QColor, QPalette

from .qtdesigner.ui_QTermLinks import Ui_QTermLinks


class TermLinker(QWidget):
    color_map = collections.OrderedDict()

    linkTermsClicked = pyqtSignal()
    unlinkTermsClicked = pyqtSignal()
    add_file = pyqtSignal()
    remove_files = pyqtSignal()

    """
    Signals do not pass current term, since the module doesn't need to know it.
    """

    def __init__(self, parent=None):
        super(TermLinker, self).__init__(parent)
        self._items = list()
        self._item_dictionary = collections.OrderedDict()
        self.__index = 0
        self.ui = Ui_QTermLinks()
        self.ui.setupUi(self)
        self.edit_mode()

        self.ui.tableWidget.setColumnCount(5)
        palette = self.ui.tableWidget.palette()
        palette.setColor(QPalette.Base, QColor("Gray"))
        palette.setColor(QPalette.HighlightedText, QColor("Black"))
        palette.setColor(QPalette.Highlight, QColor("White"))
        self.ui.tableWidget.setPalette(palette)
        palette.setColor(QPalette.Base, QColor("Black"))
        self.ui.keyTableWidget.setPalette(palette)

        self.ui.buttonLinkTerms.clicked.connect(self._link_term)
        self.ui.buttonUnlinkTerms.clicked.connect(self._unlink_term)
        self.ui.buttonAddFile.clicked.connect(self.add_file)
        self.ui.buttonRemoveFiles.clicked.connect(self.remove_files)

        self.ui.keyTableWidget.setRowCount(1)
        self.ui.keyTableWidget.setColumnCount(3)
        max_height = self.ui.labelKeys.size().height()*0.70
        self.ui.keyTableWidget.setMaximumHeight(max_height)
        self.ui.keyTableWidget.setMaximumWidth(self.ui.keyTableWidget.width()*3)
        self.ui.keyTableWidget.setRowHeight(0, max_height)
        self.ui.keyTableWidget.columnWidth(self.ui.keyTableWidget.width()//3)
        self.ui.keyTableWidget.setEnabled(False)

    @pyqtSlot()
    def _populate_TableWidget(self):
        columns = self.ui.tableWidget.width() // 150
        self._items.clear()
        self.ui.tableWidget.clear()
        self.ui.tableWidget.columnWidth(150)

        for key in self._item_dictionary:
            for str_item in self._item_dictionary[key]:
                item = QTableWidgetItem(str_item)
                self._items.append(item)
                item.setForeground(QBrush(QColor(self.color_map[key][0])))
                item.setBackground(QBrush(QColor(self.color_map[key][1])))

        self.ui.tableWidget.setRowCount(len(self._items)//columns+1)
        row = 0
        col = 0
        for item in self._items:
            self.ui.tableWidget.setItem(row, col, item)
            col += 1
            if col >= self.ui.tableWidget.columnCount():
                col = 0
                row += 1

    def add_item_group(self, group_name: str, fg_color: str, bg_color: str):
        self.color_map[group_name] = [fg_color, bg_color]

    def update_item_group(self, group_name: str, items_str: list):
        self._item_dictionary[group_name] = items_str

    def _update_key(self):
        i = 0
        for key in self.color_map.keys():
            item = QTableWidgetItem(key)
            item.setForeground(QBrush(QColor(self.color_map[key][0])))
            item.setBackground(QBrush(QColor(self.color_map[key][1])))
            self.ui.keyTableWidget.setItem(0, i, item)
            i += 1

    @pyqtSlot()
    def edit_mode(self):
        self.ui.buttonUnlinkTerms.setEnabled(True)
        self.ui.buttonLinkTerms.setEnabled(True)
        self.ui.buttonRemoveFiles.setEnabled(True)
        self.ui.buttonAddFile.setEnabled(True)

    @pyqtSlot()
    def display_mode(self):
        self.ui.buttonUnlinkTerms.setEnabled(False)
        self.ui.buttonLinkTerms.setEnabled(False)
        self.ui.buttonRemoveFiles.setEnabled(False)
        self.ui.buttonAddFile.setEnabled(False)

    @pyqtSlot()
    def _link_term(self):
        self.linkTermsClicked.emit()

    @pyqtSlot()
    def _unlink_term(self):
        self.unlinkTermsClicked.emit()

    @pyqtSlot()
    def clear(self):
        self.ui.tableWidget.clear()
        for key in self._item_dictionary:
            self._item_dictionary[key] = []

    def showEvent(self, arg):
        self._populate_TableWidget()
        self._update_key()
        super().showEvent(arg)
