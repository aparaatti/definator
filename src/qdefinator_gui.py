# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QLabel, QMainWindow, QFrame
from PyQt5.QtGui import QKeySequence

from pathlib import Path
from copy import deepcopy

from .data.term import Term
from .main_widget import MainWidget
from .terms_controller import TermsController
from .qute_helper_functions import *

__author__ = "Niko Humalamäki"
__version__ = "0.001"


class MainWindow(QMainWindow):
    """
    MainWindow counts on the fact that parameter self._current_term_unmodified represents always
    the term before any changes made to it. The modules that modifie the terms are supposed
    to deepcopy the term and signal it back when editing is done.

    So the self._current_term_unmodified should always represent the term which is being edited and
    signals should always return the right term.
    """
    # TODO change all camel case method names and parameters to _ separated names
    signal_current_term = pyqtSignal(Term)
    signal_added_a_term = pyqtSignal(Term)
    signal_updated_a_term = pyqtSignal()

    # Event sent when TermsController has opened a new project
    #tuple contains list of terms and Term is the term to show at first eg.
    #first term in tuple.
    signal_opened_a_project = pyqtSignal(list, Term)

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self._current_term_unmodified = None
        self.terms_controller = TermsController()
        self.qerror_message = QErrorMessage(self)

        self.main_widget = MainWidget()
        self._init_menu()
        self._init_actions()
        self._init_event_listeners()
        self.setWindowTitle(
            self.terms_controller.project_name
            + " - Definator v. " + __version__
        )

        self.setCentralWidget(self.main_widget)

        self.size_label = QLabel()
        self.size_label.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)

        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.addPermanentWidget(self.size_label)
        status.showMessage("Ready", 5000)

    def _init_menu(self):
        self.file_menu = self.menuBar().addMenu("&File")
        self.edit_menu = self.menuBar().addMenu("&Edit")
        self.term_menu = self.menuBar().addMenu("&Term")
        self.help_menu = self.menuBar().addMenu("&Help")

    def _init_actions(self):
        action1 = make_action_helper(
            self, "&New project", "Create a new project", QKeySequence.New)
        action1.triggered.connect(self.create_a_new_project)
        self.file_menu.addAction(action1)

        action2 = make_action_helper(
            self, "&Link term", "Link a term to current term", "alt+l")
        action2.triggered.connect(self.link_term)
        self.term_menu.addAction(action2)

        action3 = make_action_helper(
            self, "&Open project", "Open a project", QKeySequence.Open)
        action3.triggered.connect(self.open_project)
        self.file_menu.addAction(action3)

    def _init_event_listeners(self):
        """
        Here is the main signaling action of the application.
        """
        #Selection of term and saving of terms signals map here,
        #because TermsController handles them.
        self.main_widget.term_str_selected.connect(self.change_term)
        self.main_widget.save_changes.connect(self.save_project)

        #When new term is added, we give it to termsController and update Main
        #Widget
        self.main_widget.add_new_term.connect(self.add_term)

        #When term content has changed, we update the term to termController
        #and pass updated term to MainWidget:
        self.signal_updated_a_term.connect(self.main_widget.update_term)

        #MainWidget handles changing and updating the term to it's components:
        #self.main_widget.current_term_updated.connect(self.update_term)
        self.signal_current_term.connect(self.main_widget.change_term)
        self.signal_opened_a_project.connect(self.main_widget.opened_a_new_project)
        self.signal_added_a_term.connect(self.main_widget.added_a_term)

    @pyqtSlot(Term)
    def update_term(self, term: Term):
        if self.terms_controller.update_term(self._current_term_unmodified, term):
            self.signal_updated_a_term.emit(term)

    @pyqtSlot(Term)
    def add_term(self, term: Term):
        if self.terms_controller.add_term(term):
            self.signal_added_a_term.emit(term)

    @pyqtSlot(str)
    def change_term(self, term_str: str):
        ct = self.terms_controller.get_term(term_str)
        if ct is not None:
            self._current_term_unmodified = ct

        self.signal_current_term.emit(deepcopy(self._current_term_unmodified))

    def link_term(self, term1=None, term2=None):
        self.statusBar().showMessage("linkTerm triggered", 2000)

    def unlink_term(self, term1=None, term2=None):
        self.statusBar().showMessage("unlinkTerm triggered", 2000)

    def create_a_new_project(self):
        if self.terms_controller.unsaved_changes:
            save = QMessageBox.question(self, "QMessageBox.question()",
                "There are unsaved changes in the current project! Do you want to save the project?",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if save:
                self.save_project()

        self.statusBar().showMessage("newProject triggered", 2000)

    def open_project(self):
        options = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        string = QFileDialog.getExistingDirectory(
            self,
            "QFileDialog.getExistingDirectory()",
            "Choose a directory.",
            options=options)
        print(str(type(string)) + " " + str(string))
        project_path = Path(string)
        print("project_path on open: " + str(project_path))

        if project_path is not Path(""):
            self._intialize_project(project_path)

    def _intialize_project(self, project_path: Path):
        try:
            list_of_terms = self.terms_controller.load_project(project_path)
        except FileNotFoundError as e:
            self.qerror_message.showMessage("Could not open project from " + str(project_path) + ". " + str(e))
            return

        self.setWindowTitle(self.terms_controller.project_name + " - " + "Definator " + __version__)
        self.signal_opened_a_project.emit(list_of_terms, self.terms_controller.get_term(list_of_terms[0]))

    def save_project(self):
        if self.terms_controller.project_path == Path(""):
            self.warning_dialog("Not implemented", "Saving a new project... but it's not implemented!")
        else:
            self.terms_controller.save_project()

    def warning_dialog(self, title: str, message: str):
        warning_message = QMessageBox(QMessageBox.Warning, title,
        message, QMessageBox.NoButton, self)
        warning_message.addButton("&Ok", QMessageBox.RejectRole)
        warning_message.exec_()