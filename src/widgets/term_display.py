# -*- coding: utf-8 -*-
#
# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
from pathlib import Path
from PyQt5.QtCore import pyqtSlot, QUrl
from PyQt5.QtWidgets import QWidget

from ..data.term import Term
from .qtdesigner.ui_QTermDisplay import Ui_TermDisplay


class TermDisplay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_TermDisplay()
        self.ui.setupUi(self)

    @pyqtSlot(Term)
    def set_current_term(self, term: Term):
        self.ui.contentWebView.setHtml(term.term_as_html, QUrl("file://"))
