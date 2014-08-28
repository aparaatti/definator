from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout

from .widgets.definator_button import DefinatorButton


class MainWidgetButtons(object):
    def __init__(self):
        self.edit_term = DefinatorButton("Edit")
        self.view_term = DefinatorButton("View")
        self.remove_term = DefinatorButton("Delete")
        self.edit_term.align_right()
        self.view_term.align_right()
        self.remove_term.align_right()
        self.add_term = DefinatorButton("Add term")
        self.add_term.center()
        #self.save_project = DefinatorButton("Save changes")
        #self.save_project.center()


class MainWidgetHelper(object):
    @staticmethod
    def make_layout(main_widget):
        layout_h = QHBoxLayout()
        layout_h2 = QHBoxLayout()

        layout_h_term_buttons = QHBoxLayout()
        layout_v_term_view = QVBoxLayout()
        layout_v_term_browser = QVBoxLayout()

        #Term browser area:
        layout_h.addLayout(layout_v_term_browser)
        layout_v_term_browser.addWidget(main_widget.term_str_browser)
        layout_v_term_browser.addWidget(main_widget.buttons.add_term)
        #layout_v_term_browser.addWidget(main_widget.buttons.save_project)

        #Term editor area:
        layout_h_term_buttons.addWidget(main_widget.buttons.edit_term)
        layout_h_term_buttons.addWidget(main_widget.buttons.view_term)
        layout_h_term_buttons.addWidget(main_widget.buttons.remove_term)
        main_widget.buttons.edit_term.hide()
        main_widget.buttons.remove_term.hide()

        layout_v_term_view.addLayout(layout_h_term_buttons)
        layout_v_term_view.addWidget(main_widget.term_editor)
        layout_v_term_view.addWidget(main_widget.term_display)
        main_widget.term_display.hide()
        #layout_v_term_view.addLayout(layout_h2)

        #Add editor area to browser layout
        layout_h.addLayout(layout_v_term_view)
        return layout_h
