# -*- coding: utf-8 -*-
#
# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QListWidgetItem, QDialog, QDialogButtonBox

from .qtdesigner.ui_QStrChooser import Ui_QStrChooser


class StrChooser(QDialog):
    """
    This dialog shows a list of strings. Can filter them and select multiple of
    them. On accept dialog emits **str_list_accept signal(list)** containing
    list of selected strings.

    :param: parent, parent QObject of this QObject.
    """
    str_list_accepted = pyqtSignal(list)

    def __init__(self, parent):
        super(StrChooser, self).__init__(parent)
        self.ui = Ui_QStrChooser()
        self._str_2_item = dict()
        self.ui.setupUi(self)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok |
                                     QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        self.ui.verticalLayout.addWidget(buttonBox)
        self.ui.lineEdit.textChanged.connect(self._filter)
        self.setSizeGripEnabled(True)

    @pyqtSlot(str)
    def _filter(self, string):
        """
        Filtering. This is triggered when filter lineEdit field's content
        changes. The content of the field is received as a parameter and a new
        filtered list is set to be displayed based on received string.

        :param string: String from signal bind to this slot
        """
        if string == "":
            self.set_list(list(self._str_2_item.keys()))
        else:
            filtered_list = [filtered_string for filtered_string
                             in self._str_2_item.keys()
                             if filtered_string.startswith(string)]
            self.ui.listWidget.clear()
            for string in filtered_list:
                self._add_a_str(string)

    def set_title(self, string: str):
        """
        This set's the title for the dialog. It also sets label on top of the
        dialog with the same text.

        :param string: tilte text as a string
        """
        self.setWindowTitle(string)

    def _add_a_str(self, string: str):
        """
        Adds a string to the list widget and sorts the list.

        :param string: one item in to be displayed on list widget.
        """
        self._str_2_item[string] = QListWidgetItem(string, self.ui.listWidget)
        self.ui.listWidget.sortItems()

    def set_list(self, str_list: list):
        """
        Adds all the items in the given string list to the display widget.

        :param str_list: list of string to be displayed
        """
        self.ui.listWidget.clear()
        for string in str_list:
            self._add_a_str(string)

    def get_list(self):
        """
        Gets the content of the list widget, also the filtered out strings.

        :return: Content of the list widget.
        """
        return list(self.str_2_item.keys())

    def _get_selected_str_list(self):
        """
        Gets a list of all the selected strings in the list widget.
        :return: list of strings
        """
        items = self.ui.listWidget.selectedItems()
        str_list = list()
        for item in items:
            str_list.append(item.text())

        return str_list

    def accept(self):
        """
        Hooks in to the super class accept method and sends a
        **str_list_accepted** signal containing selected strings as a list
        from the list widget on accept.

        :return: list of strings
        """
        self.str_list_accepted.emit(self._get_selected_str_list())
        super().accept()
