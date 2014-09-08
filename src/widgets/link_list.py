# -*- coding: utf-8 -*-
#
# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QUrl
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWebKitWidgets import QWebPage

from .qtdesigner.ui_QLinkList import Ui_QLinkList


class LinkList(QWidget):
    link_selected = pyqtSignal(str)

    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.ui = Ui_QLinkList()
        self.ui.setupUi(self)
        #linkClicked(const QUrl & url)
        self.ui.linksWebView.linkClicked.connect(self._map_to_signal)
        self.ui.linksWebView.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
        self.ui.linkBox.setTitle(title)

    @pyqtSlot(str)
    def set_current_html(self, html: str):
        self.ui.linksWebView.setHtml(html, QUrl("file://"))

    @pyqtSlot(QUrl)
    def _map_to_signal(self, url):
        self.link_selected.emit(url.toString()[8:])
