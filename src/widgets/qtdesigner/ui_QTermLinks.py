# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QTermLinks.ui'
#
# Created: Mon Sep  8 03:39:46 2014
#      by: PyQt5 UI code generator 5.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_QTermLinks(object):
    def setupUi(self, QTermLinks):
        QTermLinks.setObjectName("QTermLinks")
        QTermLinks.resize(550, 235)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(QTermLinks.sizePolicy().hasHeightForWidth())
        QTermLinks.setSizePolicy(sizePolicy)
        QTermLinks.setMinimumSize(QtCore.QSize(550, 150))
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(QTermLinks)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.groupBoxTermLinker = QtWidgets.QGroupBox(QTermLinks)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBoxTermLinker.sizePolicy().hasHeightForWidth())
        self.groupBoxTermLinker.setSizePolicy(sizePolicy)
        self.groupBoxTermLinker.setMaximumSize(QtCore.QSize(16777215, 300))
        self.groupBoxTermLinker.setObjectName("groupBoxTermLinker")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBoxTermLinker)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tableWidget = QtWidgets.QTableWidget(self.groupBoxTermLinker)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setAutoFillBackground(True)
        self.tableWidget.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tableWidget.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.setGridStyle(QtCore.Qt.DashLine)
        self.tableWidget.setCornerButtonEnabled(True)
        self.tableWidget.setRowCount(3)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setDefaultSectionSize(20)
        self.horizontalLayout.addWidget(self.tableWidget)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.buttonLinkTerms = QtWidgets.QPushButton(self.groupBoxTermLinker)
        self.buttonLinkTerms.setObjectName("buttonLinkTerms")
        self.verticalLayout.addWidget(self.buttonLinkTerms)
        self.buttonUnlinkTerms = QtWidgets.QPushButton(self.groupBoxTermLinker)
        self.buttonUnlinkTerms.setObjectName("buttonUnlinkTerms")
        self.verticalLayout.addWidget(self.buttonUnlinkTerms)
        self.buttonAddFile = QtWidgets.QPushButton(self.groupBoxTermLinker)
        self.buttonAddFile.setObjectName("buttonAddFile")
        self.verticalLayout.addWidget(self.buttonAddFile)
        self.buttonRemoveFiles = QtWidgets.QPushButton(self.groupBoxTermLinker)
        self.buttonRemoveFiles.setObjectName("buttonRemoveFiles")
        self.verticalLayout.addWidget(self.buttonRemoveFiles)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.labelKeys = QtWidgets.QLabel(self.groupBoxTermLinker)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelKeys.setFont(font)
        self.labelKeys.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.labelKeys.setObjectName("labelKeys")
        self.horizontalLayout_2.addWidget(self.labelKeys)
        self.keyTableWidget = QtWidgets.QTableWidget(self.groupBoxTermLinker)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.keyTableWidget.sizePolicy().hasHeightForWidth())
        self.keyTableWidget.setSizePolicy(sizePolicy)
        self.keyTableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.keyTableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.keyTableWidget.setShowGrid(False)
        self.keyTableWidget.setWordWrap(False)
        self.keyTableWidget.setCornerButtonEnabled(False)
        self.keyTableWidget.setObjectName("keyTableWidget")
        self.keyTableWidget.setColumnCount(0)
        self.keyTableWidget.setRowCount(0)
        self.keyTableWidget.horizontalHeader().setVisible(False)
        self.keyTableWidget.verticalHeader().setVisible(False)
        self.horizontalLayout_2.addWidget(self.keyTableWidget)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4.addWidget(self.groupBoxTermLinker)

        self.retranslateUi(QTermLinks)
        QtCore.QMetaObject.connectSlotsByName(QTermLinks)

    def retranslateUi(self, QTermLinks):
        _translate = QtCore.QCoreApplication.translate
        QTermLinks.setWindowTitle(_translate("QTermLinks", "Term linker"))
        self.groupBoxTermLinker.setTitle(_translate("QTermLinks", "Related things"))
        self.tableWidget.setSortingEnabled(False)
        self.buttonLinkTerms.setText(_translate("QTermLinks", "&Link terms"))
        self.buttonUnlinkTerms.setText(_translate("QTermLinks", "&Unlink terms"))
        self.buttonAddFile.setText(_translate("QTermLinks", "&Add a file"))
        self.buttonRemoveFiles.setText(_translate("QTermLinks", "&Remove files"))
        self.labelKeys.setText(_translate("QTermLinks", "Key: "))

