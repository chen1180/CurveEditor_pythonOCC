from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from view import nodeProperty, property, curveProperty, \
    newSketchProperty, clippingPlaneProperty, viewPortProperty
from data.model import SceneGraphModel
from data.node import *


class PropertyEditor(QWidget):
    def __init__(self, parent=None):
        super(PropertyEditor, self).__init__(parent)
        self.ui = property.Ui_Form()
        self.ui.setupUi(self)

        self._model = None
        self._editor_dict = {}

        self._nodeEditor = NodeEditor(self)
        self._pointEditor = PointEditor(self)
        self._lineEditor = LineEditor(self)
        self._bezierCurveEditor = BezierCurveEditor(self)
        self._bsplineEditor = BsplineEditor(self)
        self._bezierSurfaceEditor = BezierSurfaceEditor(self)
        self._ruledSurfaceEditor = RuledSurfaceEditor(self)
        self._revolutedSurfaceEditor = RevolutedSurfaceEditor(self)
        self._sweepSurfaceEditor = SweepSurfaceEditor(self)
        self.addEditor(self._nodeEditor, "Node")
        self.addEditor(self._pointEditor, "Point")
        self.addEditor(self._lineEditor, "Line")
        self.addEditor(self._bezierCurveEditor, "Bezier Curve")
        self.addEditor(self._bsplineEditor, "Bspline")
        self.addEditor(self._bezierSurfaceEditor, "Bezier Surface")
        self.addEditor(self._revolutedSurfaceEditor, "Surface of Revolution")
        self.addEditor(self._ruledSurfaceEditor, "Ruled Surface")
        self.addEditor(self._sweepSurfaceEditor, "Sweep Surface")

    def addEditor(self, editor: QWidget, type: str):
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

    def setSelection(self, current: QModelIndex, old: QModelIndex):
        node = current.internalPointer()

        if node is not None:
            typeInfo = node.typeInfo()
            self.showEditor(typeInfo)
        for type, editor in self._editor_dict.items():
            editor.setSelection(current)


class NodeEditor(QWidget):
    def __init__(self, parent=None):
        super(NodeEditor, self).__init__(parent)
        self.ui = nodeProperty.Ui_uiNodeEditor()
        self.ui.setupUi(self)
        self._dataMapper = QDataWidgetMapper()

    def setModel(self, model):
        self._model = model
        self._dataMapper.setModel(model)
        self._dataMapper.addMapping(self.ui.uiName, 0)
        self._dataMapper.addMapping(self.ui.uiTypeInfo, 1)

    def setSelection(self, current: QModelIndex):
        parent = current.parent()
        self._dataMapper.setRootIndex(parent)
        self._dataMapper.setCurrentModelIndex(current)


class PointEditor(QWidget):
    def __init__(self, parent=None):
        super(PointEditor, self).__init__(parent)
        self.ui = viewPortProperty.Ui_Form()
        self.ui.setupUi(self)
        self._dataMapper = QDataWidgetMapper()

    def setModel(self, model):
        self._model: SceneGraphModel = model
        self._dataMapper.setModel(model)
        self._dataMapper.addMapping(self.ui.uiViewport, 2)
        self._dataMapper.addMapping(self.ui.uiViewportAuxiliry, 3)
        self._dataMapper.addMapping(self.ui.uiViewportName, 4)
        self._dataMapper.addMapping(self.ui.uiViewportCoordinate, 5)

    """INPUTS: QModelIndex"""

    def setSelection(self, current):
        parent = current.parent()
        self._dataMapper.setRootIndex(parent)
        self._dataMapper.setCurrentModelIndex(current)
        # node information can be obtained
        # node = self._model.getNode(current)


class LineEditor(QWidget):
    def __init__(self, parent=None):
        super(LineEditor, self).__init__(parent)
        self.ui = viewPortProperty.Ui_Form()
        self.ui.setupUi(self)
        self._dataMapper = QDataWidgetMapper()

    def setModel(self, model):
        self._model: SceneGraphModel = model
        self._dataMapper.setModel(model)
        self._dataMapper.addMapping(self.ui.uiViewport, 2)
        self._dataMapper.addMapping(self.ui.uiViewportAuxiliry, 3)
        self._dataMapper.addMapping(self.ui.uiViewportName, 4)
        self._dataMapper.addMapping(self.ui.uiViewportCoordinate, 5)

    """INPUTS: QModelIndex"""

    def setSelection(self, current):
        parent: QModelIndex = current.parent()
        self._dataMapper.setRootIndex(parent)
        self._dataMapper.setCurrentModelIndex(current)


