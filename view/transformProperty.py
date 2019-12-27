# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'transformProperty.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_uiTransfromEditor(object):
    def setupUi(self, uiTransfromEditor):
        uiTransfromEditor.setObjectName("uiTransfromEditor")
        uiTransfromEditor.resize(278, 40)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(uiTransfromEditor)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(uiTransfromEditor)
        self.label.setEnabled(True)
        self.label.setMinimumSize(QtCore.QSize(0, 0))
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.uiX = QtWidgets.QDoubleSpinBox(uiTransfromEditor)
        self.uiX.setObjectName("uiX")
        self.horizontalLayout.addWidget(self.uiX)
        self.uiY = QtWidgets.QDoubleSpinBox(uiTransfromEditor)
        self.uiY.setObjectName("uiY")
        self.horizontalLayout.addWidget(self.uiY)
        self.uiZ = QtWidgets.QDoubleSpinBox(uiTransfromEditor)
        self.uiZ.setObjectName("uiZ")
        self.horizontalLayout.addWidget(self.uiZ)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(uiTransfromEditor)
        QtCore.QMetaObject.connectSlotsByName(uiTransfromEditor)

    def retranslateUi(self, uiTransfromEditor):
        _translate = QtCore.QCoreApplication.translate
        uiTransfromEditor.setWindowTitle(_translate("uiTransfromEditor", "Form"))
        self.label.setText(_translate("uiTransfromEditor", "Position"))
