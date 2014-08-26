from PyQt5.QtGui import QKeySequence, QIcon
from PyQt5.QtWidgets import QAction

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
    def make_actions(main_window):
        action_new_project = make_action_helper(
            main_window,
            "&New project",
            "Create a new project",
            QKeySequence.New)
        action_new_project.triggered.connect(main_window.create_a_new_project)

        action_link_term = make_action_helper(
            main_window,
            "&Link term",
            "Link a term to current term",
            "alt+l")
        action_link_term.triggered.connect(main_window.link_term)

        action_open_project = make_action_helper(
            main_window,
            "&Open project",
            "Open a project",
            QKeySequence.Open)
        action_open_project.triggered.connect(main_window.open_project)

        main_window.menu["file"].addAction(action_new_project)
        main_window.menu["term"].addAction(action_link_term)
        main_window.menu["file"].addAction(action_open_project)

    @staticmethod
    def init_event_listeners(main_window):
        """
        Here is the main signaling action of the application.
        """
        #Selection of term and saving of terms signals map here,
        #because TermsController handles them.
        main_window.main_widget.term_str_selected.connect(main_window.get_term)
        main_window.main_widget.save_changes.connect(main_window.save_project)

        #When new term is added, we give it to termsController and update Main
        #Widget
        main_window.main_widget.add_new_term.connect(main_window.add_term)
        main_window.main_widget.update_term.connect(main_window.update_term)

        #When term content has changed, we update the term to termController
        #and pass updated term to MainWidget:
        main_window.signal_updated_a_term.connect(
            main_window.main_widget.term_has_been_updated)

        #MainWidget handles changing and updating the term to it's components:
        #self.main_widget.current_term_updated.connect(self.update_term)
        main_window.signal_current_term.connect(
            main_window.main_widget.change_term)
        main_window.signal_opened_a_project.connect(
            main_window.main_widget.initialize_a_project)
        main_window.signal_added_a_term.connect(
            main_window.main_widget.added_a_term)


def make_action_helper(self, text, help_text, Qshortcut, icon_path=None):
    """ Idea from "Rapid GUI Programming with Python and Qt" by Mark Summerfield
        Published:  Jun 2008
        Publisher:  Prentice Hall """
    if icon_path is not None:
        action = QAction(QIcon(icon_path), text, self)
    else:
        action = QAction(text, self)

    action.setShortcut(QKeySequence.New)
    action.setToolTip(help_text)
    action.setStatusTip(help_text)
    return action
