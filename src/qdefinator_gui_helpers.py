# -*- coding: utf-8 -*-
#
# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
from PyQt5.QtGui import QKeySequence, QIcon
from PyQt5.QtWidgets import QAction, QShortcut


class MainWindowHelper(object):
    @staticmethod
    def make_menu(menu_bar):
        menu = dict()
        menu["file"] = menu_bar.addMenu("&File")
        menu["edit"] = menu_bar.addMenu("&Edit")
        menu["term"] = menu_bar.addMenu("&Term")
        menu["help"] = menu_bar.addMenu("&Help")
        return menu

    @staticmethod
    def make_actions(mw):
        action_new_project = make_action_helper(mw, "&New project", "Create a new project", QKeySequence.New)
        action_open_project = make_action_helper(mw, "&Open project", "Open a project", QKeySequence.Open)
        action_save_project = make_action_helper(mw, "&Save project", "Save the project", QKeySequence.Save)
        action_save_project_as = make_action_helper(mw, "&Save project_as...", "Save project to...", QKeySequence.Save)
        action_new_project.triggered.connect(mw.create_a_new_project)
        action_open_project.triggered.connect(mw.open_project)
        action_save_project.triggered.connect(mw.save_project)
        action_save_project_as.triggered.connect(mw.save_project_as)

        mw.menu["file"].addAction(action_new_project)
        mw.menu["file"].addAction(action_open_project)
        mw.menu["file"].addAction(action_save_project)
        mw.menu["file"].addAction(action_save_project_as)

        action_link_term = make_action_helper(
            mw, "&Link terms", "Link terms to current term", "alt+l")
        action_link_term.triggered.connect(mw.link_term)
        action_rem_term = make_action_helper(
            mw, "&Remove term", "Remove current term", "del")
        action_rem_term.triggered.connect(mw.remove_current_term)

        mw.menu["term"].addAction(action_rem_term)
        mw.menu["term"].addAction(action_link_term)

    @staticmethod
    def init_event_listeners(mw):
        """
        Here is the main signaling action of the application.
        """
        #Selection of term and saving of terms signals map here,
        #because TermsController handles them.
        mw.main_widget.term_str_selected.connect(mw.get_term)
        mw.main_widget.save_changes.connect(mw.save_project)
        mw.main_widget.remove_term.connect(mw.remove_term)

        #When new term is added, we give it to termsController and update Main
        #Widget
        mw.main_widget.add_new_term.connect(mw.add_term)
        mw.main_widget.update_term.connect(mw.update_term)

        #When term content has changed, we update the term to termController
        #and pass updated term to MainWidget:
        mw.signal_updated_a_term.connect(mw.main_widget.term_has_been_updated)

        #MainWidget handles changing and updating the term to it's components:
        #self.main_widget.current_term_updated.connect(self.update_term)
        mw.signal_current_term.connect(mw.main_widget.change_term)
        mw.signal_opened_a_project.connect(mw.main_widget.initialize_a_project)
        mw.signal_added_a_term.connect(mw.main_widget.added_a_term)
        mw.signal_removed_a_term.connect(mw.main_widget.term_has_been_removed)
        mw.signal_started_a_new_project.connect(mw.main_widget.reset)


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
