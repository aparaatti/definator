# -*- coding: utf-8 -*-
#
# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
# "Road map":
# TODO: split description text to description objects
#   TODO: handling of tags in text (Paragraph, Title)
#   TODO: buttons/icons to add tags
#   TODO: test that saving and loading works
# TODO: Make linking UI:s pretty
#   TODO: attached files could be just read from the content of term folder!
# TODO: All menu items
#   -copy/paste
#   -about, help
#   -setting?
# TODO: Translations
# TODO: linking of files
# TODO: tagging images to text (ImagePath)
#   TODO: test that saving and loading of links works
#
# TODO Later:
#       str-browser as own widget to left side and MainWidget contains term
#           display and editor.
#       Maybe open terms in tabs, with editor/term --> proper undo/redo
#       Save term (ctrl + s) + save project + save project as
#       Writing unit tests
#       utf8 problem with QLineEdit in TermEditor!
#
# Monikielisyys --> tulisi kolmonen
# Joku asetus esim. kielen vaihto?
#
from PyQt5.QtWidgets import QApplication
import sys
import src.qdefinator_gui

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = src.qdefinator_gui.MainWindow()
    form.show()
    app.exec()
