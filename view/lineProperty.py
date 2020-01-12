# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lineProperty.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_uiLineEditor(object):
    def setupUi(self, uiLineEditor):
        uiLineEditor.setObjectName("uiLineEditor")
        uiLineEditor.resize(311, 144)
        self.verticalLayout = QtWidgets.QVBoxLayout(uiLineEditor)
        self.verticalLayout.setObjectName("verticalLayout")
        self.geometryTreeView = QtWidgets.QTreeView(uiLineEditor)
        self.geometryTreeView.setObjectName("geometryTreeView")
        self.verticalLayout.addWidget(self.geometryTreeView)

        self.retranslateUi(uiLineEditor)
        QtCore.QMetaObject.connectSlotsByName(uiLineEditor)

    def retranslateUi(self, uiLineEditor):
        _translate = QtCore.QCoreApplication.translate
        uiLineEditor.setWindowTitle(_translate("uiLineEditor", "Form"))
