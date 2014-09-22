# -*- coding: utf-8 -*-
#
# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
import os
import logging
from pathlib import Path

from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt
from PyQt5.QtGui import QKeySequence, QIcon, QCursor
from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication, QFileDialog, \
    QMessageBox, QStatusBar

from .widgets.qt_helper_functions import make_action_helper, warning_dialog, \
    info_dialog
from .data.term import Term
from .widgets.main_widget import MainWidget
from .terms_controller import TermsController


__author__ = "Niko Humalamäki"
__ver__ = "0.02"
__date__ = "22.9.2014"


class MainWindow(QMainWindow):
    """
    Contains MainWidget.

    Handles interaction with backend.
    """
    # Signals informing about done actions:
    signal_current_term = pyqtSignal(Term)
    signal_added_a_term = pyqtSignal(Term)
    signal_updated_a_term = pyqtSignal(Term)
    signal_removed_a_term = pyqtSignal(Term)

    signal_opened_a_project = pyqtSignal(list, Term)
    signal_started_a_new_project = pyqtSignal()
    signal_project_saved = pyqtSignal()
    signal_edit_term = pyqtSignal(Term)

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self._current_term = None

        self.terms_controller = TermsController()
        self.main_widget = MainWidget()
        self._init_settings()
        self.menu = self._init_menu()
        self._init_actions()
        self._init_event_listeners()
        self._init_toolbar()

        self.setCentralWidget(self.main_widget)

        self.term_count_label = QLabel()
        self.term_count_label.setMargin(5)

        self._create_a_new_project()
        QStatusBar()
        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.addPermanentWidget(self.term_count_label)
        status.showMessage("Ready", 5000)

    def _initialize_project(self, project_path):
        """
        This method initializes a project based on given project_path e.g.
        loads a project.
        """
        logging.debug("Initializing project from: " + str(project_path))
        try:
            list_of_terms = self.terms_controller.load_project(project_path)
        except FileNotFoundError:
            warning_dialog(
                self, "Could not open.",
                "Could not open project from " + str(project_path) + ".")
            return
        self._set_window_title()
        self._term_counter()
        self.signal_opened_a_project.emit(
            list_of_terms, self.terms_controller.get_term(list_of_terms[0]))

    def _set_window_title(self):
        """
        This method sets the title for window based on the name of the project
        root folder.
        """
        self.setWindowTitle(
            self.terms_controller.project_name + " - " + "Definator "
            + __ver__)

    def _create_a_new_project(self):
        """
        This method creates a new project and asks for saving changes if there
        are unsaved changes.
        """
        if not self._check_for_unsaved_changes():
            return
        logging.info("Initializing a new project...")
        self.signal_started_a_new_project.emit()
        self.terms_controller = TermsController()
        self._current_term = None
        self._set_window_title()
        self._term_counter()

    def _check_for_unsaved_changes(self):
        """
        This method checks if there are unsaved changes and asks if user
        wants to save them. If No is given, the changes are lost.

        :return: False if Cancel is given, True if No or Yes is given in the
            dialog.
        """
        if self.terms_controller.unsaved_changes:
            save = QMessageBox.question(
                self, "Unsaved changes",
                "There are unsaved changes in the current project!"
                + " Do you want to save the project?",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if save == QMessageBox.Yes:
                self._save_project()
            elif save == QMessageBox.Cancel:
                return False
        return True

    def _open_project(self):
        """
        This raises the open project dialog. If we get a path from dialog
        setting up of the project is delegated to _initialize_project() method.
        """
        if not self._check_for_unsaved_changes():
            return
        project_path = self._choose_a_folder()
        if project_path is not Path(""):
            self._initialize_project(project_path)

    def _save_project(self):
        """
        This method saves the project. If current project doesn't
        have a project_path saving is delegated to _save_project_as
        method.

        After saving an info dialog is shown, that tells that the project was
        saved.
        """
        if self.terms_controller.project_path == Path(""):
            self._save_project_as()
        else:
            self.terms_controller.save_project()
            self.signal_project_saved.emit()
            info_dialog(
                self, "Project saved", "Project saved at "
                + str(self.terms_controller.project_path) + ".")

    def _save_project_as(self):
        """
        This method saves the project to a new location. User chooses a folder
        with raised dialog. If the path from dialog is sane the project is
        saved and an information dialog is shown.
        """
        project_path = self._choose_a_folder()
        logging.debug("Project path on save: " + str(project_path))
        if project_path is not Path("."):
            self.terms_controller.save_project_as(project_path)
            self._set_window_title()
            info_dialog(
                self, "Project saved", "Project saved at " +
                str(self.terms_controller.project_path) + ".")
            self.signal_project_saved.emit()

    def _open_help(self):
        """
        This method opens the help documentation for the app.
        """
        # TODO disable saving edits for help project.
        logging.debug("Help fetch path: " + os.getcwd() + "/help-project")
        if self._check_for_unsaved_changes():
            self._initialize_project(Path(Path(os.getcwd() + "/help-project")))

    def _quit(self):
        """
        This method maps the quit action to actual quit. Before quitting
        it checks for unsaved changes.
        """
        if self._check_for_unsaved_changes():
            QApplication.quit()

    def closeEvent(self, event):
        """
        This method hooks into window being closed. Before
        the window is closed it is checked if there are
        unsaved changes.
        """
        if self._check_for_unsaved_changes():
            super().closeEvent(event)
        else:
            event.ignore()

    ############
    # DIALOGS: #
    ############
    def _choose_a_folder(self):
        """
        This method raises standard qt directory dialog
        """
        options = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        string = QFileDialog.getExistingDirectory(
            self,
            "QFileDialog.getExistingDirectory()",
            "Choose a directory.",
            options=options)

        return Path(string)

    def _show_about(self):
        """
        This method raises an message box showing some information on
        definator. It is triggered from act_show_about action.
        """
        QMessageBox.about(
            self, "About Definator", "Definator v. " + __ver__ + " (" +
            __date__ + ")" + os.linesep + os.linesep +
            "Definator is " +
            "intended to be useful for writing up definitions for terms. "
            "It can link them and attach files to them. "
            "It is mostly written to be a tool for making up notes of "
            + "concepts on a lecture and thus help creating a picture of a " +
            "new topic. Definator can also be used for other purposes." +
            os.linesep + os.linesep + "Definator is licensed under GPLv3 "
            + "and is written by " + __author__)

    ##################################
    # Slots for operations on terms: #
    ##################################
    @pyqtSlot(Term)
    def update_term(self, term: Term):
        """
        This slot delegates a term to TermsController to be updated.
        If TermsController updates the term signal_updated_a_term
        is emitted. If terms controller detects that the Term.term string of
        the term has changed signal_removed_a_term(Term.previous_term) is
        emitted and after that signal_added_a_term(term) is emitted.

        If an error happens, Runtime Error is excepted and a warning
        dialog is raised with the error message.

        :param: term: Term to update
        """
        try:
            if self.terms_controller.update_term(term):
                self.signal_removed_a_term.emit(term.previous_term)
                self.signal_added_a_term.emit(term)
            else:
                self.signal_updated_a_term.emit(term)
        except RuntimeError as re:
            warning_dialog(self, "Runtime error", re.message)

    @pyqtSlot(Term)
    def add_term(self, term: Term):
        """
        This slot delegates a received term to be added to TermsController term
        set. If term is added a signal_added_a_term(Term) is emitted. If the
        term could not be added a warning dialog is raised warning the user
        that the term already exists and signal_edit_term(Term) is emitted.
        """
        if self.terms_controller.add_term(term):
            self._current_term = term
            self.signal_added_a_term.emit(term)
            self._term_counter()
        else:
            warning_dialog(
                self, "Term already exists.", 'The term "' +
                term.term + '" already exists in the project.')
            self.signal_edit_term.emit(term)

    @pyqtSlot(Term)
    def remove_term(self, term_str: str):
        """
        This slots delegates received term_str to TermsController to be
        removed from its term set. If the removal succeeds
        **signal_removed_a_term(Term)** is emitted.

        :param: term_str: str Term.term of the Term object, that needs to be
            removed
        """
        if self.terms_controller.remove_term(term_str):
            self.signal_removed_a_term.emit(Term(term_str))
            self._term_counter()

    @pyqtSlot(str)
    def get_term(self, term_str: str):
        """
        This slot delegates fetching of the actual Term object
        for received term_str to TermsController. If TermsControlled succeeds
        **signal_current_term(Term)** is emitted.

        If Term corresponding the term_str is not found a warning_dialog
        is raised with information on missing Term.
        """
        try:
            term = self.terms_controller.get_term(term_str)
            self._current_term = term
            self.signal_current_term.emit(self._current_term)
        except KeyError:
            logging.warning("KeyError, No key: " + term_str)
            warning_dialog(
                self, "No such term", 'Current project does not have term "'
                + term_str + '".')

    @pyqtSlot(str, list)
    def link_terms(self, term: Term, str_terms: list):
        """
        This slot delegates linking of terms (received as string list) to
        a received Term object to TermsController. When linking is done
        signal_updated_a_term(Term) is emitted.

        """
        # TODO Maybe needs error handling?
        self.terms_controller.link_terms(term, str_terms)
        self.signal_updated_a_term.emit(term)

    @pyqtSlot(str, list)
    def unlink_terms(self, term: Term, str_terms: list):
        """
        This slot delegates unlinking of terms (received as string list)
        from a received Term object to TermsController. When unlinking
        is done signal_updated_a_term(Term) is raised.
        """
        # TODO Maybe needs error handling?
        self.terms_controller.unlink_terms(term, str_terms)
        self.signal_updated_a_term.emit(term)

    @pyqtSlot()
    def _term_counter(self):
        self.term_count_label.setText(
            "Term count: " + str(self.terms_controller.count))

    ###########################
    # Initialization methods: #
    ###########################
    def _init_settings(self):
        """
        Here are some settings deffering from the default Qt settings. These
        could be made configurable. Also the colors in StrBrowser and KeyList
        (set from TermEditor) could be made configurable.
        """
        self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.setCursor(QCursor(0))

    def _init_menu(self):
        """
        Here is the initialization of the menu. It is filled in _init_actions
        """
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
        # Selection of term and saving of terms signals map here,
        # because TermsController handles them.
        self.main_widget.term_str_selected.connect(self.get_term)
        self.main_widget.save_changes.connect(self._save_project)
        self.main_widget.remove_term.connect(self.remove_term)

        # When new term is added, we give it to termsController and update
        # MainWidget
        self.main_widget.add_new_term.connect(self.add_term)
        self.main_widget.update_term.connect(self.update_term)

        # Link terms, these has to be done at TermsController.
        self.main_widget.term_editor.add_links_to_term.connect(self.link_terms)
        self.main_widget.term_editor.remove_links_from_term.connect(
            self.unlink_terms)

        # When term content has changed, we update the term to termController
        # and pass updated term to MainWidget:
        self.signal_updated_a_term.connect(
            self.main_widget.term_has_been_updated)

        # MainWidget handles changing and updating the term to it's components:
        self.signal_current_term.connect(self.main_widget.change_term)
        self.signal_opened_a_project.connect(
            self.main_widget.initialize_a_project)
        self.signal_added_a_term.connect(self.main_widget.added_a_term)
        self.signal_added_a_term.connect(self._term_counter)
        self.signal_removed_a_term.connect(
            self.main_widget.term_has_been_removed)
        self.signal_started_a_new_project.connect(self.main_widget.reset)
        self.signal_project_saved.connect(self.main_widget.unmark)
        self.signal_edit_term.connect(self.main_widget.edit_current_term)

    def _init_actions(self):
        """
        All the actions are defined and/or bind here.
        Icon names for theme:

        standards.freedesktop.org/icon-naming-spec/icon-naming-spec-latest.html

        """
        self.act_new_project = make_action_helper(
            self, "&New project", "Create a &new project", None,
            QIcon.fromTheme('document-new'))
        self.act_open_project = make_action_helper(
            self, "&Open project", "&Open a project", QKeySequence.Open,
            QIcon.fromTheme('document-open'))
        self.act_save_project = make_action_helper(
            self, "&Save project", "Save the project", QKeySequence.Save,
            QIcon.fromTheme('document-save'))
        self.act_save_project_as = make_action_helper(
            self, "Save project &As...", "Save project as...",
            QKeySequence.SaveAs, QIcon.fromTheme('document-save-as'))
        self.act_quit = make_action_helper(
            self, "Quit", "Exit application", QKeySequence.Quit,
            QIcon.fromTheme('application-exit'))
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

        self.menu["edit"].addAction(self.main_widget.term_editor.act_copy)
        self.menu["edit"].addAction(self.main_widget.term_editor.act_paste)
        self.menu["edit"].addAction(self.main_widget.term_editor.act_cut)
        self.menu["edit"].addSeparator()
        self.menu["edit"].addAction(self.main_widget.term_editor.act_undo)
        self.menu["edit"].addAction(self.main_widget.term_editor.act_redo)

        self.menu["term"].addAction(self.main_widget.act_view_term)
        self.menu["term"].addAction(self.main_widget.act_edit_term)
        self.menu["term"].addAction(self.main_widget.act_add_term)
        self.menu["term"].addSeparator()
        self.menu["term"].addAction(self.main_widget.act_link_terms)
        self.menu["term"].addAction(self.main_widget.act_unlink_terms)
        self.menu["term"].addSeparator()
        self.menu["term"].addAction(
            self.main_widget.term_editor.act_link_files)
        self.menu["term"].addAction(
            self.main_widget.term_editor.act_unlink_files)
        self.menu["term"].addSeparator()
        self.menu["term"].addAction(self.main_widget.act_save_term)
        self.menu["term"].addAction(self.main_widget.act_rem_term)

        self.act_help = make_action_helper(
            self, "Open help...", "Open help",
            QKeySequence.HelpContents, QIcon.fromTheme('help-contents'))
        self.act_help.triggered.connect(self._open_help)
        self.act_show_about = make_action_helper(
            self, "&About", "About Definator", None,
            QIcon.fromTheme('help-about'))
        self.act_show_about.triggered.connect(self._show_about)
        self.act_about_qt = make_action_helper(self, "About &Qt",
                                               "About Qt framework")
        self.act_about_qt.triggered.connect(QApplication.instance().aboutQt)
        self.menu["help"].addAction(self.act_help)
        self.menu["help"].addSeparator()
        self.menu["help"].addAction(self.act_show_about)
        self.menu["help"].addAction(self.act_about_qt)

    def _init_toolbar(self):
        """
        Here is the building of the toolbar.
        """
        self.tool_bar_project = self.addToolBar("Project")
        self.tool_bar_project.addAction(self.act_open_project)
        self.tool_bar_project.addAction(self.act_save_project)
        self.tool_bar_project.addAction(self.act_new_project)

        self.tool_bar_add_rem_term = self.addToolBar("Term add/remove")
        self.tool_bar_add_rem_term.addAction(self.main_widget.act_add_term)
        self.tool_bar_add_rem_term.addAction(self.main_widget.act_rem_term)

        self.tool_bar_edit = self.addToolBar("Edit")
        self.tool_bar_edit.addAction(self.main_widget.term_editor.act_undo)
        self.tool_bar_edit.addAction(self.main_widget.term_editor.act_redo)

        self.addToolBarBreak()

        self.tool_bar_view_edit_term = self.addToolBar("Term view/edit")
        self.tool_bar_view_edit_term.addAction(self.main_widget.act_view_term)
        self.tool_bar_view_edit_term.addAction(self.main_widget.act_edit_term)

        self.tool_bar_link_terms = self.addToolBar("Link terms")
        self.tool_bar_link_terms.addAction(self.main_widget.act_link_terms)
        self.tool_bar_link_terms.addAction(self.main_widget.act_unlink_terms)

        self.tool_bar_link_files = self.addToolBar("Link files")
        self.tool_bar_link_files.addAction(
            self.main_widget.term_editor.act_link_files)
        self.tool_bar_link_files.addAction(
            self.main_widget.term_editor.act_unlink_files)
