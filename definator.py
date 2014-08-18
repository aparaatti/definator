# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
__author__ = "Niko Humalamäki"
__version__ = "0.0.1"

import sys
import src.qdefinator_gui

if __name__ == "__main__":
    app = src.qdefinator_gui.QApplication(sys.argv)
    form = src.qdefinator_gui.MainWindow()
    form.show()
    app.exec()
