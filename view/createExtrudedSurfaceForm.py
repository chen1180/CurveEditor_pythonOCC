# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'createExtrudedSurfaceForm.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(204, 277)
        self.gridLayout_4 = QtWidgets.QGridLayout(Form)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.uiAlongEdge = QtWidgets.QRadioButton(self.groupBox_2)
        self.uiAlongEdge.setObjectName("uiAlongEdge")
        self.buttonGroup = QtWidgets.QButtonGroup(Form)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.uiAlongEdge)
        self.gridLayout_2.addWidget(self.uiAlongEdge, 2, 0, 1, 1)
        self.uiSelectEdgeButton = QtWidgets.QPushButton(self.groupBox_2)
        self.uiSelectEdgeButton.setObjectName("uiSelectEdgeButton")
        self.gridLayout_2.addWidget(self.uiSelectEdgeButton, 3, 1, 1, 1)
        self.uiEdgeLineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.uiEdgeLineEdit.setObjectName("uiEdgeLineEdit")
        self.gridLayout_2.addWidget(self.uiEdgeLineEdit, 3, 0, 1, 1)
        self.uiAlongNormal = QtWidgets.QRadioButton(self.groupBox_2)
        self.uiAlongNormal.setChecked(True)
        self.uiAlongNormal.setObjectName("uiAlongNormal")
        self.buttonGroup.addButton(self.uiAlongNormal)
        self.gridLayout_2.addWidget(self.uiAlongNormal, 1, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox_2, 1, 0, 1, 2)
        self.groupBox_3 = QtWidgets.QGroupBox(Form)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label = QtWidgets.QLabel(self.groupBox_3)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        self.uiLength = QtWidgets.QSpinBox(self.groupBox_3)
        self.uiLength.setMinimum(10)
        self.uiLength.setMaximum(1000)
        self.uiLength.setSingleStep(100)
        self.uiLength.setProperty("value", 100)
        self.uiLength.setObjectName("uiLength")
        self.gridLayout_3.addWidget(self.uiLength, 0, 1, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox_3, 2, 0, 1, 2)
        self.uiOk = QtWidgets.QPushButton(Form)
        self.uiOk.setObjectName("uiOk")
        self.gridLayout_4.addWidget(self.uiOk, 3, 1, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.uiSelectButton = QtWidgets.QPushButton(self.groupBox)
        self.uiSelectButton.setObjectName("uiSelectButton")
        self.gridLayout.addWidget(self.uiSelectButton, 0, 2, 1, 1)
        self.uiProfileLineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.uiProfileLineEdit.setReadOnly(True)
        self.uiProfileLineEdit.setObjectName("uiProfileLineEdit")
        self.gridLayout.addWidget(self.uiProfileLineEdit, 0, 1, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox, 0, 0, 1, 2)
        self.uiPreview = QtWidgets.QPushButton(Form)
        self.uiPreview.setObjectName("uiPreview")
        self.gridLayout_4.addWidget(self.uiPreview, 3, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem, 4, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox_2.setTitle(_translate("Form", "Direction"))
        self.uiAlongEdge.setText(_translate("Form", "Along edge"))
        self.uiSelectEdgeButton.setToolTip(_translate("Form", "Select a profile"))
        self.uiSelectEdgeButton.setText(_translate("Form", "Select"))
        self.uiAlongNormal.setText(_translate("Form", "Along normal"))
        self.groupBox_3.setTitle(_translate("Form", "Length"))
        self.label.setText(_translate("Form", "Along:"))
        self.uiOk.setText(_translate("Form", "Ok"))
        self.groupBox.setTitle(_translate("Form", "Geometry"))
        self.uiSelectButton.setToolTip(_translate("Form", "Select a profile"))
        self.uiSelectButton.setText(_translate("Form", "Select"))
        self.uiPreview.setText(_translate("Form", "Preview"))
