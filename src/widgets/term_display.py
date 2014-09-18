# -*- coding: utf-8 -*-
#
# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QUrl
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWebKitWidgets import QWebPage
from PyQt5.QtGui import QKeySequence

from ..data.term import Term
from .qtdesigner.ui_QTermDisplay import Ui_TermDisplay
from .key_press_eater import KeyPressEater


class TermDisplay(QWidget):
    signal_link_clicked = pyqtSignal(str)

    signal_undo_event = pyqtSignal()
    signal_redo_event = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_TermDisplay()
        self.ui.setupUi(self)
        self.ui.contentWebView.linkClicked.connect(self._map_to_signal)
        self.ui.contentWebView.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)

        #Hook into undo/redo of term_editor
        self.eventFilter = KeyPressEater(QKeySequence.Undo, self)
        self.eventFilter2 = KeyPressEater(QKeySequence.Redo, self)
        self.installEventFilter(self.eventFilter)
        self.installEventFilter(self.eventFilter2)

    @pyqtSlot(Term)
    def set_term(self, term: Term):
        self.ui.contentWebView.setHtml(term.term_as_html, QUrl("file://"))

    @pyqtSlot(QUrl)
    def _map_to_signal(self, url: QUrl):
        self.signal_link_clicked.emit(url.toLocalFile().split("/")[-1])

    def _trigger_event(self, sequence: QKeySequence):
        if sequence is QKeySequence.Undo:
            self.signal_undo_event.emit()

        if sequence is QKeySequence.Redo:
            self.signal_redo_event.emit()
