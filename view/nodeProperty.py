# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'nodeProperty.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_uiNodeEditor(object):
    def setupUi(self, uiNodeEditor):
        uiNodeEditor.setObjectName("uiNodeEditor")
        uiNodeEditor.resize(272, 70)
        self.verticalLayout = QtWidgets.QVBoxLayout(uiNodeEditor)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(uiNodeEditor)
        self.label.setEnabled(True)
        self.label.setMinimumSize(QtCore.QSize(75, 0))
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.uiName = QtWidgets.QLineEdit(uiNodeEditor)
        self.uiName.setObjectName("uiName")
        self.horizontalLayout.addWidget(self.uiName)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(uiNodeEditor)
        self.label_2.setMinimumSize(QtCore.QSize(75, 0))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.uiTypeInfo = QtWidgets.QLineEdit(uiNodeEditor)
        self.uiTypeInfo.setReadOnly(True)
        self.uiTypeInfo.setObjectName("uiTypeInfo")
        self.horizontalLayout_2.addWidget(self.uiTypeInfo)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(uiNodeEditor)
        QtCore.QMetaObject.connectSlotsByName(uiNodeEditor)

    def retranslateUi(self, uiNodeEditor):
        _translate = QtCore.QCoreApplication.translate
        uiNodeEditor.setWindowTitle(_translate("uiNodeEditor", "Form"))
        self.label.setText(_translate("uiNodeEditor", "Name"))
        self.label_2.setText(_translate("uiNodeEditor", "Type Info"))
