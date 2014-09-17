# -*- coding: utf-8 -*-
#
# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QUrl
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWebKitWidgets import QWebPage
from PyQt5.QtGui import QKeySequence

from .qtdesigner.ui_QLinkList import Ui_QLinkList
from .key_press_eater import KeyPressEater


class LinkList(QWidget):
    """
    This widget show html given to it. All links beginning with url "file://" are
    sent as link_selected(str) signal in which the str is the url string in the link.

    Module sends signal_undo_event or signal_redo_event when standard undo or redo key combination is
    pressed while the html view is focused.
    """
    link_selected = pyqtSignal(str)

    signal_undo_event = pyqtSignal()
    signal_redo_event = pyqtSignal()

    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.ui = Ui_QLinkList()
        self.ui.setupUi(self)

        #linkClicked(const QUrl & url)
        self.ui.linksWebView.linkClicked.connect(self._map_to_signal)
        self.ui.linksWebView.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
        self.ui.linkBox.setTitle(title)

        #Hook into undo/redo of term_editor
        self.eventFilter = KeyPressEater(QKeySequence.Undo, self)
        self.eventFilter2 = KeyPressEater(QKeySequence.Redo, self)
        self.ui.linksWebView.installEventFilter(self.eventFilter)
        self.ui.linksWebView.installEventFilter(self.eventFilter2)

    @pyqtSlot(str)
    def set_current_html(self, html: str):
        """
        This slot sets the html the module shows.
        :param html: string containing html document.
        """
        self.ui.linksWebView.setHtml(html, QUrl("file://"))

    @pyqtSlot(QUrl)
    def _map_to_signal(self, url):
        self.link_selected.emit(url.toString()[8:])

    def _trigger_event(self, sequence: QKeySequence):
        if sequence is QKeySequence.Undo:
            self.signal_undo_event.emit()

        if sequence is QKeySequence.Redo:
            self.signal_redo_event.emit()