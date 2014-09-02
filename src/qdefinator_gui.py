# -*- coding: utf-8 -*-
#
# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtGui import QKeySequence, QIcon
from PyQt5.QtWidgets import QLabel, QMainWindow, QFrame, QMessageBox, \
    QErrorMessage, QFileDialog, QAction, QShortcut

from pathlib import Path

from .data.term import Term
from .main_widget import MainWidget
from .terms_controller import TermsController

__author__ = "Niko Humalamäki"
__ver__ = "0.001"


class MainWindow(QMainWindow):
    """
    Contains MainWidget.

    Handles interaction with backend.
    """
    signal_current_term = pyqtSignal(Term)
    signal_added_a_term = pyqtSignal(Term)
    signal_updated_a_term = pyqtSignal(Term)
    signal_removed_a_term = pyqtSignal(Term)

    signal_opened_a_project = pyqtSignal(list, Term)
    signal_started_a_new_project = pyqtSignal()

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self._current_term = None
        self.terms_controller = TermsController()
        self.main_widget = MainWidget()
        self._initialize_new_project()

        self.q_error_message = QErrorMessage(self)

        self.menu = self._make_menu()
        self._make_actions()
        self._init_event_listeners()

        self.setCentralWidget(self.main_widget)

        self.size_label = QLabel()
        self.size_label.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)

        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.addPermanentWidget(self.size_label)
        status.showMessage("Ready", 5000)

    def _make_menu(self):
        menu_bar = self.menuBar()
        menu = dict()
        menu["file"] = menu_bar.addMenu("&File")
        menu["edit"] = menu_bar.addMenu("&Edit")
        menu["term"] = menu_bar.addMenu("&Term")
        menu["help"] = menu_bar.addMenu("&Help")
        return menu

    def _make_actions(self):
        action_new_project = make_action_helper(
            self, "&New project", "Create a new project", QKeySequence.New)
        action_open_project = make_action_helper(
            self, "&Open project", "Open a project", QKeySequence.Open)
        action_save_project = make_action_helper(
            self, "&Save project", "Save the project", QKeySequence.Save)
        action_save_project_as = make_action_helper(
            self, "Save project &As...",
            "Save project as...", QKeySequence.Save)

        action_new_project.triggered.connect(self._create_a_new_project)
        action_open_project.triggered.connect(self._open_project)
        action_save_project.triggered.connect(self._save_project)
        action_save_project_as.triggered.connect(self._save_project_as)

        self.menu["file"].addAction(action_new_project)
        self.menu["file"].addAction(action_open_project)
        self.menu["file"].addAction(action_save_project)
        self.menu["file"].addAction(action_save_project_as)

        action_link_term = make_action_helper(
            self, "&Link terms", "Link terms to current term", "alt+l")
        action_link_term.triggered.connect(self.link_terms)
        action_rem_term = make_action_helper(
            self, "&Remove term", "Remove current term", "del")
        action_rem_term.triggered.connect(self._remove_current_term)

        self.menu["term"].addAction(action_rem_term)
        self.menu["term"].addAction(action_link_term)

    def _init_event_listeners(self):
        """
        Here is the main signaling action of the application.
        """
        #Selection of term and saving of terms signals map here,
        #because TermsController handles them.
        self.main_widget.term_str_selected.connect(self.get_term)
        self.main_widget.save_changes.connect(self._save_project)
        self.main_widget.remove_term.connect(self.remove_term)

        #When new term is added, we give it to termsController and update Main
        #Widget
        self.main_widget.add_new_term.connect(self.add_term)
        self.main_widget.update_term.connect(self.update_term)
        self.main_widget.add_links_to_term.connect(self.link_terms)
        self.main_widget.remove_links_from_term.connect(self.unlink_terms)

        #When term content has changed, we update the term to termController
        #and pass updated term to MainWidget:
        self.signal_updated_a_term.connect(self.main_widget.term_has_been_updated)

        #MainWidget handles changing and updating the term to it's components:
        #self.main_widget.current_term_updated.connect(self.update_term)
        self.signal_current_term.connect(self.main_widget.change_term)
        self.signal_opened_a_project.connect(self.main_widget.initialize_a_project)
        self.signal_added_a_term.connect(self.main_widget.added_a_term)
        self.signal_removed_a_term.connect(self.main_widget.term_has_been_removed)
        self.signal_started_a_new_project.connect(self.main_widget.reset)

    def _initialize_project(self, project_path):
        try:
            list_of_terms = self.terms_controller.load_project(project_path)
        except FileNotFoundError:
            self._warning_dialog(
                "Could not open.",
                "Could not open project from " + str(project_path) + ".")
            return

        self.setWindowTitle(
            self.terms_controller.project_name
            + " - " + "Definator " + __ver__)
        self.signal_opened_a_project.emit(
            list_of_terms, self.terms_controller.get_term(list_of_terms[0]))

    def _initialize_new_project(self):
        print("Initializing a new project...")
        self._current_term = None
        self.setWindowTitle(
            self.terms_controller.project_name + " - " + "Definator " + __ver__)
        self.signal_started_a_new_project.emit()

    def _create_a_new_project(self):
        if self.terms_controller.unsaved_changes:
            save = QMessageBox.question(
                self, "QMessageBox.question()",
                "There are unsaved changes in the current project!"
                + " Do you want to save the project?",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if save:
                self._save_project()

        self._initialize_new_project()

    def _open_project(self):
        project_path = self._choose_a_folder()
        if project_path is not Path(""):
            self._initialize_project(project_path)

    def _choose_a_folder(self):
        options = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        string = QFileDialog.getExistingDirectory(
            self,
            "QFileDialog.getExistingDirectory()",
            "Choose a directory.",
            options=options)

        return Path(string)

    def _warning_dialog(self, title: str, message: str):
        warning_message = QMessageBox(
            QMessageBox.Warning, title, message, QMessageBox.NoButton, self)
        warning_message.addButton("&Ok", QMessageBox.RejectRole)
        warning_message.exec_()

    def _save_project(self):
        if self.terms_controller.project_path == Path(""):
            self._save_project_as()
        else:
            self.terms_controller.save_project()

    def _save_project_as(self):
        self.terms_controller.save_project_as(self._choose_a_folder())

    def _remove_current_term(self):
        self.remove_term(self._current_term)

    @pyqtSlot(Term)
    def update_term(self, term: Term):
        #If the name of the term changed:
        if self.terms_controller.update_term(term):
            self.signal_removed_a_term.emit(Term(term.term_on_init))
            self.signal_added_a_term.emit(term)
        else:
            self.signal_updated_a_term.emit(term)

    @pyqtSlot(Term)
    def add_term(self, term: Term):
        if self.terms_controller.add_term(term):
            self._current_term = term
            self.signal_added_a_term.emit(term)

    @pyqtSlot(Term)
    def remove_term(self, term: Term):
        if self.terms_controller.remove_term(term):
            self.signal_removed_a_term.emit(term)

    @pyqtSlot(str)
    def get_term(self, term_str: str):
        self._current_term = self.terms_controller.get_term(term_str)
        self.signal_current_term.emit(self._current_term)

    @pyqtSlot(str, list)
    def link_terms(self, term_str: str, str_terms: list):
        if self.terms_controller.link_terms(term_str, str_terms):
            self.signal_updated_a_term.emit(
                self.terms_controller.get_term(term_str))

    @pyqtSlot(str, list)
    def unlink_terms(self, term_str: str, str_terms: list):
        if self.terms_controller.unlink_terms(term_str, str_terms):
            self.signal_updated_a_term.emit(
                self.terms_controller.get_term(term_str))


def make_action_helper(self, text, help_text, shortcut: QShortcut,
                       icon_path=None):
    """ Idea from "Rapid GUI Programming with Python and Qt" by Mark Summerfield
        Published:  Jun 2008
        Publisher:  Prentice Hall """
    if icon_path is not None:
        action = QAction(QIcon(icon_path), text, self)
    else:
        action = QAction(text, self)

    action.setShortcut(shortcut)
    action.setToolTip(help_text)
    action.setStatusTip(help_text)
    return action
