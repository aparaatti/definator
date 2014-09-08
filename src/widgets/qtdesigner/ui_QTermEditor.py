# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QTermEditor.ui'
#
# Created: Mon Sep  8 03:39:46 2014
#      by: PyQt5 UI code generator 5.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TermEditor(object):
    def setupUi(self, TermEditor):
        TermEditor.setObjectName("TermEditor")
        TermEditor.resize(658, 422)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(TermEditor.sizePolicy().hasHeightForWidth())
        TermEditor.setSizePolicy(sizePolicy)
        TermEditor.setAutoFillBackground(False)
        self.verticalLayout = QtWidgets.QVBoxLayout(TermEditor)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(TermEditor)
        self.groupBox.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lineEditTitle = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditTitle.sizePolicy().hasHeightForWidth())
        self.lineEditTitle.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.lineEditTitle.setFont(font)
        self.lineEditTitle.setText("")
        self.lineEditTitle.setObjectName("lineEditTitle")
        self.verticalLayout_2.addWidget(self.lineEditTitle)
        self.textEditContent = QtWidgets.QTextEdit(self.groupBox)
        self.textEditContent.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEditContent.sizePolicy().hasHeightForWidth())
        self.textEditContent.setSizePolicy(sizePolicy)
        self.textEditContent.setObjectName("textEditContent")
        self.verticalLayout_2.addWidget(self.textEditContent)
        self.verticalLayout.addWidget(self.groupBox)

        self.retranslateUi(TermEditor)
        QtCore.QMetaObject.connectSlotsByName(TermEditor)

    def retranslateUi(self, TermEditor):
        _translate = QtCore.QCoreApplication.translate
        TermEditor.setWindowTitle(_translate("TermEditor", "Form"))
        self.groupBox.setTitle(_translate("TermEditor", "Editor"))
        self.lineEditTitle.setPlaceholderText(_translate("TermEditor", "Term name"))
        self.textEditContent.setPlaceholderText(_translate("TermEditor", "Description of the term."))

