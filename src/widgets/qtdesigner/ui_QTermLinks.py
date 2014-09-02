# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QTermLinks.ui'
#
# Created: Tue Sep  2 14:55:00 2014
#      by: PyQt5 UI code generator 5.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_QTermLinks(object):
    def setupUi(self, QTermLinks):
        QTermLinks.setObjectName("QTermLinks")
        QTermLinks.resize(550, 150)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(QTermLinks.sizePolicy().hasHeightForWidth())
        QTermLinks.setSizePolicy(sizePolicy)
        QTermLinks.setMinimumSize(QtCore.QSize(550, 150))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(QTermLinks)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBoxTermLinker = QtWidgets.QGroupBox(QTermLinks)
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
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setAutoFillBackground(False)
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

        self.retranslateUi(QTermLinks)
        QtCore.QMetaObject.connectSlotsByName(QTermLinks)

    def retranslateUi(self, QTermLinks):
        _translate = QtCore.QCoreApplication.translate
        QTermLinks.setWindowTitle(_translate("QTermLinks", "Term linker"))
        self.groupBoxTermLinker.setTitle(_translate("QTermLinks", "Related terms"))
        self.tableWidget.setSortingEnabled(True)
        self.buttonLinkTerm.setText(_translate("QTermLinks", "&Link term"))
        self.buttonUnlinkTerm.setText(_translate("QTermLinks", "&Unlink term"))