class BezierCurveEditor(QWidget):
    def __init__(self, parent=None):
        super(BezierCurveEditor, self).__init__(parent)
        self.ui = viewPortProperty.Ui_Form()
        self.ui.setupUi(self)
        self._dataMapper = QDataWidgetMapper()

    def setModel(self, model):
        self._model: SceneGraphModel = model
        self._dataMapper.setModel(model)
        self._dataMapper.addMapping(self.ui.uiViewport, 2)
        self._dataMapper.addMapping(self.ui.uiViewportAuxiliry, 3)
        self._dataMapper.addMapping(self.ui.uiViewportName, 4)
        self._dataMapper.addMapping(self.ui.uiViewportCoordinate, 5)

    """INPUTS: QModelIndex"""

    def setSelection(self, current):
        parent: QModelIndex = current.parent()
        self._dataMapper.setRootIndex(parent)
        self._dataMapper.setCurrentModelIndex(current)


class BsplineEditor(QWidget):
    def __init__(self, parent=None):
        super(BsplineEditor, self).__init__(parent)
        self.ui = viewPortProperty.Ui_Form()
        self.ui.setupUi(self)
        self._dataMapper = QDataWidgetMapper()

    def setModel(self, model):
        self._model: SceneGraphModel = model
        self._dataMapper.setModel(model)
        self._dataMapper.addMapping(self.ui.uiViewport, 2)
        self._dataMapper.addMapping(self.ui.uiViewportAuxiliry, 3)
        self._dataMapper.addMapping(self.ui.uiViewportName, 4)
        self._dataMapper.addMapping(self.ui.uiViewportCoordinate, 5)

    """INPUTS: QModelIndex"""

    def setSelection(self, current):
        parent: QModelIndex = current.parent()
        self._dataMapper.setRootIndex(parent)
        self._dataMapper.setCurrentModelIndex(current)


from data.design.geometry import *
from OCC.Core.gp import gp_Vec
from OCC.Core.Graphic3d import Graphic3d_ClipPlane, Graphic3d_Vec4d
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB


class SurfaceEditor(QWidget):
    def __init__(self, parent=None):
        super(SurfaceEditor, self).__init__(parent)
        self.ui = clippingPlaneProperty.Ui_Form()
        self.ui.setupUi(self)
        self._dataMapper = QDataWidgetMapper()
        self.ui.checkBox.stateChanged.connect(self.clippingOn)
        self.ui.buttonGroup.buttonClicked.connect(self.changeClippingPlane)
        self.ui.animatePushButton.pressed.connect(self.animateClipping)
        self.ui.resetPushButton.pressed.connect(self.resetClipping)

    def setModel(self, model):
        self._model = model
        self._dataMapper.setModel(model)

    """INPUTS: QModelIndex"""

    def setSelection(self, current):
        parent = current.parent()
        self._dataMapper.setRootIndex(parent)
        self._dataMapper.setCurrentModelIndex(current)

    def setClippingPlane(self):
        # clip plane number one, by default xOy
        clip_plane_1 = Graphic3d_ClipPlane()
        # set hatch on
        clip_plane_1.SetCapping(True)
        clip_plane_1.SetCappingHatch(True)
        # off by default, user will have to enable it
        clip_plane_1.SetOn(True)
        # set clip plane color
        aMat = clip_plane_1.CappingMaterial()
        aColor = Quantity_Color(0.5, 0.6, 0.7, Quantity_TOC_RGB)
        aMat.SetAmbientColor(aColor)
        aMat.SetDiffuseColor(aColor)
        clip_plane_1.SetCappingMaterial(aMat)
        self.clippingPlane = clip_plane_1

    def clippingOn(self, checked):
        if checked:
            self._surface.GetAIS_Object().AddClipPlane(self.clippingPlane)
            self.clippingPlane.SetOn(True)
        else:
            self._surface.GetAIS_Object().RemoveClipPlane(self.clippingPlane)
            self.clippingPlane.SetOn(False)
        self._surface.myContext.UpdateCurrentViewer()

    def changeClippingPlane(self):
        equation = Graphic3d_Vec4d(0., 0., 1., 0.0)
        checkedButton = self.ui.buttonGroup.checkedButton().text()
        if checkedButton == "X":
            equation = Graphic3d_Vec4d(1., 0., 0., 0.)
        elif checkedButton == "Y":
            equation = Graphic3d_Vec4d(0., 1., 0., 0.)
        self.clippingPlane.SetEquation(equation)
        self._surface.myContext.UpdateCurrentViewer()

    def animateClipping(self):
        if self.ui.checkBox.isChecked():
            plane_definition = self.clippingPlane.ToPlane()  # it's a gp_Pln
            h = 1.0
            direction = gp_Vec(0., 0., h)
            checkedButton = self.ui.buttonGroup.checkedButton().text()
            if checkedButton == "X":
                direction = gp_Vec(h, 0., 0.)
            elif checkedButton == "Y":
                direction = gp_Vec(0., h, 0.)
            for i in range(100):
                plane_definition.Translate(direction)
                self.clippingPlane.SetEquation(plane_definition)
                self._surface.myContext.UpdateCurrentViewer()

    def resetClipping(self):
        if self.ui.checkBox.isChecked():
            self._surface.GetAIS_Object().RemoveClipPlane(self.clippingPlane)
            self.setClippingPlane()
            self._surface.GetAIS_Object().AddClipPlane(self.clippingPlane)
            self._surface.myContext.UpdateCurrentViewer()


