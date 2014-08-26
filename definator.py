# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
from PyQt5.QtWidgets import QApplication
import sys
import src.qdefinator_gui

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = src.qdefinator_gui.MainWindow()
    form.show()
    app.exec()
