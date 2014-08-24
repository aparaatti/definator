# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QTermDisplay.ui'
#
# Created: Sun Aug 24 00:29:15 2014
#      by: PyQt5 UI code generator 5.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TermDisplay(object):
    def setupUi(self, TermDisplay):
        TermDisplay.setObjectName("TermDisplay")
        TermDisplay.resize(658, 429)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(TermDisplay.sizePolicy().hasHeightForWidth())
        TermDisplay.setSizePolicy(sizePolicy)
        TermDisplay.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.verticalLayout = QtWidgets.QVBoxLayout(TermDisplay)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.contentWebView = QtWebKitWidgets.QWebView(TermDisplay)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.contentWebView.sizePolicy().hasHeightForWidth())
        self.contentWebView.setSizePolicy(sizePolicy)
        self.contentWebView.setUrl(QtCore.QUrl("about:blank"))
        self.contentWebView.setObjectName("contentWebView")
        self.verticalLayout.addWidget(self.contentWebView)

        self.retranslateUi(TermDisplay)
        QtCore.QMetaObject.connectSlotsByName(TermDisplay)

    def retranslateUi(self, TermDisplay):
        _translate = QtCore.QCoreApplication.translate
        TermDisplay.setWindowTitle(_translate("TermDisplay", "Form"))

from PyQt5 import QtWebKitWidgets
