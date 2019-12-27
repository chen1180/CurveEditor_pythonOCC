# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cameraProperty.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_form(object):
    def setupUi(self, form):
        form.setObjectName("form")
        form.resize(294, 76)
        self.verticalLayout = QtWidgets.QVBoxLayout(form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(form)
        self.label.setEnabled(True)
        self.label.setMinimumSize(QtCore.QSize(75, 0))
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.uiBlur = QtWidgets.QCheckBox(form)
        self.uiBlur.setText("")
        self.uiBlur.setObjectName("uiBlur")
        self.horizontalLayout.addWidget(self.uiBlur)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(form)
        self.label_2.setEnabled(True)
        self.label_2.setMinimumSize(QtCore.QSize(75, 0))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.uiShakeIntensity = QtWidgets.QDoubleSpinBox(form)
        self.uiShakeIntensity.setObjectName("uiShakeIntensity")
        self.horizontalLayout_2.addWidget(self.uiShakeIntensity)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(form)
        QtCore.QMetaObject.connectSlotsByName(form)

    def retranslateUi(self, form):
        _translate = QtCore.QCoreApplication.translate
        form.setWindowTitle(_translate("form", "Form"))
        self.label.setText(_translate("form", "Motion Blur"))
        self.label_2.setText(_translate("form", "Shake Intensity"))
