# -*- coding: utf-8 -*-
#
# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
#TODO: replace sub module method calls with signals
#
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QSize
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from .data.term import Term

from .widgets.str_browser import StrBrowser
from .widgets.term_display import TermDisplay
from .widgets.term_editor import TermEditor
from .widgets.term_linker import TermLinker
from .widgets.definator_button import DefinatorButton


class MainWidget(QWidget):
    """
    Wrapper widget which contains the term handling widgets and routing of
    events between them and to the parent widget. Also knows the current term
    being examined
    """
    #sent when a exist term content is updated (termEditor knows this)
    update_term = pyqtSignal(Term)
    term_updated = pyqtSignal(Term)

    #sent when user wants to add a new term
    create_term = pyqtSignal()
    #sent when a new term has been created
    add_new_term = pyqtSignal(Term)
    remove_term = pyqtSignal(Term)
    save_changes = pyqtSignal()

    term_str_selected = pyqtSignal(str)

    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        self.current_term = None

        self.term_str_browser = StrBrowser()
        self.term_display = TermDisplay()
        self.term_editor = TermEditor()
        self.term_linker = TermLinker()

        #self.save_project = DefinatorButton("Save changes")
        #self.save_project.center()
        self.buttons.edit_term = DefinatorButton("Edit")
        self.buttons.view_term = DefinatorButton("View")
        self.buttons.remove_term = DefinatorButton("Delete")
        self.buttons.edit_term.align_right()
        self.buttons.view_term.align_right()
        self.buttons.remove_term.align_right()
        self.buttons.add_term = DefinatorButton("Add term")
        self.buttons.add_term.center()

        self.setMinimumSize(QSize(750, 200))

        #Set layout
        layout_h = QHBoxLayout()

        layout_h_term_buttons = QHBoxLayout()
        layout_v_term_view = QVBoxLayout()
        layout_v_term_browser = QVBoxLayout()

        #Term browser area:
        layout_h.addLayout(layout_v_term_browser)
        layout_v_term_browser.addWidget(self.term_str_browser)
        layout_v_term_browser.addWidget(self.buttons.add_term)
        #layout_v_term_browser.addWidget(self.buttons.save_project)

        #Term editor area:
        layout_h_term_buttons.addWidget(self.buttons.remove_term)
        layout_h_term_buttons.addWidget(self.buttons.view_term)
        layout_h_term_buttons.addWidget(self.buttons.edit_term)
        self.buttons.edit_term.hide()
        self.buttons.remove_term.hide()

        layout_v_term_view.addLayout(layout_h_term_buttons)
        layout_v_term_view.addWidget(self.term_editor)
        layout_v_term_view.addWidget(self.term_display)
        self.term_display.hide()
        layout_v_term_view.addWidget(self.term_linker)
        #Add editor area to browser layout
        layout_h.addLayout(layout_v_term_view)

        self.setLayout(layout_h)

        self.term_str_browser.setFocus()

        # Inner interaction logic:
        self.term_editor.stopped_editing.connect(self._stopped_editing)
        self.term_editor.stopped_editing_new_term.connect(
            self._stopped_editing_new_term)

        self.term_str_browser.str_selected.connect(self._change_term)
        self.term_str_browser.list_is_empty.connect(self._create_new_term)

        self.buttons.add_term.clicked.connect(self._create_new_term)
        self.buttons.edit_term.clicked.connect(self._start_editing)
        self.buttons.view_term.clicked.connect(self._show_term_display)
        self.buttons.remove_term.clicked.connect(self._remove_term)

    @pyqtSlot()
    def _show_term_display(self):
        """
        TermEditor emits changes when it is hidden.
        """
        if self.term_editor.isVisible():
            self.term_editor.hide()
            self.term_display.show()
            self.buttons.view_term.hide()
            self.buttons.view_term.siz
            self.buttons.edit_term.show()
            self.buttons.remove_term.show()

    def _show_term_editor(self):
        if self.term_display.isVisible():
            self.term_display.hide()
            self.term_editor.show()
            self.buttons.view_term.show()
            self.buttons.edit_term.hide()
            self.buttons.remove_term.hide()

    def _set_current_term(self, term: Term):
        self.term_str_browser.set_current_str(term.term)
        self.term_display.set_current_term(term)
        self.term_linker.set_current_term(term)
        self.current_term = term

    @pyqtSlot()
    def reset(self):
        self.term_str_browser.set_list([])
        self._create_new_term()

    # In comming slots from outside:
    @pyqtSlot(tuple, Term)
    def initialize_a_project(self, terms: tuple, term: Term):
        self._show_term_display()
        self.term_str_browser.set_list(list(terms))
        self._set_current_term(term)

    @pyqtSlot(Term)
    def change_term(self, term: Term):
        self._show_term_display()
        self._set_current_term(term)

    @pyqtSlot(Term)
    def term_has_been_updated(self, term: Term):
        self.term_str_browser.mark_str(term)
        self.term_display.set_current_term(term)

    @pyqtSlot(Term)
    def added_a_term(self, term: Term):
        self.term_str_browser.add_a_str(term.term)
        self._set_current_term(term)

    @pyqtSlot(Term)
    def term_has_been_removed(self, term: Term):
        self.term_str_browser.rem_a_str(term.term)

    # Slots for inner signals and triggering of events to be passed on to parent
    # module.
    @pyqtSlot()
    def _create_new_term(self):
        #Hide editor, if it's visible --> saves changes.
        self._show_term_display()
        self._show_term_editor()

    @pyqtSlot()
    def _remove_term(self):
        self.remove_term.emit(self.current_term)

    @pyqtSlot()
    def _start_editing(self):
        self.term_linker.edit_mode()
        self.term_editor.set_term(self.current_term)
        self._show_term_editor()

    @pyqtSlot(Term)
    def _stopped_editing(self, term: Term):
        self.term_linker.display_mode()
        self.term_display.show()
        self.update_term.emit(term)

    @pyqtSlot(Term)
    def _stopped_editing_new_term(self, term: Term):
        self.term_linker.display_mode()
        self.term_display.show()
        print("add new")
        self.add_new_term.emit(term)

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

    @pyqtSlot()
    def _link_file(self):
        pass

    @pyqtSlot()
    def _unlink_file(self):
        pass
