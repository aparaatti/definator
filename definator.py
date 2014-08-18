__author__ = 'aparaatti'

import sys
import src.qdefinator_gui

if __name__ == "__main__":
    app = src.qdefinator_gui.QApplication(sys.argv)
    form = src.qdefinator_gui.MainWindow()
    form.show()
    app.exec()
