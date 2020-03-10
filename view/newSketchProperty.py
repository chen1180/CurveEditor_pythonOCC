# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'newSketchProperty.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_newSketchEditor(object):
    def setupUi(self, newSketchEditor):
        newSketchEditor.setObjectName("newSketchEditor")
        newSketchEditor.resize(211, 177)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(newSketchEditor)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(newSketchEditor)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.uiXYPlane = QtWidgets.QRadioButton(self.groupBox)
        self.uiXYPlane.setObjectName("uiXYPlane")
        self.verticalLayout.addWidget(self.uiXYPlane)
        self.uiYZPlane = QtWidgets.QRadioButton(self.groupBox)
        self.uiYZPlane.setObjectName("uiYZPlane")
        self.verticalLayout.addWidget(self.uiYZPlane)
        self.uiXZPlane = QtWidgets.QRadioButton(self.groupBox)
        self.uiXZPlane.setObjectName("uiXZPlane")
        self.verticalLayout.addWidget(self.uiXZPlane)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(newSketchEditor)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.uiOffset = QtWidgets.QSpinBox(newSketchEditor)
        self.uiOffset.setMinimum(-1000)
        self.uiOffset.setMaximum(1000)
        self.uiOffset.setSingleStep(100)
        self.uiOffset.setObjectName("uiOffset")
        self.horizontalLayout.addWidget(self.uiOffset)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.uiOk = QtWidgets.QDialogButtonBox(newSketchEditor)
        self.uiOk.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.uiOk.setObjectName("uiOk")
        self.verticalLayout_2.addWidget(self.uiOk)

        self.retranslateUi(newSketchEditor)
        QtCore.QMetaObject.connectSlotsByName(newSketchEditor)

    def retranslateUi(self, newSketchEditor):
        _translate = QtCore.QCoreApplication.translate
        newSketchEditor.setWindowTitle(_translate("newSketchEditor", "Choose orientation"))
        self.groupBox.setTitle(_translate("newSketchEditor", "Sketch Orientation"))
        self.uiXYPlane.setText(_translate("newSketchEditor", "XY-Plane"))
        self.uiYZPlane.setText(_translate("newSketchEditor", "YZ-Plane"))
        self.uiXZPlane.setText(_translate("newSketchEditor", "XZ-Plane"))
        self.label.setText(_translate("newSketchEditor", "Offset:"))
