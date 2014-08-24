# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QSize
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLayout

from .data.term import Term

from .widgets.str_browser import StrBrowser
from .widgets.term_display import TermDisplay
from .widgets.term_editor import TermEditor
from .widgets.definator_button import DefinatorButton


class MainWidget(QWidget):
    """
    Wrapper widget which contains the term handling widgets and also routes
    events and works as a proxy for events.
    """
    #sent when a exist term content is updated (termEditor knows this)
    current_term_updated = pyqtSignal(Term)
    #sent when user wants to add a new term
    create_term = pyqtSignal()
    #sent when a new term has been created
    add_new_term = pyqtSignal(Term)
    save_changes = pyqtSignal()

    #
    term_str_selected = pyqtSignal(str)

    #self.main_widget.term_display.termSelected.connect(self.change_term)
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)

        self.term_browser = StrBrowser()
        self.term_display = TermDisplay()
        self.term_editor = TermEditor()

        self.term_editor.hide()

        self.edit_term_button = DefinatorButton("Edit")
        self.edit_term_button.align_right()
        self.add_term_button = DefinatorButton("Add term", self)
        self.save_project_button = DefinatorButton("Save changes")

        self.setMinimumSize(QSize(750, 200))

        layout_h = QHBoxLayout()
        self.layout_v = QVBoxLayout()
        layout_v2 = QVBoxLayout()

        #Term browser area:
        layout_h.addLayout(layout_v2)
        layout_v2.addWidget(self.term_browser)
        layout_v2.addWidget(self.add_term_button)
        layout_v2.addWidget(self.save_project_button)

        #Term editor area:
        #TODO: self.layout_v.setSizeConstraint(QLayout.SetMaximumSize)
        self.layout_v.addWidget(self.edit_term_button)
        self.layout_v.addWidget(self.term_display)
        self.layout_v.addWidget(self.term_editor)
        self.layout_h2 = QHBoxLayout()
        self.layout_v.addLayout(self.layout_h2)

        #Add editor area to browser layout
        layout_h.addLayout(self.layout_v)

        #Set layout
        self.setLayout(layout_h)
        self.term_browser.setFocus()

        # Inner interaction logic:
        self.term_display.startEditing.connect(self._start_editing)

        self.term_editor.stopped_editing.connect(self._stopped_editing)
        self.term_editor.stopped_editing_new_term.connect(
            self._stopped_editing_new_term)

        self.term_browser.str_selected.connect(self._change_term)

        self.save_project_button.clicked.connect(self._save_changes)
        self.add_term_button.clicked.connect(self._create_new_term)
        self.edit_term_button.clicked.connect(self._start_editing)

    # In comming slots from outside:
    @pyqtSlot(tuple, Term)
    def initialize_a_project(self, terms: tuple, term: Term):
        self.term_browser.set_list(terms)
        self.term_browser.set_current_str(term.term)
        self.term_display.set_current_term(term)

    @pyqtSlot(Term)
    def change_term(self, term: Term):
        if self.term_editor.isVisible():
            self.term_editor.hide()
            self.term_display.show()

        self.term_browser.set_current_str(term.term)
        self.term_display.set_current_term(term)

    @pyqtSlot()
    def update_term(self):
        self.term_browser.mark_current_term_updated()

    @pyqtSlot(Term)
    def added_a_term(self, term: Term):
        self.term_browser.add_a_term(term.term)

    # Inner communication
    @pyqtSlot()
    def _create_new_term(self):
        self.term_display.hide()
        self.term_editor.show()

    @pyqtSlot()
    def _start_editing(self):
        self.layout_v.removeWidget(self.term_display)
        self.layout_v.addWidget(self.term_editor)

    @pyqtSlot(Term)
    def _stopped_editing(self, term: Term):
        self.term_editor.hide()
        self.term_display.show()
        self.current_term_updated.emit()

    @pyqtSlot(Term)
    def _stopped_editing_new_term(self, term):
        self.add_a_term.emit(term)

    @pyqtSlot()
    def _save_changes(self):
        self.save_changes.emit()

    @pyqtSlot(str)
    def _change_term(self, term_str):
        self.term_str_selected.emit(term_str)

    @pyqtSlot()
    def _link_terms(self):
        pass

    @pyqtSlot()
    def _unlink_terms(self):
        pass
