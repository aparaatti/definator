# -*- coding: utf-8 -*-
#
# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
# "Road map":
# TODO: Validation on term title field!
#      -can't exist already
#      -can't be empty
# TODO:
#   -dialog on save project as on what was moved and so on.
# TODO: linking
#   -make StrChooser to adjust its cols and line count on size change
#   -make StrChooser item draggable on term editor and drop text at drop location (tags)
#   -combine file and image linking (add file, rem file), add tag to end of editor when image is added.
# TODO: All menu items
#   -settings
# TODO: Settings:
#   -language
#   -remember opened projects
#   -load last opened project on startup
#   -colors of files in linked things
# TODO Later:
#   -Translations
#   -str-browser as own widget to left side and MainWidget contains term display and editor.
#   -Maybe open terms in tabs, with editor/term --> proper undo/redo
#   -Writing of unit tests
#   -Add list of synonymous terms to a term.
#   -show tags bold on term editor, show references to images bold on term display
# TODO: Use python built in serialization/deserialization for saving stuff
# TODO: Generic tag class, that can be used to define a tag and html representation for it.
# TODO: term browser in side pane (QDockWidget)
# TODO: File copy doesn't work on windows
# TODO: debug option on command line to turn on debug logging
#
# REFACTOR:
#   -termdisplay to htmldisplay
#
import sys
import os
import logging

import PyQt5
from PyQt5.QtCore import QTextCodec
import src.qdefinator_gui


#We set the working directory to the definator.py location
os.chdir(os.path.dirname(__file__))
log_file = open('definator.log', 'w')
log_file.truncate()
log_file.close()
logging.basicConfig(filename='definator.log', level=logging.DEBUG)


def run():
    QTextCodec.setCodecForLocale(QTextCodec.codecForName("utf-8"))
    app = PyQt5.QtWidgets.QApplication(sys.argv)

    logging.debug(os.curdir)
    app.setWindowIcon(PyQt5.QtGui.QIcon("definator.xpm"))
    form = src.qdefinator_gui.MainWindow()
    form.show()
    app.exec()

if __name__ == "__main__":
    run()
