from PyQt5 import QtGui, QtWidgets, QtCore, uic
import sys
from view import lightProperty, nodeProperty, property, transformProperty, cameraProperty, curveProperty, \
    newSketchProperty, lineProperty
from data.model import SceneGraphModel


class PropertyEditor(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(PropertyEditor, self).__init__(parent)
        self.ui = property.Ui_Form()
        self.ui.setupUi(self)

        self._model = None
        self._editor_dict = {}

        self._nodeEditor = NodeEditor(self)
        self._pointEditor = PointEditor(self)
        self._lineEditor = LineEditor(self)
        self.addEditor(self._nodeEditor, "Node")
        self.addEditor(self._pointEditor, "Point")
        self.addEditor(self._lineEditor, "Line")

    def addEditor(self, editor: QtWidgets.QWidget, type: str):
        if type == "Node":
            self.ui.layoutNode.addWidget(editor)
        else:
            self.ui.layoutSpec.addWidget(editor)
            editor.setVisible(False)
        self._editor_dict[type] = editor

    def setModel(self, model):
        self._model = model
        for type, editor in self._editor_dict.items():
            editor.setModel(self._model)

    def showEditor(self, typeInfo):
        for type, editor in self._editor_dict.items():
            if type == "Node":
                continue
            if type == typeInfo:
                editor.setVisible(True)
            else:
                editor.setVisible(False)

    def setSelection(self, current: QtCore.QModelIndex, old: QtCore.QModelIndex):
        node = current.internalPointer()

        if node is not None:
            typeInfo = node.typeInfo()

        self.showEditor(typeInfo)

        for type, editor in self._editor_dict.items():
            editor.setSelection(current)


class NodeEditor(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(NodeEditor, self).__init__(parent)
        self.ui = nodeProperty.Ui_uiNodeEditor()
        self.ui.setupUi(self)
        self._dataMapper = QtWidgets.QDataWidgetMapper()

    def setModel(self, model):
        self._model = model
        self._dataMapper.setModel(model)
        self._dataMapper.addMapping(self.ui.uiName, 0)
        self._dataMapper.addMapping(self.ui.uiTypeInfo, 1)

    def setSelection(self, current: QtCore.QModelIndex):
        parent = current.parent()
        self._dataMapper.setRootIndex(parent)
        self._dataMapper.setCurrentModelIndex(current)


class CurveEditor(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(CurveEditor, self).__init__(parent)
        self.ui = curveProperty.Ui_uiCurveEditor()
        self.ui.setupUi(self)
        self._dataMapper = QtWidgets.QDataWidgetMapper()
        # set submission policy. The data will be updated until certain action is compelte (No enter press is required)
        # https://www.qtcentre.org/threads/45754-How-can-I-work-with-QDataWidgetMapper

    def setModel(self, model):
        self._model = model
        self._dataMapper.setModel(model)
        self._dataMapper.addMapping(self.ui.uiCurveOrder, 2)
        self._dataMapper.addMapping(self.ui.uiCurveSubdivision, 3)
        self._dataMapper.addMapping(self.ui.uiCurveKnots, 4)
        self._dataMapper.addMapping(self.ui.uiCurveWeights, 5)

    """INPUTS: QModelIndex"""

    def setSelection(self, current):
        parent = current.parent()
        self._dataMapper.setRootIndex(parent)
        self._dataMapper.setCurrentModelIndex(current)


from view.sketchProperty import Ui_SketchProperty


class PointEditor(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(PointEditor, self).__init__(parent)
        self.ui = Ui_SketchProperty()
        self.ui.setupUi(self)
        self._dataMapper = QtWidgets.QDataWidgetMapper()

    def setModel(self, model):
        self._model: SceneGraphModel = model
        self._dataMapper.setModel(model)
        self._dataMapper.addMapping(self.ui.ComboBoxColor, 2)
        self._dataMapper.addMapping(self.ui.LineEditPoint1, 3)

    """INPUTS: QModelIndex"""

    def setSelection(self, current):
        parent = current.parent()
        self._dataMapper.setRootIndex(parent)
        self._dataMapper.setCurrentModelIndex(current)


class LineEditor(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(LineEditor, self).__init__(parent)
        self.ui = lineProperty.Ui_uiLineEditor()
        self.ui.setupUi(self)
        self._dataMapper = QtWidgets.QDataWidgetMapper()

    def setModel(self, model):
        self._model: SceneGraphModel = model
        self._dataMapper.setModel(model)
        self._dataMapper.addMapping(self.ui.geometryTreeView, 2)

    """INPUTS: QModelIndex"""

    def setSelection(self, current):
        parent = current.parent()
        self._dataMapper.setRootIndex(parent)
        self._dataMapper.setCurrentModelIndex(current)


from OCC.Core.gp import gp_Pnt, gp_Pln, gp_Dir, gp_Ax3, gp
from OCC.Core.Aspect import Aspect_GDM_Lines, Aspect_GT_Rectangular
from OCC.Core.V3d import V3d_Viewer


class Sketch_NewSketchEditor(QtWidgets.QWidget):
    def __init__(self, parent=None, display=None):
        super(Sketch_NewSketchEditor, self).__init__(parent)
        self.ui = newSketchProperty.Ui_newSketchEditor()
        self.ui.setupUi(self)
        self._display = display
        self.ui.uiOk.accepted.connect(self.constructGrid)
        self.ui.uiOk.rejected.connect(self.close)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.show()

    def constructGrid(self):
        self.dir = gp_Dir()
        if self.ui.uiXYPlane.isChecked():
            self.dir = gp_Dir(0.0, 0.0, 1.0)
            self._display.View_Top()
        if self.ui.uiXZPlane.isChecked():
            self.dir = gp_Dir(0.0, 1.0, 0.0)
            self._display.View_Front()
        if self.ui.uiYZPlane.isChecked():
            self.dir = gp_Dir(1.0, 0.0, 0.0)
            self._display.View_Right()
        aPlane = gp_Pln(gp_Pnt(0.0, 0.0, 0.0), self.dir)
        self.displayGrid(aPlane, 0.0, 0.0, 1.0, 1.0, 0.0, 100, 100, self.ui.uiOffset.value())
        self.close()

    def displayGrid(self, aPlane, xOrigin, yOrigin, xStep, yStep, rotation, xSize, ySize, offset):
        ax3 = gp_Ax3(aPlane.Location(), aPlane.Axis().Direction())
        self._display.Viewer.SetPrivilegedPlane(ax3)
        assert isinstance(self._display.Viewer, V3d_Viewer)
        theAx3 = self._display.Viewer.PrivilegedPlane()
        dir = theAx3.Direction()
        # print(dir.X(), dir.Y(), dir.Z())
        self._display.Viewer.SetRectangularGridValues(xOrigin, yOrigin, xStep, yStep, rotation)
        self._display.Viewer.SetRectangularGridGraphicValues(xSize, ySize, offset)
        self._display.Viewer.ActivateGrid(Aspect_GT_Rectangular, Aspect_GDM_Lines)
        self._display.FitAll()
        self._display.Repaint()
