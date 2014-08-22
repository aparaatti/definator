# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QSize
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout

from .data.term import Term

from .widgets.str_browser import StrBrowser
from .widgets.term_display import TermDisplay
from .widgets.term_editor import TermEditor
from .widgets.definator_button import DefinatorButton


class MainWidget(QWidget):
    #sent when a exist term content is updated (termEditor knows this)
    current_term_updated = pyqtSignal(Term)

    #sent when user wants to add a new term
    add_a_term = pyqtSignal(Term)

    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        self._currentTerm = Term("New")

        self.termBrowser = StrBrowser()
        self.termDisplay = TermDisplay()
        self.termEditor = TermEditor()
        self.addTermButton = DefinatorButton("Add term")
        self.saveChangesButton = DefinatorButton("Save changes")
        self.linkTermsButton = DefinatorButton("Link terms")
        self.unlinkTermsButton = DefinatorButton("Unlink terms")

        self.setMinimumSize(QSize(750, 200))

        layout = QVBoxLayout()

        layout_h = QHBoxLayout()
        self.layout_v = QVBoxLayout()
        layout_v2 = QVBoxLayout()

        layout_h.addLayout(layout_v2)
        layout_v2.addWidget(self.termBrowser)
        layout_v2.addWidget(self.addTermButton)
        layout_v2.addWidget(self.saveChangesButton)

        self.layout_v.addWidget(self.termDisplay)

        layout_h.addLayout(self.layout_v)

        layout.addLayout(layout_h)

        self.setLayout(layout)
        self.termBrowser.setFocus()

        self.termDisplay.startEditing.connect(self.__started_editing)
        self.termEditor.stopEditing.connect(self.__stopped_editing)

    @pyqtSlot()
    def __started_editing(self):
        self.layout_v.removeWidget(self.termDisplay)
        self.layout_v.addWidget(self.termEditor)

    @pyqtSlot(bool)
    def __stopped_editing(self, changed=False):
        self.layout_v.removeWidget(self.termEditor)
        self.layout_v.addWidget(self.termDisplay)

        if changed:
            self.current_term_updated.emit()

    @pyqtSlot(Term)
    def change_term(self, term: Term):
        self.termBrowser.set_current_str(term.term)
        self.termDisplay.set_current_term(term)

    @pyqtSlot(tuple, Term)
    def opened_a_new_project(self, terms: tuple, term: Term):
        self.termBrowser.set_list(terms)
        self.termBrowser.set_current_str(term.term)
        self.termDisplay.set_current_term(term)

    @pyqtSlot()
    def update_term(self):
        self.termBrowser.mark_current_term_updated()

    @pyqtSlot(Term)
    def added_a_term(self, term: Term):
        self.termBrowser.add_a_term(term.term)
