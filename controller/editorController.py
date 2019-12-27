from PyQt5 import QtGui, QtWidgets, QtCore, uic
import sys
from view import lightProperty, nodeProperty, property, transformProperty, cameraProperty,curveProperty
class PropertyEditor(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(PropertyEditor, self).__init__(parent)
        self.ui = property.Ui_Form()
        self.ui.setupUi(self)

        self._proxyModel = None

        self._nodeEditor = NodeEditor(self)
        self._lightEditor = LightEditor(self)
        self._cameraEditor = CameraEditor(self)
        self._transformEditor = TransformEditor(self)
        self._curveEditor=CurveEditor(self)

        self.ui.layoutNode.addWidget(self._nodeEditor)
        self.ui.layoutSpec.addWidget(self._lightEditor)
        self.ui.layoutSpec.addWidget(self._cameraEditor)
        self.ui.layoutSpec.addWidget(self._transformEditor)
        self.ui.layoutSpec.addWidget(self._curveEditor)

        self._lightEditor.setVisible(False)
        self._cameraEditor.setVisible(False)
        self._transformEditor.setVisible(False)
        self._curveEditor.setVisible(False)

    def setModel(self, proxyModel):
        self._proxyModel = proxyModel
        self._nodeEditor.setModel(proxyModel)
        self._lightEditor.setModel(proxyModel)
        self._cameraEditor.setModel(proxyModel)
        self._transformEditor.setModel(proxyModel)
        self._curveEditor.setModel(proxyModel)

    def setSelection(self, current: QtCore.QModelIndex, old: QtCore.QModelIndex):
        current = self._proxyModel.mapToSource(current)
        node = current.internalPointer()

        if node is not None:
            typeInfo = node.typeInfo()

        if typeInfo == "Camera":
            self._cameraEditor.setVisible(True)
            self._lightEditor.setVisible(False)
            self._transformEditor.setVisible(False)
            self._curveEditor.setVisible(False)
        elif typeInfo == "Light":
            self._cameraEditor.setVisible(False)
            self._lightEditor.setVisible(True)
            self._transformEditor.setVisible(False)
            self._curveEditor.setVisible(False)
        elif typeInfo == "Transform":
            self._cameraEditor.setVisible(False)
            self._lightEditor.setVisible(False)
            self._transformEditor.setVisible(True)
            self._curveEditor.setVisible(False)
        elif typeInfo == "Curve":
            self._cameraEditor.setVisible(False)
            self._lightEditor.setVisible(False)
            self._transformEditor.setVisible(False)
            self._curveEditor.setVisible(True)
        else:
            self._cameraEditor.setVisible(False)
            self._lightEditor.setVisible(False)
            self._transformEditor.setVisible(False)
            self._curveEditor.setVisible(False)

        self._nodeEditor.setSelection(current)
        self._cameraEditor.setSelection(current)
        self._lightEditor.setSelection(current)
        self._transformEditor.setSelection(current)
        self._curveEditor.setSelection(current)


class NodeEditor(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(NodeEditor, self).__init__(parent)
        self.ui = nodeProperty.Ui_uiNodeEditor()
        self.ui.setupUi(self)
        self._dataMapper = QtWidgets.QDataWidgetMapper()

    def setModel(self, proxyModel):
        self._proxyModel = proxyModel
        self._dataMapper.setModel(proxyModel.sourceModel())
        self._dataMapper.addMapping(self.ui.uiName, 0)
        self._dataMapper.addMapping(self.ui.uiTypeInfo, 1)

    def setSelection(self, current: QtCore.QModelIndex):
        parent = current.parent()
        self._dataMapper.setRootIndex(parent)
        self._dataMapper.setCurrentModelIndex(current)


class LightEditor(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(LightEditor, self).__init__(parent)
        self.ui = lightProperty.Ui_uiLightEditor()
        self.ui.setupUi(self)
        self._dataMapper = QtWidgets.QDataWidgetMapper()

    def setModel(self, proxyModel):
        self._proxyModel = proxyModel
        self._dataMapper.setModel(proxyModel.sourceModel())

        self._dataMapper.addMapping(self.ui.uiLightIntensity, 2)
        self._dataMapper.addMapping(self.ui.uiNear, 3)
        self._dataMapper.addMapping(self.ui.uiFar, 4)
        self._dataMapper.addMapping(self.ui.uiShadows, 5)

    """INPUTS: QModelIndex"""

    def setSelection(self, current):
        parent = current.parent()
        self._dataMapper.setRootIndex(parent)
        self._dataMapper.setCurrentModelIndex(current)


class CameraEditor(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(CameraEditor, self).__init__(parent)
        self.ui = cameraProperty.Ui_form()
        self.ui.setupUi(self)
        self._dataMapper = QtWidgets.QDataWidgetMapper()

    def setModel(self, proxyModel):
        self._proxyModel = proxyModel
        self._dataMapper.setModel(proxyModel.sourceModel())

        self._dataMapper.addMapping(self.ui.uiBlur, 2)
        self._dataMapper.addMapping(self.ui.uiShakeIntensity, 3)

    """INPUTS: QModelIndex"""

    def setSelection(self, current):
        parent = current.parent()
        self._dataMapper.setRootIndex(parent)
        self._dataMapper.setCurrentModelIndex(current)


class TransformEditor(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(TransformEditor, self).__init__(parent)
        self.ui = transformProperty.Ui_uiTransfromEditor()
        self.ui.setupUi(self)
        self._dataMapper = QtWidgets.QDataWidgetMapper()

    def setModel(self, proxyModel):
        self._proxyModel = proxyModel
        self._dataMapper.setModel(proxyModel.sourceModel())

        self._dataMapper.addMapping(self.ui.uiX, 2)
        self._dataMapper.addMapping(self.ui.uiY, 3)
        self._dataMapper.addMapping(self.ui.uiZ, 4)

    """INPUTS: QModelIndex"""
    def setSelection(self, current):
        parent = current.parent()
        self._dataMapper.setRootIndex(parent)

        self._dataMapper.setCurrentModelIndex(current)

class CurveEditor(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(CurveEditor, self).__init__(parent)
        self.ui =curveProperty.Ui_uiCurveEditor()
        self.ui.setupUi(self)
        self._dataMapper = QtWidgets.QDataWidgetMapper()
        #set submission policy. The data will be updated until certain action is compelte (No enter press is required)
        #https://www.qtcentre.org/threads/45754-How-can-I-work-with-QDataWidgetMapper
    def setModel(self, proxyModel):
        self._proxyModel = proxyModel
        self._dataMapper.setModel(proxyModel.sourceModel())
        self._dataMapper.addMapping(self.ui.uiCurveOrder, 2)
        self._dataMapper.addMapping(self.ui.uiCurveSubdivision, 3)
        self._dataMapper.addMapping(self.ui.uiCurveKnots,4)
        self._dataMapper.addMapping(self.ui.uiCurveWeights, 5)
    """INPUTS: QModelIndex"""
    def setSelection(self, current):
        parent = current.parent()
        self._dataMapper.setRootIndex(parent)
        self._dataMapper.setCurrentModelIndex(current)