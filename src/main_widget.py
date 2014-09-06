# -*- coding: utf-8 -*-
#
# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
#TODO: replace sub module method calls with signals
#
from pathlib import Path
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QSize
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from .data.term import Term

from .widgets.str_browser import StrBrowser
from .widgets.term_display import TermDisplay
from .widgets.term_editor import TermEditor
from .widgets.term_linker import TermLinker
from .widgets.definator_button import DefinatorButton
from .widgets.str_chooser import StrChooser


class MainWidget(QWidget):
    """
    Wrapper widget which contains the term handling widgets and routing of
    events between them and to the parent widget. Also knows the current term
    being examined
    """
    #sent when a exist term content is updated (termEditor knows this)
    update_term = pyqtSignal(Term)
    term_updated = pyqtSignal(Term)

    #sent when term links have been changed:
    add_links_to_term = pyqtSignal(str, list)
    remove_links_from_term = pyqtSignal(str, list)

    #sent when file links have been changed:
    add_files_to_term = pyqtSignal(str, list)
    remove_files_from_term = pyqtSignal(str, list)

    #sent when user wants to add a new term (needed to be public?)
    create_term = pyqtSignal()
    #sent when a new term has been created, can use str?
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
        self.str_chooser = StrChooser(self)
        self.str_remover = StrChooser(self)

        self.edit_term_button = DefinatorButton("Edit")
        self.view_term_button = DefinatorButton("View")
        self.remove_term_button = DefinatorButton("Delete")
        self.edit_term_button.align_right()
        self.view_term_button.align_right()
        self.remove_term_button.align_right()
        self.add_term_button = DefinatorButton("Add term")
        self.add_term_button.align_right()

        self.setMinimumSize(QSize(750, 200))

        #Set layout
        layout_h = QHBoxLayout()

        layout_h_term_buttons = QHBoxLayout()
        layout_v_term_view = QVBoxLayout()
        layout_v_term_browser = QVBoxLayout()

        #Term browser area:
        layout_h.addLayout(layout_v_term_browser)
        layout_v_term_browser.addWidget(self.term_str_browser)

        #Term editor area:
        layout_h_term_buttons.addWidget(self.add_term_button)
        layout_h_term_buttons.addWidget(self.remove_term_button)
        layout_h_term_buttons.addWidget(self.view_term_button)
        layout_h_term_buttons.addWidget(self.edit_term_button)

        layout_v_term_view.addLayout(layout_h_term_buttons)
        layout_v_term_view.addWidget(self.term_editor)
        layout_v_term_view.addWidget(self.term_display)
        layout_v_term_view.addWidget(self.term_linker)

        #New project state:
        self.term_display.hide()
        self.add_term_button.setEnabled(False)
        self.remove_term_button.setEnabled(False)
        self.edit_term_button.setEnabled(False)
        self.view_term_button.setEnabled(True)
        self.term_linker.edit_mode()

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

        self.term_linker.linkTermsClicked.connect(self._link_terms)
        self.term_linker.unlinkTermsClicked.connect(self._unlink_terms)
        self.str_chooser.str_list_accepted.connect(self.link_terms)
        self.str_remover.str_list_accepted.connect(self.unlink_terms)

        self.add_term_button.clicked.connect(self._create_new_term)
        self.edit_term_button.clicked.connect(self._edit_current_term)
        self.view_term_button.clicked.connect(self._show_term_display)
        self.remove_term_button.clicked.connect(self._remove_term)

    def _set_current_term(self, term: Term):
        self.term_str_browser.set_current_str(term.term)
        self.term_display.set_current_term(term)
        self.term_linker.set_current_term(term)
        self.current_term = term

    def _show_term_editor(self):
        if self.term_display.isVisible():
            self.term_linker.edit_mode()
            self.term_display.hide()
            self.term_editor.show()
            self.add_term_button.setEnabled(False)
            self.remove_term_button.setEnabled(False)
            self.edit_term_button.setEnabled(False)
            self.view_term_button.setEnabled(True)

    @pyqtSlot()
    def _show_term_display(self):
        """
        TermEditor emits changes when it is hidden.
        """
        if self.term_editor.isVisible():
            self.term_editor.hide()
            self.term_display.show()
            self.add_term_button.setEnabled(True)
            self.view_term_button.setEnabled(False)
            self.edit_term_button.setEnabled(True)
            self.remove_term_button.setEnabled(True)

    @pyqtSlot()
    def reset(self, currentPath: Path=None):
        self.term_str_browser.set_list([])
        self._create_new_term()
        self.term_display = TermDisplay(currentPath)

    # In coming slots from outside:
    @pyqtSlot(tuple, Term)
    def initialize_a_project(self, terms: tuple, term: Term):
        self.term_str_browser.set_list(list(terms))
        self._set_current_term(term)
        self._show_term_display()

    @pyqtSlot(Term)
    def change_term(self, term: Term):
        self._show_term_display()
        self._set_current_term(term)

    @pyqtSlot(Term)
    def term_has_been_updated(self, term: Term):
        self.term_str_browser.mark_str(term.term)
        self.term_display.set_current_term(term)

    @pyqtSlot(Term)
    def added_a_term(self, term: Term):
        self.term_str_browser.add_a_str(term.term)
        self._set_current_term(term)

    @pyqtSlot(Term)
    def term_has_been_removed(self, term: Term):
        self.term_str_browser.rem_a_str(term.term)

    @pyqtSlot(list)
    def link_terms(self, str_list):
        if len(str_list) > 0:
            self.add_links_to_term.emit(self.current_term.term, str_list)

    @pyqtSlot(list)
    def unlink_terms(self, str_list):
        if len(str_list) > 0:
            self.remove_links_from_term.emit(self.current_term.term, str_list)

    # Slots for inner signals and triggering of events to be passed on to parent
    # module.
    @pyqtSlot()
    def _create_new_term(self):
        #Hide editor, if it's visible --> saves changes.
        self._show_term_display()
        self._show_term_editor()

    @pyqtSlot()
    def _edit_current_term(self):
        self.term_editor.set_term(self.current_term)
        self._show_term_editor()

    @pyqtSlot()
    def _remove_term(self):
        self.remove_term.emit(self.current_term)

    @pyqtSlot(Term)
    def _stopped_editing(self, term: Term):
        self.term_linker.display_mode()
        self.term_display.show()
        self.update_term.emit(term)

    @pyqtSlot(Term)
    def _stopped_editing_new_term(self, term: Term):
        if term.term is None:
            self._show_term_editor()
        else:
            self.add_new_term.emit(term)

    @pyqtSlot(str)
    def _change_term(self, term_str):
        self.term_str_selected.emit(term_str)

    @pyqtSlot()
    def _link_terms(self):
        a_list = self.term_str_browser.get_list()
        black_list = self.current_term.related_terms
        black_list.append(self.current_term.term)
        [a_list.remove(item) for item in black_list]
        self.str_chooser.set_list(a_list)
        self.str_chooser.show()

    @pyqtSlot()
    def _unlink_terms(self):
        self.str_remover.set_list(self.current_term.related_terms)
        self.str_remover.show()

    @pyqtSlot()
    def _link_file(self):
        pass

    @pyqtSlot()
    def _unlink_file(self):
        pass
