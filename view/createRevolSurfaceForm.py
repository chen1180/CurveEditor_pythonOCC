# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'createRevolSurfaceForm.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(255, 271)
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.uiOk = QtWidgets.QPushButton(Form)
        self.uiOk.setObjectName("uiOk")
        self.gridLayout_2.addWidget(self.uiOk, 1, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 2, 1, 1, 1)
        self.uiPreview = QtWidgets.QPushButton(Form)
        self.uiPreview.setObjectName("uiPreview")
        self.gridLayout_2.addWidget(self.uiPreview, 1, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.uiChangeProfile = QtWidgets.QPushButton(self.groupBox)
        self.uiChangeProfile.setObjectName("uiChangeProfile")
        self.gridLayout.addWidget(self.uiChangeProfile, 1, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 4, 1, 1, 1)
        self.uiProfile = QtWidgets.QLineEdit(self.groupBox)
        self.uiProfile.setReadOnly(True)
        self.uiProfile.setObjectName("uiProfile")
        self.gridLayout.addWidget(self.uiProfile, 1, 1, 1, 1)
        self.uiAxis = QtWidgets.QLineEdit(self.groupBox)
        self.uiAxis.setReadOnly(True)
        self.uiAxis.setObjectName("uiAxis")
        self.gridLayout.addWidget(self.uiAxis, 3, 1, 1, 1)
        self.uiChangeAxis = QtWidgets.QPushButton(self.groupBox)
        self.uiChangeAxis.setObjectName("uiChangeAxis")
        self.gridLayout.addWidget(self.uiChangeAxis, 3, 2, 1, 1)
        self.uiDegree = QtWidgets.QSpinBox(self.groupBox)
        self.uiDegree.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.uiDegree.setMinimum(90)
        self.uiDegree.setMaximum(360)
        self.uiDegree.setSingleStep(90)
        self.uiDegree.setProperty("value", 360)
        self.uiDegree.setObjectName("uiDegree")
        self.gridLayout.addWidget(self.uiDegree, 5, 1, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.uiOk.setText(_translate("Form", "Ok"))
        self.uiPreview.setText(_translate("Form", "Preview"))
        self.groupBox.setTitle(_translate("Form", "Geometry"))
        self.label_2.setText(_translate("Form", "Profile"))
        self.uiChangeProfile.setToolTip(_translate("Form", "Select a profile"))
        self.uiChangeProfile.setText(_translate("Form", "Select"))
        self.label_3.setText(_translate("Form", "Axis"))
        self.label.setText(_translate("Form", "Angle"))
        self.uiChangeAxis.setToolTip(_translate("Form", "Select a line"))
        self.uiChangeAxis.setText(_translate("Form", "Select"))
        self.uiDegree.setSuffix(_translate("Form", "°"))
