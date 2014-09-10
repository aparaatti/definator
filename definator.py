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
#   -merge term linker into term editor
# TODO signal when editor has saveable term --> view button activation
# TODO: All menu items
#   -settings
# TODO: Translations
# TODO: Settings:
#   -language
#   -remember opened projects
#   -load last opened project on startup
#   -colors of files in linked things
# TODO Later:
#   -str-browser as own widget to left side and MainWidget contains term display and editor.
#   -Maybe open terms in tabs, with editor/term --> proper undo/redo
#   -Writing of unit tests
#   -Add list of synonymous terms to a term.
#   -show tags bold on term editor, show references to images bold on term display
# TODO: Use python built in serialization/deserialization for saving stuff
# TODO: Generic tag class, that can be used to define a tag and html representation for it.
#
# FIX: create new term when term str has changed!
# FIX: after removal of terms a term editor with last edited term is opened
#from PyQt5.QtWidgets import QApplication
import PyQt5
from PyQt5.QtCore import QTextCodec
import sys
import os
import src.qdefinator_gui


def run():
    QTextCodec.setCodecForLocale(QTextCodec.codecForName("utf-8"))
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    path = os.path.dirname(__file__)
    print(path)
    app.setWindowIcon(PyQt5.QtGui.QIcon(path + "/" + "definator.xpm"))
    form = src.qdefinator_gui.MainWindow()
    form.show()
    app.exec()

if __name__ == "__main__":
    run()
