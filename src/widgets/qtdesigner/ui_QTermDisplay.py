# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QTermDisplay.ui'
#
# Created: Wed Oct  1 14:29:07 2014
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TermDisplay(object):
    def setupUi(self, TermDisplay):
        TermDisplay.setObjectName("TermDisplay")
        TermDisplay.resize(521, 449)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(TermDisplay.sizePolicy().hasHeightForWidth())
        TermDisplay.setSizePolicy(sizePolicy)
        TermDisplay.setLayoutDirection(QtCore.Qt.LeftToRight)
        TermDisplay.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.verticalLayout = QtWidgets.QVBoxLayout(TermDisplay)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(TermDisplay)
        self.groupBox.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.contentWebView = QtWebKitWidgets.QWebView(self.groupBox)
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
        self.verticalLayout_2.addWidget(self.contentWebView)
        self.verticalLayout.addWidget(self.groupBox)

        self.retranslateUi(TermDisplay)
        QtCore.QMetaObject.connectSlotsByName(TermDisplay)

    def retranslateUi(self, TermDisplay):
        _translate = QtCore.QCoreApplication.translate
        TermDisplay.setWindowTitle(_translate("TermDisplay", "Form"))
        self.groupBox.setTitle(_translate("TermDisplay", "Description"))

from PyQt5 import QtWebKitWidgets
