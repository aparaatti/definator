# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QPushButton, QWidget, QHBoxLayout

from ..data.term import Term
from .qtdesigner.ui_QTermEditor import Ui_TermEditor


class TermEditor(QWidget):
    stopped_editing = pyqtSignal(Term)
    stopped_editing_new_term = pyqtSignal(Term)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_TermEditor()
        self.ui.setupUi(self)
        self.ui.lineEditTitle.text = ""
        self._current_term = None

        #TODO Tähän tulee oma moduulinsa text dropper bar, jossa ikoni
        #jonka voi raahata tekstialueelle, jolloin alueelle tulee
        #tagi. Barista klikatessa pitäisi tagi tupsahtaa editorin viimeiselle
        #tyhjälle riville.

        #editori alue

        #TODO Tähän tulee klemmarin kuva, mistä voi liittää mitä tahansa
        # tiedostoja projektiin. edit modessa voi poistaa ja lisätä, view
        # modessa klikatessa antaa tiedoston polun jollekin joka päättelee minkä
        # tyyppisestä tiedostosta on kyse ja käsittelee sen sopivalla tavalla.
        # Aluksi voisi esim. avata tiedoston käyttöjärjestelmän
        # oletussovelluksella.

        #TODO Tästä tulee oma moduulinsa "String linker", sillä edit mode, jossa
        # voi lisätä linkkejä

        link_button_layout = QHBoxLayout()
        self.link_terms_button = QPushButton("Link terms", self)
        self.unlink_terms_button = QPushButton("Unlink terms", self)
        link_button_layout.addWidget(self.link_terms_button)
        link_button_layout.addWidget(self.unlink_terms_button)
        # end

        self.ui.verticalLayout.addLayout(link_button_layout)

    def set_term(self, term: Term):
        self._current_term = term
        self.ui.lineEditTitle.setText(term.term)
        self.ui.textEditContent.setText(term.description)

    def hide(self):
        if self._current_term is None:
            term = Term(self.ui.lineEditTitle.displayText())
            term.description = self.ui.textEditContent.toPlainText()
            self.ui.lineEditTitle.clear()
            self.ui.textEditContent.clear()
            self.stopped_editing_new_term.emit(term)
        else:
            self._current_term.term = self.ui.lineEditTitle.displayText()
            self._current_term.description = self.ui.textEditContent.toPlainText()
            self.stopped_editing.emit(self._current_term)
            self._current_term = None

        super().hide()

