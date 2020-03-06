# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'nodeProperty.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_uiNodeEditor(object):
    def setupUi(self, uiNodeEditor):
        uiNodeEditor.setObjectName("uiNodeEditor")
        uiNodeEditor.resize(288, 246)
        self.gridLayout = QtWidgets.QGridLayout(uiNodeEditor)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_2 = QtWidgets.QGroupBox(uiNodeEditor)
        self.groupBox_2.setObjectName("groupBox_2")
        self.formLayout_2 = QtWidgets.QFormLayout(self.groupBox_2)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setEnabled(True)
        self.label.setMinimumSize(QtCore.QSize(75, 0))
        self.label.setObjectName("label")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.uiName = QtWidgets.QLineEdit(self.groupBox_2)
        self.uiName.setObjectName("uiName")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.uiName)
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setMinimumSize(QtCore.QSize(75, 0))
        self.label_2.setObjectName("label_2")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.uiTypeInfo = QtWidgets.QLineEdit(self.groupBox_2)
        self.uiTypeInfo.setReadOnly(True)
        self.uiTypeInfo.setObjectName("uiTypeInfo")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.uiTypeInfo)
        self.gridLayout.addWidget(self.groupBox_2, 0, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(uiNodeEditor)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.uiViewport = QtWidgets.QCheckBox(self.groupBox)
        self.uiViewport.setObjectName("uiViewport")
        self.horizontalLayout.addWidget(self.uiViewport)
        self.uiSelectable = QtWidgets.QCheckBox(self.groupBox)
        self.uiSelectable.setObjectName("uiSelectable")
        self.horizontalLayout.addWidget(self.uiSelectable)
        self.gridLayout.addWidget(self.groupBox, 1, 0, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(uiNodeEditor)
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.uiViewportName = QtWidgets.QCheckBox(self.groupBox_3)
        self.uiViewportName.setObjectName("uiViewportName")
        self.horizontalLayout_2.addWidget(self.uiViewportName)
        self.uiViewportCoordinate = QtWidgets.QCheckBox(self.groupBox_3)
        self.uiViewportCoordinate.setObjectName("uiViewportCoordinate")
        self.horizontalLayout_2.addWidget(self.uiViewportCoordinate)
        self.gridLayout.addWidget(self.groupBox_3, 2, 0, 1, 1)

        self.retranslateUi(uiNodeEditor)
        QtCore.QMetaObject.connectSlotsByName(uiNodeEditor)

    def retranslateUi(self, uiNodeEditor):
        _translate = QtCore.QCoreApplication.translate
        uiNodeEditor.setWindowTitle(_translate("uiNodeEditor", "Form"))
        self.groupBox_2.setTitle(_translate("uiNodeEditor", "ID"))
        self.label.setText(_translate("uiNodeEditor", "Name"))
        self.label_2.setText(_translate("uiNodeEditor", "Type Info"))
        self.groupBox.setTitle(_translate("uiNodeEditor", "Visibility"))
        self.uiViewport.setText(_translate("uiNodeEditor", "Shows in viewport"))
        self.uiSelectable.setText(_translate("uiNodeEditor", "Display auxiliry line"))
        self.groupBox_3.setTitle(_translate("uiNodeEditor", "Viewport Display"))
        self.uiViewportName.setText(_translate("uiNodeEditor", "Name"))
        self.uiViewportCoordinate.setText(_translate("uiNodeEditor", "Coordinate"))
