# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QPushButton, QWidget, QHBoxLayout

from ..data.term import Term
from .qtdesigner.ui_QTermEditor import Ui_TermEditor


class TermEditor(QWidget):
    stopped_editing = pyqtSignal(Term)
    stopped_editing_new_term = pyqtSignal(Term)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_TermEditor()
        self.ui.setupUi(self)
        self._current_term = Term()
        self._is_new_term = False

        link_button_layout = QHBoxLayout()
        self.link_terms_button = QPushButton("Link terms", self)
        self.unlink_terms_button = QPushButton("Unlink terms", self)
        link_button_layout.addWidget(self.link_terms_button)
        link_button_layout.addWidget(self.unlink_terms_button)

        self.ui.verticalLayout.addLayout(link_button_layout)

    def set_term(self, term: Term):
        self._current_term = term
        if term.term == Term().term:
            self._is_new_term = True

        self.ui.lineEditTitle.text = term.term
        self.ui.textEditContent.text = term.description

    def hide(self):
        if self._is_new_term:
            self.stopped_editing_new_term.emit(self._current_term)
            self._is_new_term = False
        else:
            self.stopped_editing.emit(self._current_term)

        super().hide()
