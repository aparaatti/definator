from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton


class DefinatorButton(QWidget):
    def __init__(self, text: str, parent=None):
        super(DefinatorButton, self).__init__(parent)

        self.layout = QVBoxLayout(self)
        self.button = QPushButton(self)
        self.button.setObjectName("button" + text)
        self.layout.addWidget(self.button)
