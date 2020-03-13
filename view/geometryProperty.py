# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'geometryProperty.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SketchProperty(object):
    def setupUi(self, SketchProperty):
        SketchProperty.setObjectName("SketchProperty")
        SketchProperty.resize(244, 313)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(SketchProperty)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.GroupBoxGP = QtWidgets.QGroupBox(SketchProperty)
        self.GroupBoxGP.setObjectName("GroupBoxGP")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.GroupBoxGP)
        self.verticalLayout.setObjectName("verticalLayout")
        self.treeWidget = QtWidgets.QTreeWidget(self.GroupBoxGP)
        self.treeWidget.setObjectName("treeWidget")
        self.verticalLayout.addWidget(self.treeWidget)
        self.verticalLayout_3.addWidget(self.GroupBoxGP)

        self.retranslateUi(SketchProperty)
        QtCore.QMetaObject.connectSlotsByName(SketchProperty)

    def retranslateUi(self, SketchProperty):
        _translate = QtCore.QCoreApplication.translate
        SketchProperty.setWindowTitle(_translate("SketchProperty", "Form"))
        self.GroupBoxGP.setTitle(_translate("SketchProperty", "Geometry Properties"))
        self.treeWidget.headerItem().setText(0, _translate("SketchProperty", "Key"))
        self.treeWidget.headerItem().setText(1, _translate("SketchProperty", "Value"))
