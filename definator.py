# -*- coding: utf-8 -*-
#
# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
# "Road map":
# TODO: linking
#   -make StrChooser to adjust its cols and line count on size change
#   -make StrChooser item draggable on term editor and drop text at drop location (tags)
#   -combine file and image linking (add file, rem file), add tag to end of editor when image is added.
# TODO signal when editor has saveable term --> view button activation
# TODO: All menu items
#   -Save term (ctrl + s) + save project + save project as
#   -copy/paste
#   -about, help
#   -settings
# TODO: Translations
# TODO: Settings:
#   -language
#   -remember opened projects
#   -load last opened project on startup
# TODO: Make linking UI:s better (combine to term editor)
#   -Files and images as list on the term display
#   -Files and images as separate web display on term editor
#   -buttons/icons to add tags
# TODO Later:
#   -str-browser as own widget to left side and MainWidget contains term display and editor.
#   -Maybe open terms in tabs, with editor/term --> proper undo/redo
#   -Writing of unit tests
#   -Add list of synonymous terms to a term.
#   -show tags bold on term editor, show references to images bold on term display
# TODO: Use python built in serialization/deserialization for saving stuff
#
from PyQt5.QtWidgets import QApplication
import sys
import src.qdefinator_gui

def run():
    app = QApplication(sys.argv)
    form = src.qdefinator_gui.MainWindow()
    form.show()
    app.exec()

if __name__ == "__main__":
    run()
