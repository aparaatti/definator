# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
import os
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget

from ..data.term import Term
from .qtdesigner.ui_QTermEditor import Ui_TermEditor


class TermEditor(QWidget):
    signal_stopped_editing = pyqtSignal(Term)
    signal_stopped_editing_new_term = pyqtSignal(Term)

    signal_valid = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._valid = None
        self.ui = Ui_TermEditor()
        self.ui.setupUi(self)
        self.ui.lineEditTitle.text = ""
        self._current_term = None
        self.ui.addImageToolButton.clicked.connect(self.add_image_tag)
        self.ui.addTitleToolButton.clicked.connect(self.add_title_tag)

    def _clear(self):
        self.ui.lineEditTitle.clear()
        self.ui.textEditContent.clear()
        self._current_term = None

    def set_term(self, term: Term):
        self._current_term = term
        if self._current_term is None:
            self._clear()
        else:
            self.ui.lineEditTitle.setText(term.term)
            self.ui.textEditContent.setText(term.description)

    def hide(self):
        if self._current_term is None:
            self.signal_stopped_editing_new_term.emit(self._fill_term(Term()))
            self._clear()
        else:
            self._fill_term(self._current_term)
            self.signal_stopped_editing.emit(self._current_term)
            self._clear()

        super().hide()

    @pyqtSlot()
    def add_image_tag(self):
        self.ui.textEditContent.insertPlainText('#img("path/to/image","Image title")')

    @pyqtSlot()
    def add_title_tag(self):
        self.ui.textEditContent.insertPlainText("##Title##")

    def _fill_term(self, term: Term):
        term.term = self.ui.lineEditTitle.displayText()
        text = self.ui.textEditContent.toPlainText()
        white_space_removed = list()
        [white_space_removed.append(line.strip()) for line in text.splitlines()]
        term.description = os.linesep.join(white_space_removed)
        return term
