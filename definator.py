#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
import sys
import os
import logging
import argparse

import PyQt5
from PyQt5.QtCore import QTextCodec
from PyQt5.QtWidgets import QApplication
from src import qdefinator_gui

app = None
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
    app = QApplication(sys.argv)

    logging.debug(os.curdir)
    app.setWindowIcon(PyQt5.QtGui.QIcon("definator.xpm"))
    form = qdefinator_gui.MainWindow()
    form.show()
    app.exec()

if __name__ == "__main__":
    run()
