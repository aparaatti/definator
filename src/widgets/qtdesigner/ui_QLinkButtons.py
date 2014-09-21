# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QLinkButtons.ui'
#
# Created: Sun Sep 21 06:31:35 2014
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(122, 146)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.buttonLinkTerms = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonLinkTerms.sizePolicy().hasHeightForWidth())
        self.buttonLinkTerms.setSizePolicy(sizePolicy)
        self.buttonLinkTerms.setObjectName("buttonLinkTerms")
        self.verticalLayout.addWidget(self.buttonLinkTerms)
        self.buttonUnlinkTerms = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonUnlinkTerms.sizePolicy().hasHeightForWidth())
        self.buttonUnlinkTerms.setSizePolicy(sizePolicy)
        self.buttonUnlinkTerms.setObjectName("buttonUnlinkTerms")
        self.verticalLayout.addWidget(self.buttonUnlinkTerms)
        self.buttonAddFile = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonAddFile.sizePolicy().hasHeightForWidth())
        self.buttonAddFile.setSizePolicy(sizePolicy)
        self.buttonAddFile.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.buttonAddFile.setObjectName("buttonAddFile")
        self.verticalLayout.addWidget(self.buttonAddFile)
        self.buttonRemoveFiles = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonRemoveFiles.sizePolicy().hasHeightForWidth())
        self.buttonRemoveFiles.setSizePolicy(sizePolicy)
        self.buttonRemoveFiles.setObjectName("buttonRemoveFiles")
        self.verticalLayout.addWidget(self.buttonRemoveFiles)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.buttonLinkTerms.setText(_translate("Form", "Li&nk terms"))
        self.buttonUnlinkTerms.setText(_translate("Form", "Unlink te&rms"))
        self.buttonAddFile.setText(_translate("Form", "Link file&s"))
        self.buttonRemoveFiles.setText(_translate("Form", "Unlin&k files"))

