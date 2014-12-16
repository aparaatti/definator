#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
# "Road map":
# TODO: All menu items
#   -settings
#      -language
#       -remember opened projects
#       -load last opened project on startup
#       -colors of files in linked things
# TODO Later:
#   -Generic tag class, that can be used to define a tag and html
#    representation for it.
#   -term browser in side pane (QDockWidget).
#   -File copy doesn't work on windows (?)
#   -Maybe open terms in tabs, with editor/term --> proper undo/redo
#   -Writing of unit tests
#   -Add list of synonymous terms to a term.
#   -show tags bold on term editor, show references to images bold on term
#       display
#   -maybe different types of links for terms (sub term, parent term)
#   -Use python built in serialization/de serialization for saving stuff
#   -Warn user when removing a term that also the linked files in term folder
#   will be deleted.
#
# RE FACTOR:
#   -TermDisplay to HtmlDisplay
#
import sys
import os
import logging
import argparse

import PyQt5
from PyQt5.QtCore import QTextCodec
import src.qdefinator_gui


# We set the working directory to the definator.py location
os.chdir(os.path.dirname(__file__))
aparser = argparse.ArgumentParser(description="Define some terms.")
aparser.add_argument('--log', '-l', action='count',
                     help='Enable logging to "definator.log" file')

if aparser.parse_args().log:
    log_file = open('definator.log', 'w')
    log_file.truncate()
    log_file.close()

    FORMAT = '%(msecs)d [%(module)s] %(levelname)s %(message)s'
    logging.basicConfig(
        filename='definator.log', level=logging.DEBUG, format=FORMAT,
        datefmt='%y.%m.%d %I:%M:%S')
else:
    logging.disable(logging.INFO)


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
