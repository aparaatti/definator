#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
# "Road map":
# TODO: linking
#   -make StrChooser to adjust its cols and line count on size change
#   -make StrChooser item draggable on term editor and drop text at drop location (tags)
# TODO: All menu items
#   -settings
#      -language
#       -remember opened projects
#       -load last opened project on startup
#       -colors of files in linked things
# TODO Later:
#   -Generic tag class, that can be used to define a tag and html representation for it.
#   -term browser in side pane (QDockWidget).
#   -File copy doesn't work on windows (?)
#   -debug option on command line to turn on debug logging
#   -Maybe open terms in tabs, with editor/term --> proper undo/redo
#   -Writing of unit tests
#   -Add list of synonymous terms to a term.
#   -show tags bold on term editor, show references to images bold on term display
#   -maybe different types of links for terms (sub term, parent term)
#   -Use python built in serialization/deserialization for saving stuff
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
