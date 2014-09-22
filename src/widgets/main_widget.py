# -*- coding: utf-8 -*-
#
# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
import logging
import os

from PyQt5.QtCore import pyqtSignal, pyqtSlot, QSize, QUrl
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QKeySequence, QIcon, QDesktopServices

from .qt_helper_functions import make_action_helper, warning_dialog
from ..data.term import Term

from .str_browser import StrBrowser
from .term_display import TermDisplay
from .term_editor import TermEditor
from .link_list import LinkList


class MainWidget(QWidget):
    """
    Wrapper widget which contains the term handling widgets and routing of
    events between them and to the parent widget. Also knows the current term
    being examined.
    """
    # sent when a existing term content is updated (termEditor knows this)
    update_term = pyqtSignal(Term)

    # sent when a new term has been created
    add_new_term = pyqtSignal(Term)
    remove_term = pyqtSignal(str)
    save_changes = pyqtSignal()

    term_str_selected = pyqtSignal(str)

    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        self._current_term = Term()

        # Modules:
        self.term_str_browser = StrBrowser("Term browser")
        self.term_display = TermDisplay()
        self.related_terms = LinkList("Related terms")
        self.term_editor = TermEditor()

        # Initialization methods:
        self._init_actions()
        self._init_layout()
        self._init_signals()

        self.term_str_browser.setFocus()
        self.term_display.hide()
        self.related_terms.hide()
        self.term_editor.hide()

    def _set_current_term(self, term: Term):
        self._current_term = term

    def _show_term_editor(self):
        logging.debug(" ** Showing term editor ** ")
        self.term_editor.set_term(self._current_term)

        if not self.term_editor.isVisible():
            self.term_display.hide()
            self.related_terms.hide()
            self.term_editor.show()

        self.act_add_term.setEnabled(False)
        self.act_rem_term.setEnabled(False)
        self.act_edit_term.setEnabled(False)

    @pyqtSlot()
    def show_term_display(self):
        """
        TermEditor emits changes when it is hidden.
        """
        logging.debug(" ** Showing term display ** ")
        if not self.term_display.isVisible():
            self.term_editor.hide()
            self.term_display.show()
            self.related_terms.show()

        self.term_str_browser.set_current_str(self._current_term.term)
        self.term_display.set_term(self._current_term)
        self.related_terms.set_current_html(
            self._current_term.related_terms_as_html)

        self.act_add_term.setEnabled(True)
        self.act_rem_term.setEnabled(True)
        self.act_edit_term.setEnabled(True)
        self.act_view_term.setEnabled(False)
        self.act_link_terms.setEnabled(False)
        self.act_unlink_terms.setEnabled(False)

    # In coming slots from outside:
    @pyqtSlot()
    def reset(self):
        """
        This slot initializes a new project.
        """
        self.term_str_browser.set_list([])
        self._current_term = Term()
        self.create_new_term()

    @pyqtSlot(tuple, Term)
    def initialize_a_project(self, terms: tuple, term: Term):
        """
        This slot initializes a project.

        :param terms: terms to show, a tuple containing strings
        :param term: term to show, a Term object
        """
        logging.debug("INITIALIZING A PROJECT")
        self.term_str_browser.set_list(list(terms))
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
        """
        This slot marks the term that has been updated and shows it.
        """
        self.term_str_browser.mark_str(term.term)

    @pyqtSlot(Term)
    def added_a_term(self, term: Term):
        """
        This slot adds a term to term browser and marks it.
        """
        self.term_str_browser.add_a_str(term.term)
        self.term_str_browser.mark_str(term.term)
        self._set_current_term(term)

    @pyqtSlot(Term)
    def term_has_been_removed(self, term: Term):
        """
        This slot removes a term from term browser.
        """
        self.term_str_browser.rem_a_str(term.term)

    def save_current_term(self):
        """
        Not implemented, maybe not needed.
        """
        warning_dialog(
            self, "Not implemented", "Saving current term is not implemented. "
            + os.linesep + "Saving the project saves all changed terms.")

    # Slots for inner signals and triggering of events to be passed on to
    # parent module.
    @pyqtSlot()
    def create_new_term(self):
        """
        This slot starts the creation of a new term.
        """
        # If term editor is visible we show term display to save changes from
        # term editor
        if self.term_editor.isVisible:
            self.show_term_display()

        self._set_current_term(Term())
        self._show_term_editor()

        self.act_link_terms.setEnabled(False)
        self.act_unlink_terms.setEnabled(False)
        self.act_view_term.setEnabled(False)

    @pyqtSlot()
    def edit_current_term(self):
        """
        This slots starts the editing of the current term.
        """
        self._set_current_term(self._current_term)
        self._show_term_editor()
        self.act_link_terms.setEnabled(True)
        self.act_unlink_terms.setEnabled(True)
        self.act_add_term.setEnabled(True)
        self.act_view_term.setEnabled(True)

    @pyqtSlot(str)
    def open_in_desktop_default_app(self, file_name: str):
        """
        This slot passes the opening of a file to desktop environment. If
        currentterm doesn't have the current file a warning dialog is raised.

        :parameter: file_name: str
        """
        logging.debug("File name @ os open: " + file_name)
        try:
            path = self._current_term.get_file_path(file_name)
        except FileNotFoundError:
            logging.info(
                'Could not open. No file "' + file_name + '" in project.')
            warning_dialog(
                self, "Could not open.", 'Could not open No file "' + file_name
                + '" in project.')
        else:
            logging.debug("path: " + str(path))
            QDesktopServices.openUrl(QUrl("file://" + str(path)))

    @pyqtSlot()
    def _remove_term(self):
        """
        This slot removes a term. A confirmation dialog is shown and
        after that removal is delegated with remove_term signal.
        """
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
        """
        This slot is triggered when the term editor stops editing existing
        term. The updated term is delegated with update_term signal.
        """
        self._set_current_term(term)
        self.term_display.show()
        self.update_term.emit(term)

    @pyqtSlot(Term)
    def _stopped_editing_new_term(self, term: Term):
        """
        This slot is triggered when the term editor stops editing a new term.
        The created term is delegated with add_new_term signal.
        """
        self.add_new_term.emit(term)

    @pyqtSlot(str)
    def _change_term(self, term_str):
        """
        This slot is triggered when term needs to be changed. The retrieval
        of the term is delegated with term_str_selected signal.
        """
        self.term_str_selected.emit(term_str)

    def _init_actions(self):
        # ACTIONS:
        self.act_link_terms = make_action_helper(
            self, "&Link terms", "Link terms to current term", "alt+l",
            QIcon.fromTheme('list-add'))
        self.act_link_terms.triggered.connect(self.term_editor.link_terms)
        self.act_unlink_terms = make_action_helper(
            self, "&Unlink terms", "Remove related terms from current term",
            "alt+u", QIcon.fromTheme('list-remove'))
        self.act_unlink_terms.triggered.connect(self.term_editor.unlink_terms)
        self.act_rem_term = make_action_helper(
            self, "&Remove term", "Remove current term", QKeySequence.Delete,
            QIcon.fromTheme('edit-delete'))
        self.act_rem_term.triggered.connect(self._remove_term)
        self.act_save_term = make_action_helper(
            self, "&Save current term", "Save changes for term", None,
            QIcon.fromTheme('document-save'))
        self.act_save_term.triggered.connect(self.save_current_term)
        self.act_view_term = make_action_helper(
            self, "&View current term", "View current term",
            QKeySequence.Close, QIcon.fromTheme('document-revert'))
        self.act_view_term.triggered.connect(self.show_term_display)
        self.act_edit_term = make_action_helper(
            self, "&Edit current term", "Edit current term", "ctrl+e",
            QIcon.fromTheme('accessories-text-editor'))
        self.act_edit_term.triggered.connect(self.edit_current_term)
        self.act_add_term = make_action_helper(
            self, "&Add term", "Add new term to project.",
            QKeySequence.New, QIcon.fromTheme('document-new',))
        self.act_add_term.triggered.connect(self.create_new_term)

    def _init_layout(self):
        # TermBrowser:
        layout_v_term_browser = QVBoxLayout()
        layout_v_term_browser.addWidget(self.term_str_browser)

        # Display/editor:
        layout_v_term_view = QVBoxLayout()
        layout_v_term_view.addWidget(self.term_editor)
        layout_v_term_view.addWidget(self.term_display)
        layout_v_term_view.addWidget(self.related_terms)

        # Wrap browser and editor in h-layout:
        layout_h = QHBoxLayout()
        layout_h.addLayout(layout_v_term_browser)
        layout_h.addLayout(layout_v_term_view)

        self.setLayout(layout_h)

    def _init_signals(self):
        # Inner interaction logic:
        self.term_editor.signal_term_was_changed.connect(self._stopped_editing)
        self.term_editor.signal_stopped_editing_new_term.connect(
            self._stopped_editing_new_term)
        self.term_editor.signal_current_term_is_valid.connect(
            self.act_view_term.setEnabled)
        self.term_editor.signal_current_term_is_valid.connect(
            self.act_add_term.setEnabled)

        self.term_str_browser.str_selected.connect(self._change_term)
        self.related_terms.link_selected.connect(self._change_term)
        self.term_str_browser.list_is_empty.connect(self.reset)

        # Delegate file to os default app:
        self.term_display.signal_link_clicked.connect(
            self.open_in_desktop_default_app)
