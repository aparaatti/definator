# -*- coding: utf-8 -*-
#
# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QSize
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QKeySequence, QIcon

from .action_helper import make_action_helper
from .data.term import Term

from .widgets.str_browser import StrBrowser
from .widgets.term_display import TermDisplay
from .widgets.term_editor import TermEditor
from .widgets.link_list import LinkList


class MainWidget(QWidget):
    """
    Wrapper widget which contains the term handling widgets and routing of
    events between them and to the parent widget. Also knows the current term
    being examined.
    """
    #sent when a existing term content is updated (termEditor knows this)
    update_term = pyqtSignal(Term)

    #sent when a new term has been created
    add_new_term = pyqtSignal(Term)
    remove_term = pyqtSignal(str)
    save_changes = pyqtSignal()

    term_str_selected = pyqtSignal(str)

    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        self._current_term = None

        #Modules:
        self.term_str_browser = StrBrowser("Term Browser")
        self.term_display = TermDisplay()
        self.related_terms = LinkList("Related terms")
        self.term_editor = TermEditor()

        self.setMinimumSize(QSize(750, 200))

        self._init_actions()
        self._init_layout()
        #New project state:
        self._init_state()

        # Inner interaction logic:
        self.term_editor.signal_term_was_changed.connect(self._stopped_editing)
        self.term_editor.signal_stopped_editing_new_term.connect(
            self._stopped_editing_new_term)
        self.term_editor.signal_valid.connect(self.act_view_term.setEnabled)

        self.term_str_browser.str_selected.connect(self._change_term)
        self.related_terms.link_selected.connect(self._change_term)
        self.term_str_browser.list_is_empty.connect(self.reset)

        #Undo - redo
        self.term_editor.signal_redo_event.connect(self.redo)
        self.term_editor.signal_undo_event.connect(self.undo)
        self.term_display.signal_redo_event.connect(self.redo)
        self.term_display.signal_undo_event.connect(self.undo)
        self.related_terms.signal_redo_event.connect(self.redo)
        self.related_terms.signal_undo_event.connect(self.undo)
        self.term_str_browser.signal_redo_event.connect(self.redo)
        self.term_str_browser.signal_undo_event.connect(self.undo)

        self.term_editor.signal_can_undo.connect(self.set_can_undo)
        self.term_editor.signal_can_redo.connect(self.set_can_redo)

    def _set_current_term(self, term: Term):
        self.term_str_browser.set_current_str(term.term)
        self.term_display.set_term(term)
        self.term_editor.set_term(term)
        self.related_terms.set_current_html(term.related_terms_as_html)
        self._current_term = term
        self.act_undo.setEnabled(self._current_term.previous_term is not None)
        self.act_redo.setEnabled(self._current_term.next_term is not None)

    def _linking_enabled(self, boolean: bool):
        self.act_link_terms.setEnabled(boolean)
        self.act_unlink_terms.setEnabled(boolean)
        self.act_link_files.setEnabled(boolean)
        self.act_unlink_files.setEnabled(boolean)

    def _show_term_editor(self):
        if self.term_display.isVisible():
            self.term_display.hide()
            self.related_terms.hide()
            self.term_editor.show()
            self.act_add_term.setEnabled(False)
            self.act_rem_term.setEnabled(False)
            self.act_edit_term.setEnabled(False)
            self.act_view_term.setEnabled(True)

    @pyqtSlot()
    def show_term_display(self):
        """
        TermEditor emits changes when it is hidden.
        """
        if self.term_editor.isVisible():
            self.term_editor.hide()
            self.term_display.show()
            self.related_terms.show()
            self.act_add_term.setEnabled(True)
            self.act_rem_term.setEnabled(True)
            self.act_edit_term.setEnabled(True)
            self.act_view_term.setEnabled(False)

    # In coming slots from outside:
    @pyqtSlot()
    def reset(self):
        """
        This slot initializes a new project.
        """
        self.term_str_browser.set_list([])
        self._current_term = None
        self._init_state()
        self.create_new_term()

    @pyqtSlot(tuple, Term)
    def initialize_a_project(self, terms: tuple, term: Term):
        """
        This slot initializes a project.

        :param terms: list of terms to show as a tuple containing strings
        :param term: term to show, a Term object
        """
        self.term_str_browser.set_list(list(terms))
        self._init_state()
        self._set_current_term(term)
        self.show_term_display()

    @pyqtSlot()
    def unmark(self):
        self.term_str_browser.unmark_all()

    @pyqtSlot(Term)
    def change_term(self, term: Term):
        self._set_current_term(term)
        self.show_term_display()

    @pyqtSlot(Term)
    def term_has_been_updated(self, term: Term):
        self.term_str_browser.mark_str(term.term)
        self._set_current_term(term)

    @pyqtSlot(Term)
    def added_a_term(self, term: Term):
        self.term_str_browser.add_a_str(term.term)
        self.term_str_browser.mark_str(term.term)
        self._set_current_term(term)

    @pyqtSlot(Term)
    def term_has_been_removed(self, term: Term):
        self.term_str_browser.rem_a_str(term.term)

    def save_current_term(self):
        pass

    # Slots for inner signals and triggering of events to be passed on to parent
    # module.
    @pyqtSlot()
    def create_new_term(self):
        """
        This slot starts the creation of a new term.
        """
        #We show term display, so that term_editor saves changes.
        self.show_term_display()
        self.term_editor.set_term(Term())

        #One can't links things to a new term
        self._show_term_editor()

        self._linking_enabled(False)
        self.act_undo.setEnabled(False)
        self.act_redo.setEnabled(False)
        self.act_view_term.setEnabled(False)
        self.act_link_files.setEnabled(False)
        self.act_link_terms.setEnabled(False)
        self.act_unlink_terms.setEnabled(False)
        self.act_unlink_files.setEnabled(False)

    @pyqtSlot()
    def edit_current_term(self):
        self._set_current_term(self._current_term)
        self._linking_enabled(True)
        self._show_term_editor()

    @pyqtSlot(bool)
    def set_can_undo(self, boolean: bool):
        """
        :param boolean:
        :return:
        """
        if boolean:
            self.act_undo.setEnabled(True)
        elif self._current_term is not None and self._current_term.can_undo:
            self.act_undo.setEnabled(True)
        else:
            self.act_undo.setEnabled(False)


    @pyqtSlot(bool)
    def set_can_redo(self, boolean: bool):
        if boolean:
            self.act_redo.setEnabled(True)
        elif self._current_term is not None and self._current_term.can_redo:
            self.act_redo.setEnabled(True)
        else:
            self.act_redo.setEnabled(False)

    @pyqtSlot()
    def undo(self):
        if self.term_editor.isVisible():
            self.term_editor.undo()
        elif self._current_term and self._current_term.can_undo:
            self._set_current_term(self._current_term.previous_term)

    @pyqtSlot()
    def redo(self):
        if self.term_editor.isVisible():
            self.term_editor.redo()
        elif self._current_term and self._current_term.can_redo:
            self._set_current_term(self._current_term.next_term)

    @pyqtSlot()
    def _remove_term(self):
        if not self._current_term:
            return
        remove = QMessageBox.question(
            self, "Are you sure you want to delete this term?",
            "Are you sure, you wannt to delete this term?",
            QMessageBox.Yes | QMessageBox.No)
        if remove == QMessageBox.Yes:
            self.remove_term.emit(self._current_term.term)

    @pyqtSlot(Term)
    def _stopped_editing(self, term: Term):
        self._set_current_term(term)
        self.term_display.show()
        self.update_term.emit(term)

    @pyqtSlot(Term)
    def _stopped_editing_new_term(self, term: Term):
        self.add_new_term.emit(term)

    @pyqtSlot(str)
    def _change_term(self, term_str):
        self.term_str_selected.emit(term_str)

    def _init_actions(self):
        #ACTIONS:
        self.act_link_terms = make_action_helper(self, "&Link terms", "Link terms to current term", "alt+l", QIcon.fromTheme('list-add'))
        self.act_link_terms.triggered.connect(self.term_editor.link_terms)
        self.act_unlink_terms = make_action_helper(self, "&Unlink terms", "Remove related terms from current term", "alt+u", QIcon.fromTheme('list-remove'))
        self.act_unlink_terms.triggered.connect(self.term_editor.unlink_terms)
        self.act_link_files = make_action_helper(self, "Link &files", "Link files to current term", "alt+k", QIcon.fromTheme('list-add'))
        self.act_link_files.triggered.connect(self.term_editor.link_files)
        self.act_unlink_files = make_action_helper(
            self, "U&nlink files", "Unlink files from current term", "alt+y", QIcon.fromTheme('list-remove'))
        self.act_unlink_files.triggered.connect(self.term_editor.unlink_files)
        self.act_rem_term = make_action_helper(
            self, "&Remove term", "Remove current term", QKeySequence.Delete, QIcon.fromTheme('edit-delete'))
        self.act_rem_term.triggered.connect(self._remove_term)
        self.act_save_term = make_action_helper(
            self, "&Save current term", "Save changes for term", None, QIcon.fromTheme('document-save'))
        self.act_save_term.triggered.connect(self.save_current_term)
        self.act_view_term = make_action_helper(
            self, "&View current term", "View current term", QKeySequence.Close, QIcon.fromTheme('document-revert'))
        self.act_view_term.triggered.connect(self.show_term_display)
        self.act_edit_term = make_action_helper(
            self, "&Edit current term", "Edit current term", "ctrl+e", QIcon.fromTheme('accessories-text-editor'))
        self.act_edit_term.triggered.connect(self.edit_current_term)
        self.act_add_term = make_action_helper(
            self, "&Add term", "Add new term to project.",
            QKeySequence.New, QIcon.fromTheme('document-new',))
        self.act_add_term.triggered.connect(self.create_new_term)
        self.act_undo = make_action_helper(
            self, "Undo", "Undo previous change", QKeySequence.Undo, QIcon.fromTheme('edit-undo'))
        self.act_undo.triggered.connect(self.undo)
        self.act_redo = make_action_helper(
            self, "Redo", "Redo undone change", QKeySequence.Redo, QIcon.fromTheme('edit-redo'))
        self.act_redo.triggered.connect(self.redo)
        self.act_undo.setEnabled(False)
        self.act_redo.setEnabled(False)

    def _init_layout(self):
        #Set layout
        layout_h = QHBoxLayout()

        layout_v_term_view = QVBoxLayout()
        layout_v_term_browser = QVBoxLayout()

        #Term browser area:
        layout_h.addLayout(layout_v_term_browser)
        layout_v_term_browser.addWidget(self.term_str_browser)

        layout_v_term_view.addWidget(self.term_editor)
        layout_v_term_view.addWidget(self.term_display)
        layout_v_term_view.addWidget(self.related_terms)

        #Add editor area to browser layout
        layout_h.addLayout(layout_v_term_view)
        self.setLayout(layout_h)

    def _init_state(self):
        self.term_str_browser.setFocus()
        self.act_add_term.setEnabled(False)
        self.act_rem_term.setEnabled(False)
        self.act_edit_term.setEnabled(False)
        self.act_view_term.setEnabled(False)
        self.act_link_terms.setEnabled(False)
        self.act_unlink_terms.setEnabled(False)
        self.act_link_files.setEnabled(False)
        self.act_unlink_files.setEnabled(False)
        self.act_save_term.setEnabled(False)
        self.term_display.hide()
        self.related_terms.hide()
        self.term_editor.show()
