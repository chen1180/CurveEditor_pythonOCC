# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'createBezierSurfaceForm.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(340, 467)
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.listWidget = QtWidgets.QListWidget(self.groupBox)
        self.listWidget.setObjectName("listWidget")
        self.gridLayout.addWidget(self.listWidget, 0, 0, 1, 2)
        self.uiAddCurve = QtWidgets.QPushButton(self.groupBox)
        self.uiAddCurve.setObjectName("uiAddCurve")
        self.gridLayout.addWidget(self.uiAddCurve, 1, 0, 1, 1)
        self.uiDeleteCurve = QtWidgets.QPushButton(self.groupBox)
        self.uiDeleteCurve.setObjectName("uiDeleteCurve")
        self.gridLayout.addWidget(self.uiDeleteCurve, 1, 1, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 3)
        self.uiCancel = QtWidgets.QPushButton(Form)
        self.uiCancel.setObjectName("uiCancel")
        self.gridLayout_2.addWidget(self.uiCancel, 1, 0, 1, 1)
        self.uiOk = QtWidgets.QPushButton(Form)
        self.uiOk.setObjectName("uiOk")
        self.gridLayout_2.addWidget(self.uiOk, 1, 1, 1, 1)
        self.pushButton_5 = QtWidgets.QPushButton(Form)
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout_2.addWidget(self.pushButton_5, 1, 2, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "Curves"))
        self.uiAddCurve.setText(_translate("Form", "Add"))
        self.uiDeleteCurve.setText(_translate("Form", "Delete"))
        self.uiCancel.setText(_translate("Form", "Preview"))
        self.uiOk.setText(_translate("Form", "Ok"))
        self.pushButton_5.setText(_translate("Form", "Cancel"))
