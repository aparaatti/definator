class Actions(object):
    @staticmethod
    def init_file_menu_actions(self, main_window, file_menu):
        action1 = make_action_helper(
            main_window, "&New project", "Create a new project", QKeySequence.New)
        action1.triggered.connect(self.create_a_new_project)
        file_menu.addAction(action1)

        action2 = make_action_helper(
            self, "&Open project", "Open a project", QKeySequence.Open)
        action2.triggered.connect(self.open_project)
        file_menu.addAction(action2)


    def init_term_menu_actions(self, term_menu):
        action2 = make_action_helper(
            self, "&Link term", "Link a term to current term", "alt+l")
        action2.triggered.connect(self.link_term)
        self.term_menu.addAction(action2)




def make_action_helper(self, text, help_text, Qshortcut, icon_path=None):
    """ Idea from "Rapid GUI Programming with Python and Qt" by Mark Summerfield
        Published:  Jun 2008
        Publisher:  Prentice Hall """
    if icon_path is not None:
        Action = QAction(QIcon(icon_path), text, self)
    else:
        Action = QAction(text, self)
    Action.setShortcut(QKeySequence.New)
    Action.setToolTip(help_text)
    Action.setStatusTip(help_text)
    return Action