class RuledSurfaceEditor(SurfaceEditor):
    def __init__(self, parent=None):
        super(RuledSurfaceEditor, self).__init__(parent)

    def setSelection(self, current):
        super(RuledSurfaceEditor, self).setSelection(current)
        # node information can be obtained
        node = self._model.getNode(current)
        if type(node) == ExtrudedSurfaceNode:
            self._surface: Surface_LinearExtrusion = node.getSketchObject()
            self.setClippingPlane()
            self.changeClippingPlane()


class BezierSurfaceEditor(SurfaceEditor):
    def __init__(self, parent=None):
        super(BezierSurfaceEditor, self).__init__(parent)

    def setSelection(self, current):
        super(BezierSurfaceEditor, self).setSelection(current)
        # node information can be obtained
        node = self._model.getNode(current)
        if type(node) == BezierSurfaceNode:
            self._surface = node.getSketchObject()
            self.setClippingPlane()
            self.changeClippingPlane()


class RevolutedSurfaceEditor(SurfaceEditor):
    def __init__(self, parent=None):
        super(RevolutedSurfaceEditor, self).__init__(parent)

    def setSelection(self, current):
        super(RevolutedSurfaceEditor, self).setSelection(current)
        # node information can be obtained
        node = self._model.getNode(current)
        if type(node) == RevolvedSurfaceNode:
            self._surface = node.getSketchObject()
            self.setClippingPlane()
            self.changeClippingPlane()


class SweepSurfaceEditor(SurfaceEditor):
    def __init__(self, parent=None):
        super(SweepSurfaceEditor, self).__init__(parent)

    def setSelection(self, current):
        super(SweepSurfaceEditor, self).setSelection(current)
        # node information can be obtained
        node = self._model.getNode(current)
        if type(node) == SweepSurfaceNode:
            self._surface = node.getSketchObject()
            self.setClippingPlane()
            self.changeClippingPlane()


from OCC.Core.gp import gp_Pnt, gp_Pln, gp_Dir, gp_Ax3, gp
from OCC.Core.Geom import *
from OCC.Core.AIS import *

class Sketch_NewSketchEditor(QWidget):
    def __init__(self, parent=None, display=None):
        super(Sketch_NewSketchEditor, self).__init__(parent)
        self.ui = newSketchProperty.Ui_newSketchEditor()
        self.ui.setupUi(self)
        self.ui.uiXYPlane.setChecked(True)
        self._display = display
        self.ui.uiOk.accepted.connect(self.constructGrid)
        self.ui.uiOk.rejected.connect(self.close)
        self.setWindowModality(Qt.ApplicationModal)
        self._plane = gp_Pln(gp_Pnt(0.0, 0.0, 0.0), gp_Dir(0.0, 0.0, 1.0))
        self.show()

    def constructGrid(self):
        self.dir = gp_Dir()
        offset=self.ui.uiOffset.value()
        if self.ui.uiXYPlane.isChecked():
            self.dir = gp_Dir(0.0, 0.0, 1.0)
            pnt=gp_Pnt(0.0,0.0,offset)
            self._display.View_Top()
        if self.ui.uiXZPlane.isChecked():
            self.dir = gp_Dir(0.0, 1.0, 0.0)
            pnt = gp_Pnt(0.0, offset, 0.0)
            self._display.View_Front()
        if self.ui.uiYZPlane.isChecked():
            self.dir = gp_Dir(1.0, 0.0, 0.0)
            pnt = gp_Pnt(offset, 0.0, 0.0)
            self._display.View_Right()
        self._coordinate = gp_Ax3(pnt, self._plane.Axis().Direction())
        self._display.Viewer.SetPrivilegedPlane( self._coordinate)
        self.close()

    def getCoordinate(self):
        return self._coordinate
