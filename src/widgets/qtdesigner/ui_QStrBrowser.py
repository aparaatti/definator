# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QStrBrowser.ui'
#
# Created: Thu Sep 18 09:31:32 2014
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_QStrBrowser(object):
    def setupUi(self, QStrBrowser):
        QStrBrowser.setObjectName("QStrBrowser")
        QStrBrowser.resize(166, 357)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(QStrBrowser.sizePolicy().hasHeightForWidth())
        QStrBrowser.setSizePolicy(sizePolicy)
        QStrBrowser.setMinimumSize(QtCore.QSize(166, 200))
        QStrBrowser.setMaximumSize(QtCore.QSize(166, 16777215))
        self.verticalLayout = QtWidgets.QVBoxLayout(QStrBrowser)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.str_box = QtWidgets.QGroupBox(QStrBrowser)
        self.str_box.setObjectName("str_box")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.str_box)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lineEdit = QtWidgets.QLineEdit(self.str_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout_3.addWidget(self.lineEdit)
        self.listWidget = QtWidgets.QListWidget(self.str_box)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_3.addWidget(self.listWidget)
        self.verticalLayout.addWidget(self.str_box)

        self.retranslateUi(QStrBrowser)
        QtCore.QMetaObject.connectSlotsByName(QStrBrowser)

    def retranslateUi(self, QStrBrowser):
        _translate = QtCore.QCoreApplication.translate
        QStrBrowser.setWindowTitle(_translate("QStrBrowser", "Term list"))
        self.str_box.setTitle(_translate("QStrBrowser", "String browser"))
        self.lineEdit.setToolTip(_translate("QStrBrowser", "<html><head/><body><p>Filter out terms by writing here</p></body></html>"))
        self.lineEdit.setPlaceholderText(_translate("QStrBrowser", "Filter"))

