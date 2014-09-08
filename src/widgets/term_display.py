# -*- coding: utf-8 -*-
#
# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QUrl
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWebKitWidgets import QWebPage

from ..data.term import Term
from .qtdesigner.ui_QTermDisplay import Ui_TermDisplay


class TermDisplay(QWidget):
    link_clicked = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_TermDisplay()
        self.ui.setupUi(self)
        self.ui.contentWebView.linkClicked.connect(self._map_to_signal)
        self.ui.contentWebView.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)

    @pyqtSlot(Term)
    def set_current_term(self, term: Term):
        self.ui.contentWebView.setHtml(term.term_as_html, QUrl("file://"))

    @pyqtSlot(QUrl)
    def _map_to_signal(self, url: QUrl):
        self.link_clicked.emit(url.toString())
