# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QTermEditor.ui'
#
# Created: Fri Sep 12 17:21:07 2014
#      by: PyQt5 UI code generator 5.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TermEditor(object):
    def setupUi(self, TermEditor):
        TermEditor.setObjectName("TermEditor")
        TermEditor.setAutoFillBackground(False)
        self.verticalLayout = QtWidgets.QVBoxLayout(TermEditor)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(TermEditor)
        self.groupBox.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lineEditTitle = QtWidgets.QLineEdit(self.groupBox)
        font = QtGui.QFont()
        font.setFamily("Oxygen Mono")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
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
        font = QtGui.QFont()
        font.setFamily("Oxygen Mono")
        self.textEditContent.setFont(font)
        self.textEditContent.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.textEditContent.setObjectName("textEditContent")
        self.verticalLayout_2.addWidget(self.textEditContent)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.addTitleToolButton = QtWidgets.QToolButton(self.groupBox)
        self.addTitleToolButton.setArrowType(QtCore.Qt.NoArrow)
        self.addTitleToolButton.setObjectName("addTitleToolButton")
        self.gridLayout_2.addWidget(self.addTitleToolButton, 0, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 4, 1, 1)
        self.addImageToolButton = QtWidgets.QToolButton(self.groupBox)
        self.addImageToolButton.setObjectName("addImageToolButton")
        self.gridLayout_2.addWidget(self.addImageToolButton, 0, 3, 1, 1)
        self.addTagLabel = QtWidgets.QLabel(self.groupBox)
        self.addTagLabel.setObjectName("addTagLabel")
        self.gridLayout_2.addWidget(self.addTagLabel, 0, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_2)
        self.verticalLayout.addWidget(self.groupBox)

        self.retranslateUi(TermEditor)
        QtCore.QMetaObject.connectSlotsByName(TermEditor)

    def retranslateUi(self, TermEditor):
        _translate = QtCore.QCoreApplication.translate
        TermEditor.setWindowTitle(_translate("TermEditor", "Form"))
        self.groupBox.setTitle(_translate("TermEditor", "Editor"))
        self.lineEditTitle.setPlaceholderText(_translate("TermEditor", "Term name"))
        self.textEditContent.setPlaceholderText(_translate("TermEditor", "Description of the term."))
        self.addTitleToolButton.setText(_translate("TermEditor", "title"))
        self.addImageToolButton.setText(_translate("TermEditor", "image"))
        self.addTagLabel.setText(_translate("TermEditor", "Add a tag:"))

