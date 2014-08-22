# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QTermList.ui'
#
# Created: Fri Aug 15 21:57:00 2014
#      by: PyQt5 UI code generator 5.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_QTermList(object):
    def setupUi(self, QTermList):
        QTermList.setObjectName("QTermList")
        QTermList.resize(166, 210)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(QTermList.sizePolicy().hasHeightForWidth())
        QTermList.setSizePolicy(sizePolicy)
        QTermList.setMinimumSize(QtCore.QSize(166, 200))
        QTermList.setMaximumSize(QtCore.QSize(166, 16777215))
        self.verticalLayout = QtWidgets.QVBoxLayout(QTermList)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lineEdit = QtWidgets.QLineEdit(QTermList)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.widget = QtWidgets.QWidget(QTermList)
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.listWidget = QtWidgets.QListWidget(self.widget)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_2.addWidget(self.listWidget)
        self.verticalLayout.addWidget(self.widget)
        self.buttonAddTerm = QtWidgets.QPushButton(QTermList)
        self.buttonAddTerm.setObjectName("buttonAddTerm")
        self.verticalLayout.addWidget(self.buttonAddTerm)

        self.retranslateUi(QTermList)
        QtCore.QMetaObject.connectSlotsByName(QTermList)

    def retranslateUi(self, QTermList):
        _translate = QtCore.QCoreApplication.translate
        QTermList.setWindowTitle(_translate("QTermList", "Term list"))
        self.lineEdit.setToolTip(_translate("QTermList", "<html><head/><body><p>Filter out terms by writing here</p></body></html>"))
        self.lineEdit.setText(_translate("QTermList", "Filter"))
        self.buttonAddTerm.setText(_translate("QTermList", "&Add term"))

