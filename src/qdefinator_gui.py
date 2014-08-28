# -*- coding: utf-8 -*-
#
# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QLabel, QMainWindow, QFrame, QMessageBox, \
    QErrorMessage, QFileDialog

from pathlib import Path
from copy import deepcopy

from .data.term import Term
from .main_widget import MainWidget
from .terms_controller import TermsController
from .qdefinator_gui_helpers import MainWindowHelper

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

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self._current_term = None
        self.terms_controller = TermsController()

        self.q_error_message = QErrorMessage(self)

        self.main_widget = MainWidget()
        self.menu = MainWindowHelper.make_menu(self.menuBar())
        MainWindowHelper.make_actions(self)
        MainWindowHelper.init_event_listeners(self)

        self.setWindowTitle(
            self.terms_controller.project_name + " - Definator v. " + __ver__
        )

        self.setCentralWidget(self.main_widget)

        self.size_label = QLabel()
        self.size_label.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)

        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.addPermanentWidget(self.size_label)
        status.showMessage("Ready", 5000)

    @pyqtSlot(Term)
    def update_term(self, term: Term):
        self.terms_controller.update_term(term)
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

    def remove_current_term(self):
        self.remove_term(self._current_term)


    @pyqtSlot(str)
    def get_term(self, term_str: str):
        self._current_term = self.terms_controller.get_term(term_str)
        self.signal_current_term.emit(self._current_term)

    @pyqtSlot(Term, Term)
    def link_term(self, term1: Term=None, term2: Term=None):
        self.statusBar().showMessage("linkTerm triggered", 2000)

    @pyqtSlot(Term, Term)
    def unlink_term(self, term1=None, term2=None):
        self.statusBar().showMessage("unlinkTerm triggered", 2000)

    def create_a_new_project(self):
        if self.terms_controller.unsaved_changes:
            save = QMessageBox.question(
                self, "QMessageBox.question()",
                "There are unsaved changes in the current project!"
                + " Do you want to save the project?",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if save:
                self.save_project()

        self.statusBar().showMessage("newProject triggered", 2000)

    def open_project(self):
        project_path = self.choose_a_folder()
        if project_path is not Path(""):
            self._intialize_project(project_path)

    def choose_a_folder(self):
        options = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        string = QFileDialog.getExistingDirectory(
            self,
            "QFileDialog.getExistingDirectory()",
            "Choose a directory.",
            options=options)

        return Path(string)


    def _intialize_project(self, project_path):
        try:
            list_of_terms = self.terms_controller.load_project(project_path)
        except FileNotFoundError:
            MainWindowHelper.warning_dialog(
                "Could not open.",
                "Could not open project from " + str(project_path) + ".")
            return

        self.setWindowTitle(
            self.terms_controller.project_name
            + " - " + "Definator " + __ver__)
        self.signal_opened_a_project.emit(
            list_of_terms, self.terms_controller.get_term(list_of_terms[0]))

    def _initialize_new_project(self):
        self.terms_controller = TermsController()
        self.setWindowTitle(
            self.terms_controller.project_name
            + " - " + "Definator " + __ver__)
        self.main_widget.reset()

    def save_project(self):
        if self.terms_controller.project_path == Path(""):
            self.save_project_as()
        else:
            self.terms_controller.save_project()

    def save_project_as(self):
        self.terms_controller.save_project_as(self.choose_a_folder())
