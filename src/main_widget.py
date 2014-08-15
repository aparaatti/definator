from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout

from .term_list import TermList
from .term_linker import TermLinker
from .term_display import TermDisplay


class MainWidget(QWidget):

    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

        self.termList = TermList()
        self.termLinker = TermLinker("Kissa")
        self.termDisplay = TermDisplay("kissa")
        self.title = QLabel("<h1>New project</h1>")
        self.title.setAlignment(Qt.AlignCenter)

        self.setMinimumSize(QSize(750, 200))

        layout = QVBoxLayout()
        layout_h = QHBoxLayout()
        layout_v = QVBoxLayout()

        layout.addWidget(self.title)
        layout_h.addWidget(self.termList)
        layout_v.addWidget(self.termDisplay)
        layout_v.addWidget(self.termLinker)

        layout_h.addLayout(layout_v)
        layout.addLayout(layout_h)

        self.setLayout(layout)
        self.termList.setFocus()
        #self.set_project_name("New project")

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    form = MainWidget()
    form.show()
    app.exec()
