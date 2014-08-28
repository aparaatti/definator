# -*- coding: utf-8 -*-
#
# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
# "Road map":
# TODO: removing of a term
# TODO: creation of new project
# TODO: linking of terms (dialog for linking, module to show linked terms=)
# TODO: split description text to description objects
#   TODO: handling of tags in text (Paragraph, Title)
#   TODO: buttons/icons to add tags
#   TODO: test that saving and loading works
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
#
from PyQt5.QtWidgets import QApplication
import sys
import src.qdefinator_gui

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = src.qdefinator_gui.MainWindow()
    form.show()
    app.exec()
