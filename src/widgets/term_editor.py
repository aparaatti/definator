# -*- coding: utf-8 -*-
# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
import os
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QKeySequence, QIcon

from ..action_helper import make_action_helper
from ..data.term import Term
from .qtdesigner.ui_QTermEditor import Ui_TermEditor
from .key_press_eater import KeyPressEater


class TermEditor(QWidget):

    signal_stopped_editing = pyqtSignal(Term)
    signal_stopped_editing_new_term = pyqtSignal(Term)

    signal_can_undo = pyqtSignal(bool)
    signal_can_redo = pyqtSignal(bool)

    signal_undo_event = pyqtSignal()
    signal_redo_event = pyqtSignal()

    signal_valid = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._valid = None
        self._redo_count = 0
        self._undo_count = 0
        self.ui = Ui_TermEditor()
        self._init_actions()
        self.ui.setupUi(self)
        self.ui.lineEditTitle.text = ""
        self._current_term = None
        self.ui.addImageToolButton.clicked.connect(self.add_image_tag)
        self.ui.addTitleToolButton.clicked.connect(self.add_title_tag)
        self.ui.lineEditTitle.textChanged.connect(self._validate_term)

        #Hook into undo/redo of term_editor
        self.eventFilter = KeyPressEater(QKeySequence.Undo, self)
        self.eventFilter2 = KeyPressEater(QKeySequence.Redo, self)
        self.ui.textEditContent.installEventFilter(self.eventFilter)
        self.ui.textEditContent.installEventFilter(self.eventFilter2)

        #We do not provied undo in editor window for term title, it
        #will be undone when textEdit runs out of undoes.
        #Othervice one should keep track of the order of edits to term title
        #and description text --> would not behave logically anyway.
        self.ui.textEditContent.redoAvailable.connect(self.signal_can_redo)
        self.ui.textEditContent.undoAvailable.connect(self.signal_can_undo)

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
            #Undo-redo linked list built here:
            self._current_term.next_term = self._fill_term(Term())
            self.signal_stopped_editing.emit(self._current_term.next_term)
            self._clear()

        super().hide()

    @pyqtSlot()
    def add_image_tag(self):
        self.ui.textEditContent.insertPlainText('#img("path/to/image","Image title")')

    @pyqtSlot()
    def add_title_tag(self):
        self.ui.textEditContent.insertPlainText("##Title##")

    @pyqtSlot()
    def undo(self):
        self.ui.textEditContent.undo()

    @pyqtSlot()
    def redo(self):
        self.ui.textEditContent.redo()

    def _fill_term(self, term: Term):
        term.term = self.ui.lineEditTitle.displayText()
        text = self.ui.textEditContent.toPlainText()
        white_space_removed = list()
        [white_space_removed.append(line.strip()) for line in text.splitlines()]
        term.description = os.linesep.join(white_space_removed)
        return term

    def _validate_term(self):
        if self.ui.lineEditTitle.displayText() is "":
            self.signal_valid.emit(False)
        else:
            self.signal_valid.emit(True)

    def _trigger_event(self, sequence: QKeySequence):
        if sequence is QKeySequence.Undo:
            self.signal_undo_event.emit()

        if sequence is QKeySequence.Redo:
            self.signal_redo_event.emit()

    @pyqtSlot()
    def _copy(self):
        if self.ui.textEditContent.hasFocus():
            self.ui.textEditContent.copy()
        if self.ui.lineEditTitle.hasFocus():
            self.ui.lineEditTitle.copy()

    @pyqtSlot()
    def _paste(self):
        if self.ui.textEditContent.hasFocus():
            self.ui.textEditContent.paste()
        if self.ui.lineEditTitle.hasFocus():
            self.ui.lineEditTitle.paste()

    @pyqtSlot()
    def _cut(self):
        if self.ui.textEditContent.hasFocus():
            self.ui.textEditContent.cut()
        if self.ui.lineEditTitle.hasFocus():
            self.ui.lineEditTitle.cut()

    def _init_actions(self):
        self.act_copy = make_action_helper(self, "Copy", "Copy to clipboard", QKeySequence.Copy, QIcon.fromTheme('edit-copy'))
        self.act_copy.triggered.connect(self._copy)
        self.act_paste = make_action_helper(self, "Paste", "Paste from clipboard", QKeySequence.Paste, QIcon.fromTheme('edit-paste'))
        self.act_paste.triggered.connect(self._paste)
        self.act_cut = make_action_helper(self, "Cut", "Cut to clipboard", QKeySequence.Cut, QIcon.fromTheme('edit-cut'))
        self.act_cut.triggered.connect(self._cut)
