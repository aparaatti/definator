# -*- coding: utf-8 -*-
#
# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
import os
from pathlib import Path
from PyQt5.QtWidgets import QMainWindow, QLabel, QFrame, QErrorMessage, \
    QApplication, QFileDialog, QMessageBox

from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtGui import QKeySequence, QIcon

from .action_helper import make_action_helper
from .data.term import Term
from .main_widget import MainWidget
from .terms_controller import TermsController


__author__ = "Niko Humalamäki"
__ver__ = "0.01"


class MainWindow(QMainWindow):
    """
    Contains MainWidget.

    Handles interaction with backend.
    """
    #Signals informing about done actions:
    signal_current_term = pyqtSignal(Term)
    signal_added_a_term = pyqtSignal(Term)
    signal_updated_a_term = pyqtSignal(Term)
    signal_removed_a_term = pyqtSignal(Term)

    signal_opened_a_project = pyqtSignal(list, Term)
    signal_started_a_new_project = pyqtSignal()
    signal_project_saved = pyqtSignal()

    #Signals to command Gui widgets:
    signal_save_current_term = pyqtSignal()

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self._current_term = None
        self.terms_controller = TermsController()
        self.main_widget = MainWidget()
        self.q_error_message = QErrorMessage(self)

        self.menu = self._init_menu()
        self._make_actions()
        self._init_event_listeners()
        self._init_toolbar()

        self.setCentralWidget(self.main_widget)

        self.size_label = QLabel()
        self.size_label.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)

        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.addPermanentWidget(self.size_label)
        self._initialize_new_project()
        status.showMessage("Ready", 5000)

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

    def _create_a_new_project(self):
        if not self._check_for_unsaved_changes():
            return
        self._initialize_new_project()

    def _initialize_new_project(self):
        print("Initializing a new project...")
        self._current_term = None
        self.setWindowTitle(
            self.terms_controller.project_name + " - " + "Definator " + __ver__)
        self.signal_started_a_new_project.emit()

    def _check_for_unsaved_changes(self):
        if self.terms_controller.unsaved_changes:
            save = QMessageBox.question(
                self, "QMessageBox.question()",
                "There are unsaved changes in the current project!"
                + " Do you want to save the project?",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if save == QMessageBox.Yes:
                self._save_project()
            elif save == QMessageBox.Cancel:
                return False
        return True

    def _open_project(self):
        if not self._check_for_unsaved_changes():
            return
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

    def _show_about(self):
        QMessageBox.about(
            self, "About Definator",
            "Definator v. " + __ver__ + os.linesep + os.linesep +
            "Definator is intended to be useful for writing up definitions for terms. "
            "It can link them and attach files to them. "
            "It is mostly written as a tool for making up notes of concepts on a lecture "
            "and thus help creating a picture of a new topic. Definator can also "
            "be used for other purposes." +
            os.linesep + os.linesep +
            "Definator is licensed under GPLv3 and is written by " + __author__)

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
            self.signal_project_saved.emit()

    def _save_project_as(self):
        self.terms_controller.save_project_as(self._choose_a_folder())

    def _remove_current_term(self):
        self.remove_term(self.current_term)

    def _open_help(self):
        pass

    def _quit(self):
        if self._check_for_unsaved_changes():
            QApplication.quit()

    @pyqtSlot(Term)
    def update_term(self, term: Term):
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

    @pyqtSlot(str, str)
    def link_files(self, term_str: str, file_paths_str: list):
        if self.terms_controller.link_files(term_str, file_paths_str):
            self.signal_updated_a_term.emit(
                self.terms_controller.get_term(term_str))

    @pyqtSlot(str, list)
    def unlink_files(self, term_str: str, file_paths: list):
        if self.terms_controller.unlink_files(term_str, file_paths):
            self.signal_updated_a_term.emit(
                self.terms_controller.get_term(term_str))

    def _init_menu(self):
        menu_bar = self.menuBar()
        menu = dict()
        menu["file"] = menu_bar.addMenu("&File")
        menu["edit"] = menu_bar.addMenu("&Edit")
        menu["term"] = menu_bar.addMenu("&Term")
        menu["help"] = menu_bar.addMenu("&Help")
        return menu

    def _init_event_listeners(self):
        """
        Here is the main signaling action of the application.
        """
        #Selection of term and saving of terms signals map here,
        #because TermsController handles them.
        self.main_widget.term_str_selected.connect(self.get_term)
        self.main_widget.save_changes.connect(self._save_project)
        self.main_widget.remove_term.connect(self.remove_term)

        #When new term is added, we give it to termsController and update MainWidget
        self.main_widget.add_new_term.connect(self.add_term)
        self.main_widget.update_term.connect(self.update_term)

        #Link terms
        self.main_widget.add_links_to_term.connect(self.link_terms)
        self.main_widget.remove_links_from_term.connect(self.unlink_terms)

        #Add files
        self.main_widget.add_files_to_term.connect(self.link_files)
        self.main_widget.remove_files_from_term.connect(self.unlink_files)

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
        self.signal_project_saved.connect(self.main_widget.unmark)

    def _init_toolbar(self):
        self.toolBar = self.addToolBar("Main")
        self.toolBar.addAction(self.act_open_project)
        self.toolBar.addAction(self.act_save_project)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.main_widget.act_add_term)
        self.toolBar.addAction(self.main_widget.act_view_term)
        self.toolBar.addAction(self.main_widget.act_edit_term)
        self.toolBar.addAction(self.main_widget.act_rem_term)

    def _make_actions(self):
        self.act_new_project = make_action_helper(
            self, "&New project", "Create a new project", None, QIcon.fromTheme('document-new'))
        self.act_open_project = make_action_helper(
            self, "&Open project", "Open a project", QKeySequence.Open, QIcon.fromTheme('document-open'))
        self.act_save_project = make_action_helper(
            self, "&Save project", "Save the project", QKeySequence.Save, QIcon.fromTheme('document-save'))
        self.act_save_project_as = make_action_helper(self, "Save project &As...","Save project as...", QKeySequence.SaveAs, QIcon.fromTheme('document-save-as'))
        self.act_quit = make_action_helper(self, "Quit", "Exit application", QKeySequence.Quit, QIcon.fromTheme('application-exit'))
        self.act_quit.triggered.connect(self._quit)

        self.act_new_project.triggered.connect(self._create_a_new_project)
        self.act_open_project.triggered.connect(self._open_project)
        self.act_save_project.triggered.connect(self._save_project)
        self.act_save_project_as.triggered.connect(self._save_project_as)

        self.menu["file"].addAction(self.act_new_project)
        self.menu["file"].addAction(self.act_open_project)
        self.menu["file"].addSeparator()
        self.menu["file"].addAction(self.act_save_project)
        self.menu["file"].addAction(self.act_save_project_as)
        self.menu["file"].addSeparator()
        self.menu["file"].addAction(self.act_quit)

        self.menu["edit"].addAction(self.main_widget.act_undo)
        self.menu["edit"].addAction(self.main_widget.act_redo)

        self.menu["term"].addAction(self.main_widget.act_view_term)
        self.menu["term"].addAction(self.main_widget.act_edit_term)
        self.menu["term"].addAction(self.main_widget.act_add_term)
        self.menu["term"].addSeparator()
        self.menu["term"].addAction(self.main_widget.act_link_terms)
        self.menu["term"].addAction(self.main_widget.act_unlink_terms)
        self.menu["term"].addSeparator()
        self.menu["term"].addAction(self.main_widget.act_link_files)
        self.menu["term"].addAction(self.main_widget.act_unlink_files)
        self.menu["term"].addSeparator()
        self.menu["term"].addAction(self.main_widget.act_save_term)
        self.menu["term"].addAction(self.main_widget.act_rem_term)

        self.act_help = make_action_helper(self, "Open help...", "Open help", QKeySequence.HelpContents, QIcon.fromTheme('help-contents'))
        self.act_help.triggered.connect(self._open_help)
        self.act_show_about = make_action_helper(self, "&About", "About Definator", None, QIcon.fromTheme('help-about'))
        self.act_show_about.triggered.connect(self._show_about)
        self.act_about_qt = make_action_helper(self, "About &Qt", "About Qt framework")
        self.act_about_qt.triggered.connect(QApplication.instance().aboutQt)
        self.menu["help"].addAction(self.act_help)
        self.menu["help"].addSeparator()
        self.menu["help"].addAction(self.act_show_about)
        self.menu["help"].addAction(self.act_about_qt)
