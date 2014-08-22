from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton


class DefinatorButton(QWidget):
    button_clicked = pyqtSignal()

    def __init__(self, text: str, parent=None):
        super(DefinatorButton, self).__init__(parent)

        self.layout = QVBoxLayout(self)
        self.button = QPushButton(self)
        self.button.setObjectName("button" + text)
        self.layout.addWidget(self.button)
        self.button.clicked.connect(self.button_clicked_emit)

    @pyqtSlot()
    def button_clicked_emit(self):
        self.button_clicked.emit()