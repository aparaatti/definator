# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QWidget, QSizePolicy


class DefinatorButton(QWidget):
    clicked = pyqtSignal()

    def __init__(self, text: str, parent=None):
        super(DefinatorButton, self).__init__(parent)
        self.initialized = False

        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        #sizePolicy.setHeightForWidth(QSizePolicy.hasHeightForWidth())

        self.layout = QVBoxLayout(self)
        self.button = QPushButton(self)
        self.button.setText(text)
        self.button.setSizePolicy(sizePolicy)
        self.button.setObjectName("button" + text)
        self.layout.addWidget(self.button)
        self.button.clicked.connect(self.button_clicked_emit)

    @pyqtSlot()
    def button_clicked_emit(self):
        self.clicked.emit()

    def align_right(self):
        self.layout.setAlignment(Qt.AlignRight)

    def center(self):
        self.layout.setAlignment(Qt.AlignCenter)

    def setEnabled(self, boolean: bool):
        self.button.setEnabled(boolean)
