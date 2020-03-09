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
        Form.resize(255, 214)
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.uiAddCurve = QtWidgets.QPushButton(self.groupBox)
        self.uiAddCurve.setObjectName("uiAddCurve")
        self.gridLayout.addWidget(self.uiAddCurve, 1, 0, 1, 1)
        self.listWidget = QtWidgets.QListWidget(self.groupBox)
        self.listWidget.setObjectName("listWidget")
        self.gridLayout.addWidget(self.listWidget, 0, 0, 1, 2)
        self.uiDeleteCurve = QtWidgets.QPushButton(self.groupBox)
        self.uiDeleteCurve.setObjectName("uiDeleteCurve")
        self.gridLayout.addWidget(self.uiDeleteCurve, 1, 1, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 2)
        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.gridLayout_2.addWidget(self.comboBox, 1, 1, 1, 1)
        self.uiOk = QtWidgets.QPushButton(Form)
        self.uiOk.setObjectName("uiOk")
        self.gridLayout_2.addWidget(self.uiOk, 2, 1, 1, 1)
        self.label = QtWidgets.QLabel(Form)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 1)
        self.uiPreview = QtWidgets.QPushButton(Form)
        self.uiPreview.setObjectName("uiPreview")
        self.gridLayout_2.addWidget(self.uiPreview, 2, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 3, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "Curves"))
        self.uiAddCurve.setText(_translate("Form", "Add Selection"))
        self.uiDeleteCurve.setText(_translate("Form", "Delete"))
        self.comboBox.setItemText(0, _translate("Form", "StretchStyle"))
        self.comboBox.setItemText(1, _translate("Form", "CoonsStyle"))
        self.comboBox.setItemText(2, _translate("Form", "CurvedStyle"))
        self.uiOk.setText(_translate("Form", "Ok"))
        self.label.setText(_translate("Form", "Surface style"))
        self.uiPreview.setText(_translate("Form", "Preview"))
