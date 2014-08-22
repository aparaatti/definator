# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QTermDisplay.ui'
#
# Created: Fri Aug 15 21:56:59 2014
#      by: PyQt5 UI code generator 5.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TermDisplay(object):
    def setupUi(self, TermDisplay):
        TermDisplay.setObjectName("TermDisplay")
        TermDisplay.resize(548, 435)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(TermDisplay.sizePolicy().hasHeightForWidth())
        TermDisplay.setSizePolicy(sizePolicy)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(TermDisplay)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.scrollArea = QtWidgets.QScrollArea(TermDisplay)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 528, 415))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(400, 150))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.termDisplay = QtWebKitWidgets.QWebView(self.scrollAreaWidgetContents)
        self.termDisplay.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.termDisplay.sizePolicy().hasHeightForWidth())
        self.termDisplay.setSizePolicy(sizePolicy)
        self.termDisplay.setMinimumSize(QtCore.QSize(400, 400))
        self.termDisplay.setAcceptDrops(False)
        self.termDisplay.setUrl(QtCore.QUrl("file:///home/aparaatti/Code/Python/definator/TermBase/template-term.html"))
        self.termDisplay.setObjectName("termDisplay")
        self.verticalLayout.addWidget(self.termDisplay)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_4.addWidget(self.scrollArea)

        self.retranslateUi(TermDisplay)
        QtCore.QMetaObject.connectSlotsByName(TermDisplay)

    def retranslateUi(self, TermDisplay):
        _translate = QtCore.QCoreApplication.translate
        TermDisplay.setWindowTitle(_translate("TermDisplay", "Form"))

from PyQt5 import QtWebKitWidgets
