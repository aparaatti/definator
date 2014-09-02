# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QListWidgetItem, QDialog, QDialogButtonBox

from .qtdesigner.ui_QStrChooser import Ui_QStrChooser


class StrChooser(QDialog):
    str_list_accepted = pyqtSignal(list)

    def __init__(self, parent):
        super(StrChooser, self).__init__(parent)
        self.ui = Ui_QStrChooser()
        self.ui.setupUi(self)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        self.ui.verticalLayout.addWidget(buttonBox)

    def _add_a_str(self, string: str):
        QListWidgetItem(string, self.ui.listWidget)
        self.ui.listWidget.sortItems()

    def set_list(self, str_list: list):
        self.ui.listWidget.clear()
        for string in str_list:
            self._add_a_str(string)

    def get_list(self):
        return list(self.str_2_item.keys())

    def _get_selected_str_list(self):
        items = self.ui.listWidget.selectedItems()
        str_list = list()
        for item in items:
            str_list.append(item.text())

        return str_list

    def accept(self):
        self.str_list_accepted.emit(self._get_selected_str_list())
        super().accept()
