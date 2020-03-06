# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'clippingPlaneProperty.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(200, 215)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.xRadioButton = QtWidgets.QRadioButton(Form)
        self.xRadioButton.setChecked(True)
        self.xRadioButton.setObjectName("xRadioButton")
        self.buttonGroup = QtWidgets.QButtonGroup(Form)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.xRadioButton)
        self.gridLayout.addWidget(self.xRadioButton, 1, 1, 1, 1)
        self.zRadioButton = QtWidgets.QRadioButton(Form)
        self.zRadioButton.setObjectName("zRadioButton")
        self.buttonGroup.addButton(self.zRadioButton)
        self.gridLayout.addWidget(self.zRadioButton, 3, 1, 1, 1)
        self.yRadioButton = QtWidgets.QRadioButton(Form)
        self.yRadioButton.setObjectName("yRadioButton")
        self.buttonGroup.addButton(self.yRadioButton)
        self.gridLayout.addWidget(self.yRadioButton, 2, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.checkBox = QtWidgets.QCheckBox(Form)
        self.checkBox.setChecked(False)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout.addWidget(self.checkBox, 0, 1, 1, 1)
        self.animatePushButton = QtWidgets.QPushButton(Form)
        self.animatePushButton.setObjectName("animatePushButton")
        self.gridLayout.addWidget(self.animatePushButton, 4, 0, 1, 1)
        self.resetPushButton = QtWidgets.QPushButton(Form)
        self.resetPushButton.setObjectName("resetPushButton")
        self.gridLayout.addWidget(self.resetPushButton, 4, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.xRadioButton.setText(_translate("Form", "X"))
        self.zRadioButton.setText(_translate("Form", "Z"))
        self.yRadioButton.setText(_translate("Form", "Y"))
        self.label_3.setText(_translate("Form", "Clipping Direction"))
        self.label.setText(_translate("Form", "Clipping Plane"))
        self.checkBox.setText(_translate("Form", "On/Off"))
        self.animatePushButton.setText(_translate("Form", "Animate"))
        self.resetPushButton.setText(_translate("Form", "Reset"))
