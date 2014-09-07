# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QStrChooser.ui'
#
# Created: Sun Sep  7 17:03:44 2014
#      by: PyQt5 UI code generator 5.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_QStrChooser(object):
    def setupUi(self, QStrChooser):
        QStrChooser.setObjectName("QStrChooser")
        QStrChooser.resize(166, 210)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(QStrChooser.sizePolicy().hasHeightForWidth())
        QStrChooser.setSizePolicy(sizePolicy)
        QStrChooser.setMinimumSize(QtCore.QSize(166, 200))
        QStrChooser.setMaximumSize(QtCore.QSize(166, 16777215))
        self.verticalLayout = QtWidgets.QVBoxLayout(QStrChooser)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(QStrChooser)
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout_2.addWidget(self.lineEdit)
        self.listWidget = QtWidgets.QListWidget(self.widget)
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.listWidget.setSelectionRectVisible(True)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_2.addWidget(self.listWidget)
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(QStrChooser)
        QtCore.QMetaObject.connectSlotsByName(QStrChooser)

    def retranslateUi(self, QStrChooser):
        _translate = QtCore.QCoreApplication.translate
        QStrChooser.setWindowTitle(_translate("QStrChooser", "Term list"))
        self.lineEdit.setPlaceholderText(_translate("QStrChooser", "Filter"))

