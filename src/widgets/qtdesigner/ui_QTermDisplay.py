# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QTermDisplay.ui'
#
# Created: Sun Sep  7 17:03:44 2014
#      by: PyQt5 UI code generator 5.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TermDisplay(object):
    def setupUi(self, TermDisplay):
        TermDisplay.setObjectName("TermDisplay")
        TermDisplay.resize(658, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
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
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.contentWebView.setFont(font)
        self.contentWebView.setUrl(QtCore.QUrl("about:blank"))
        self.contentWebView.setObjectName("contentWebView")
        self.verticalLayout.addWidget(self.contentWebView)
        self.groupBox = QtWidgets.QGroupBox(TermDisplay)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 100))
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.termsWebView = QtWebKitWidgets.QWebView(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.termsWebView.sizePolicy().hasHeightForWidth())
        self.termsWebView.setSizePolicy(sizePolicy)
        self.termsWebView.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.termsWebView.setSizeIncrement(QtCore.QSize(0, 0))
        self.termsWebView.setAcceptDrops(False)
        self.termsWebView.setUrl(QtCore.QUrl("about:blank"))
        self.termsWebView.setObjectName("termsWebView")
        self.verticalLayout_2.addWidget(self.termsWebView)
        self.verticalLayout.addWidget(self.groupBox)

        self.retranslateUi(TermDisplay)
        QtCore.QMetaObject.connectSlotsByName(TermDisplay)

    def retranslateUi(self, TermDisplay):
        _translate = QtCore.QCoreApplication.translate
        TermDisplay.setWindowTitle(_translate("TermDisplay", "Form"))
        self.groupBox.setTitle(_translate("TermDisplay", "Related terms"))

from PyQt5 import QtWebKitWidgets
