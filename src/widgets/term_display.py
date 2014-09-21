# -*- coding: utf-8 -*-
#
# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
import logging

from PyQt5.QtCore import pyqtSignal, pyqtSlot, QUrl
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWebKitWidgets import QWebPage
from PyQt5.QtGui import QKeySequence

from ..data.term import Term
from .qtdesigner.ui_QTermDisplay import Ui_TermDisplay
from .key_press_eater import KeyPressEater


class TermDisplay(QWidget):
    """
    This widget displays the html presentations of Term objects.
    """
    signal_link_clicked = pyqtSignal(str)

    signal_undo_event = pyqtSignal()
    signal_redo_event = pyqtSignal()

    def __init__(self, parent=None):
        self._html = ""
        super().__init__(parent)
        self.ui = Ui_TermDisplay()
        self.ui.setupUi(self)
        self.ui.contentWebView.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
        self.ui.contentWebView.linkClicked.connect(self._map_to_signal)

    @pyqtSlot(Term)
    def set_term(self, term: Term):
        """
        This slot sets the term to display.
        """
        self._html = term.term_as_html
        self.ui.contentWebView.setHtml(term.term_as_html, QUrl("file://"))

    @pyqtSlot(QUrl)
    def _map_to_signal(self, url: QUrl):
        """
        This slot delegates clicked link signal to show the same html as
        before (eg. link to a point in the term has been clicked)
        or to delegate the filename given in the link as emitted
        signal_link_clicked(filename) signal.
        """
        if url.fileName() == "" and url.path() == "/":
            logging.debug(str(url))
            self.ui.contentWebView.setHtml(self._html, url)
        else:
            self.signal_link_clicked.emit(url.toLocalFile().split("/")[-1])

