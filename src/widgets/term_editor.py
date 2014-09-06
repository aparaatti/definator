# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
import os
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

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

    def _clear(self):
        self.ui.lineEditTitle.clear()
        self.ui.textEditContent.clear()
        self._current_term = None

    def set_term(self, term: Term):
        self._current_term = term
        if self._current_term is None:
            self._clear()
        else:
            self.ui.lineEditTitle.setText(term.term)
            self.ui.textEditContent.setText(term.description)

    def hide(self):
        if self._current_term is None:
            self.stopped_editing_new_term.emit(self._fill_term(Term()))
            self._clear()
        else:
            self._fill_term(self._current_term)
            self.stopped_editing.emit(self._current_term)
            self._clear()

        super().hide()

    def _fill_term(self, term: Term):
        term.term = self.ui.lineEditTitle.displayText()
        text = self.ui.textEditContent.toPlainText()
        white_space_removed = list()
        [white_space_removed.append(line.strip()) for line in text.splitlines()]
        term.description = os.linesep.join(white_space_removed)
        return term
