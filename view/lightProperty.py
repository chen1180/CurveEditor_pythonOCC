# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lightProperty.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_uiLightEditor(object):
    def setupUi(self, uiLightEditor):
        uiLightEditor.setObjectName("uiLightEditor")
        uiLightEditor.resize(311, 144)
        self.verticalLayout = QtWidgets.QVBoxLayout(uiLightEditor)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(uiLightEditor)
        self.label.setEnabled(True)
        self.label.setMinimumSize(QtCore.QSize(75, 0))
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.uiLightIntensity = QtWidgets.QDoubleSpinBox(uiLightEditor)
        self.uiLightIntensity.setObjectName("uiLightIntensity")
        self.horizontalLayout.addWidget(self.uiLightIntensity)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(uiLightEditor)
        self.label_2.setEnabled(True)
        self.label_2.setMinimumSize(QtCore.QSize(75, 0))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.uiNear = QtWidgets.QDoubleSpinBox(uiLightEditor)
        self.uiNear.setObjectName("uiNear")
        self.horizontalLayout_2.addWidget(self.uiNear)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(uiLightEditor)
        self.label_3.setEnabled(True)
        self.label_3.setMinimumSize(QtCore.QSize(75, 0))
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.uiFar = QtWidgets.QDoubleSpinBox(uiLightEditor)
        self.uiFar.setObjectName("uiFar")
        self.horizontalLayout_3.addWidget(self.uiFar)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(uiLightEditor)
        self.label_4.setEnabled(True)
        self.label_4.setMinimumSize(QtCore.QSize(75, 0))
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.uiShadows = QtWidgets.QCheckBox(uiLightEditor)
        self.uiShadows.setText("")
        self.uiShadows.setObjectName("uiShadows")
        self.horizontalLayout_4.addWidget(self.uiShadows)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.retranslateUi(uiLightEditor)
        QtCore.QMetaObject.connectSlotsByName(uiLightEditor)

    def retranslateUi(self, uiLightEditor):
        _translate = QtCore.QCoreApplication.translate
        uiLightEditor.setWindowTitle(_translate("uiLightEditor", "Form"))
        self.label.setText(_translate("uiLightEditor", "Light Intensity"))
        self.label_2.setText(_translate("uiLightEditor", "Near Range"))
        self.label_3.setText(_translate("uiLightEditor", "Far Range"))
        self.label_4.setText(_translate("uiLightEditor", "Cast Shadows"))
