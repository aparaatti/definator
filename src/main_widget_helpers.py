from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout

from .widgets.definator_button import DefinatorButton


class MainWidgetButtons(object):
    def __init__(self):
        self.edit_term = DefinatorButton("Edit")
        self.view_term = DefinatorButton("View")
        self.edit_term.align_right()
        self.view_term.align_right()
        self.add_term = DefinatorButton("Add term")
        self.add_term.center()
        self.save_project = DefinatorButton("Save changes")
        self.save_project.center()
        self.edit_term.hide()


class MainWidgetHelper(object):
    @staticmethod
    def make_layout(main_widget):
        layout_h = QHBoxLayout()
        layout_h2 = QHBoxLayout()
        layout_v = QVBoxLayout()
        layout_v2 = QVBoxLayout()

        #Term browser area:
        layout_h.addLayout(layout_v2)
        layout_v2.addWidget(main_widget.term_str_browser)
        layout_v2.addWidget(main_widget.buttons.add_term)
        layout_v2.addWidget(main_widget.buttons.save_project)

        #Term editor area:
        layout_v.addWidget(main_widget.buttons.edit_term)
        layout_v.addWidget(main_widget.buttons.view_term)
        layout_v.addWidget(main_widget.term_display)
        layout_v.addWidget(main_widget.term_editor)
        main_widget.term_display.hide()
        layout_v.addLayout(layout_h2)

        #Add editor area to browser layout
        layout_h.addLayout(layout_v)
        return layout_h
