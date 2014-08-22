# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QStrBrowser.ui'
#
# Created: Wed Aug 20 12:04:22 2014
#      by: PyQt5 UI code generator 5.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_QStrBrowser(object):
    def setupUi(self, QStrBrowser):
        QStrBrowser.setObjectName("QStrBrowser")
        QStrBrowser.resize(166, 210)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(QStrBrowser.sizePolicy().hasHeightForWidth())
        QStrBrowser.setSizePolicy(sizePolicy)
        QStrBrowser.setMinimumSize(QtCore.QSize(166, 200))
        QStrBrowser.setMaximumSize(QtCore.QSize(166, 16777215))
        self.verticalLayout = QtWidgets.QVBoxLayout(QStrBrowser)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lineEdit = QtWidgets.QLineEdit(QStrBrowser)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.widget = QtWidgets.QWidget(QStrBrowser)
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.listWidget = QtWidgets.QListWidget(self.widget)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_2.addWidget(self.listWidget)
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(QStrBrowser)
        QtCore.QMetaObject.connectSlotsByName(QStrBrowser)

    def retranslateUi(self, QStrBrowser):
        _translate = QtCore.QCoreApplication.translate
        QStrBrowser.setWindowTitle(_translate("QStrBrowser", "Term list"))
        self.lineEdit.setToolTip(_translate("QStrBrowser", "<html><head/><body><p>Filter out terms by writing here</p></body></html>"))
        self.lineEdit.setText(_translate("QStrBrowser", "Filter"))

