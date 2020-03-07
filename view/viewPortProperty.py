# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'viewPortProperty.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(273, 124)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.uiViewport = QtWidgets.QCheckBox(self.groupBox)
        self.uiViewport.setObjectName("uiViewport")
        self.horizontalLayout.addWidget(self.uiViewport)
        self.uiViewportAuxiliry = QtWidgets.QCheckBox(self.groupBox)
        self.uiViewportAuxiliry.setObjectName("uiViewportAuxiliry")
        self.horizontalLayout.addWidget(self.uiViewportAuxiliry)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(Form)
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.uiViewportName = QtWidgets.QCheckBox(self.groupBox_3)
        self.uiViewportName.setObjectName("uiViewportName")
        self.horizontalLayout_2.addWidget(self.uiViewportName)
        self.uiViewportCoordinate = QtWidgets.QCheckBox(self.groupBox_3)
        self.uiViewportCoordinate.setObjectName("uiViewportCoordinate")
        self.horizontalLayout_2.addWidget(self.uiViewportCoordinate)
        self.gridLayout.addWidget(self.groupBox_3, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "Visibility"))
        self.uiViewport.setText(_translate("Form", "Shows in viewport"))
        self.uiViewportAuxiliry.setText(_translate("Form", "Display auxiliry line"))
        self.groupBox_3.setTitle(_translate("Form", "Viewport Display"))
        self.uiViewportName.setText(_translate("Form", "Name"))
        self.uiViewportCoordinate.setText(_translate("Form", "Coordinate"))
