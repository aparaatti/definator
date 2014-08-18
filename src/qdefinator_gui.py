# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QKeySequence

from .main_widget import MainWidget
from .terms_controller import TermsController
from .helper_functions import *


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.__dirty = False
        self.__projectPath = "../../test-project/"
        self.__projectName = "Undefined"
        self.__currentTerm = None

        self.terms = TermsController()
        self.terms.project_path = self.__projectPath

        self.mainWidget = MainWidget()

        self._init_menu()
        self._init_actions()
        self._init_event_listeners()

        self.setCentralWidget(self.mainWidget)

        self.setWindowTitle(
            self.__projectName + " - " + "Definator " + __version__)

        self.sizeLabel = QLabel()
        self.sizeLabel.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.addPermanentWidget(self.sizeLabel)
        status.showMessage("Ready", 5000)

    def _init_menu(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.editMenu = self.menuBar().addMenu("&Edit")
        self.termMenu = self.menuBar().addMenu("&Term")
        self.helpMenu = self.menuBar().addMenu("&Help")

    def _init_actions(self):
        action = MakeActionHelper(
            self, "&New", "Create a new project",
            QKeySequence.New, ":/filenew.png")
        action.triggered.connect(self.newProject)
        self.fileMenu.addAction(action)
        action = MakeActionHelper(
            self, "&Link term", "Link a term to current term", "alt+l")
        action.triggered.connect(self.linkTerm)
        self.termMenu.addAction(action)

    def _init_event_listeners(self):
        #TermList:
        self.mainWidget.termList.termChanged.connect(self.change_term)
        self.mainWidget.termList.termChanged.connect(self.helloIWork)
        #self.mainWidget.termList.termAdded.connect(self.helloIWork)

        #TermLinker:
        self.mainWidget.termLinker.unlinkTermClicked.connect(self.helloIWork)
        self.mainWidget.termLinker.linkTermClicked.connect(self.helloIWork)
        #self.mainWidget.termLinker.termChanged.connect(self.helloIWork)

        #TermDisplay:
        #self.mainWidget.termDisplay.descriptionUpdated.connect(self.helloIWork)
        #self.mainWidget.termDisplay.fileAttached(self.helloIWork)

    def helloIWork(self, value="",value2=""):
        QMessageBox.information(self, str(self.sender()), str(value) + " " + str(value2))

    def change_term(self, sender, term):
        if not sender == "TermList":
            self.mainWidget.termList.set_current_term(term)

        if not sender == "TermLinker":
            self.mainWidget.termLinker.childAt(0, 0)

        self.mainWidget.termDisplay.setContent("kissa")

    def populateTerms(self):
        self.__currentTerm = None
        self.mainWidget.termList.clear()
        for term in self.terms:
            pass

    def newProject(self):
        self.statusBar().showMessage("newProject triggered", 2000)

    def linkTerm(self, term1=None, term2=None):
        self.statusBar().showMessage("linkTerm triggered", 2000)
        raise helper_functions.NotImplementedException(
            'Linking terms not implemented')

    def unlinkTerm(self, term1=None, term2=None):
        self.statusBar().showMessage("unlinkTerm triggered", 2000)
        raise helper_functions.NotImplementedException(
            'Unlinking terms not implemented')

    def termSelected(self, term="0"):
        self.statusBar().showMessage("termSelected triggered", 2000)
        #__currentTerm = term
        self.MainWidget.changeTerm(term)
        raise NotImplementedException(
            'Choosing terms not implemented')

    def termAdded(self, term="0"):
        self.statusBar().showMessage("add term triggered", 2000)
        raise helper_functions.NotImplementedException(
            'Adding terms not implemented')


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    app.exec()
