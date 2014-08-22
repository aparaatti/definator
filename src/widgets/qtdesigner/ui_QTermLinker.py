# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QTermLinker.ui'
#
# Created: Wed Aug 20 12:04:23 2014
#      by: PyQt5 UI code generator 5.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TermLinker(object):
    def setupUi(self, TermLinker):
        TermLinker.setObjectName("TermLinker")
        TermLinker.resize(550, 185)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(TermLinker.sizePolicy().hasHeightForWidth())
        TermLinker.setSizePolicy(sizePolicy)
        TermLinker.setMinimumSize(QtCore.QSize(550, 150))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(TermLinker)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBoxTermLinker = QtWidgets.QGroupBox(TermLinker)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBoxTermLinker.sizePolicy().hasHeightForWidth())
        self.groupBoxTermLinker.setSizePolicy(sizePolicy)
        self.groupBoxTermLinker.setMaximumSize(QtCore.QSize(16777215, 300))
        self.groupBoxTermLinker.setObjectName("groupBoxTermLinker")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBoxTermLinker)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tableWidget = QtWidgets.QTableWidget(self.groupBoxTermLinker)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.horizontalLayout.addWidget(self.tableWidget)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.buttonLinkTerm = QtWidgets.QPushButton(self.groupBoxTermLinker)
        self.buttonLinkTerm.setObjectName("buttonLinkTerm")
        self.verticalLayout.addWidget(self.buttonLinkTerm)
        self.buttonUnlinkTerm = QtWidgets.QPushButton(self.groupBoxTermLinker)
        self.buttonUnlinkTerm.setObjectName("buttonUnlinkTerm")
        self.verticalLayout.addWidget(self.buttonUnlinkTerm)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_2.addWidget(self.groupBoxTermLinker)

        self.retranslateUi(TermLinker)
        QtCore.QMetaObject.connectSlotsByName(TermLinker)

    def retranslateUi(self, TermLinker):
        _translate = QtCore.QCoreApplication.translate
        TermLinker.setWindowTitle(_translate("TermLinker", "Term linker"))
        self.groupBoxTermLinker.setTitle(_translate("TermLinker", "Related terms"))
        self.buttonLinkTerm.setText(_translate("TermLinker", "&Link term"))
        self.buttonUnlinkTerm.setText(_translate("TermLinker", "&Unlink term"))

