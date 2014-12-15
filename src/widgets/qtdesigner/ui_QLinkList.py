# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QLinkList.ui'
#
# Created: Wed Oct  1 14:29:06 2014
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_QLinkList(object):
    def setupUi(self, QLinkList):
        QLinkList.setObjectName("QLinkList")
        QLinkList.resize(400, 118)
        self.verticalLayout = QtWidgets.QVBoxLayout(QLinkList)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.linkBox = QtWidgets.QGroupBox(QLinkList)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.linkBox.sizePolicy().hasHeightForWidth())
        self.linkBox.setSizePolicy(sizePolicy)
        self.linkBox.setMaximumSize(QtCore.QSize(16777215, 100))
        self.linkBox.setObjectName("linkBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.linkBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.linksWebView = QtWebKitWidgets.QWebView(self.linkBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.linksWebView.sizePolicy().hasHeightForWidth())
        self.linksWebView.setSizePolicy(sizePolicy)
        self.linksWebView.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.linksWebView.setSizeIncrement(QtCore.QSize(0, 0))
        self.linksWebView.setAcceptDrops(False)
        self.linksWebView.setUrl(QtCore.QUrl("about:blank"))
        self.linksWebView.setObjectName("linksWebView")
        self.verticalLayout_2.addWidget(self.linksWebView)
        self.verticalLayout.addWidget(self.linkBox)

        self.retranslateUi(QLinkList)
        QtCore.QMetaObject.connectSlotsByName(QLinkList)

    def retranslateUi(self, QLinkList):
        _translate = QtCore.QCoreApplication.translate
        QLinkList.setWindowTitle(_translate("QLinkList", "Form"))
        self.linkBox.setTitle(_translate("QLinkList", "Link list"))

from PyQt5 import QtWebKitWidgets
