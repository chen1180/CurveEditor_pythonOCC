from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from view import nodeProperty, property,  \
    newSketchProperty, clippingPlaneProperty, viewPortProperty
from data.model import SceneGraphModel
from data.node import *
from data.design.geometry import *
from OCC.Core.gp import *

class PropertyEditor(QWidget):
    """
    This is property dock window controller.
    It will popup window accordingly by different node type
    """

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
        self._bsplineSurfaceEditor = BsplineSurfaceEditor(self)
        self._ruledSurfaceEditor = RuledSurfaceEditor(self)
        self._revolutedSurfaceEditor = RevolutedSurfaceEditor(self)
        self._sweepSurfaceEditor = SweepSurfaceEditor(self)
        self._importSurfaceEditor = ImportedSurfaceEditor(self)
        self.addEditor(self._nodeEditor, NodeType.Node)
        self.addEditor(self._pointEditor, NodeType.PointNode)
        self.addEditor(self._lineEditor, NodeType.LineNode)
        self.addEditor(self._bezierCurveEditor, NodeType.BezierNode)
        self.addEditor(self._bsplineEditor, NodeType.BsplineNode)
        self.addEditor(self._bezierSurfaceEditor, NodeType.BezierSurfaceNode)
        self.addEditor(self._bsplineSurfaceEditor, NodeType.BsplineSurfaceNode)
        self.addEditor(self._revolutedSurfaceEditor, NodeType.RevolvedSurfaceNode)
        self.addEditor(self._ruledSurfaceEditor, NodeType.ExtrudedSurfaceNode)
        self.addEditor(self._sweepSurfaceEditor, NodeType.SweepSurfaceNode)
        self.addEditor(self._importSurfaceEditor, NodeType.ImportedSurfaceNode)
    def addEditor(self, editor: QWidget, type: str):
        """
        This is the property window UI constructor.
        @param editor: Custom section (Usually create in Qt Designer)
        @param type: The node type corresponding to popup window.
        @return: None
        """
        if type == NodeType.Node:
            self.ui.layoutNode.addWidget(editor)
        else:
            self.ui.layoutSpec.addWidget(editor)
            editor.setVisible(False)
        self._editor_dict[type] = editor

    def setModel(self, model):
        """
        Set model for widget view (Model-View controller design pattern)
        @param model: model type (subclass of QAbstractModel)
        @return:
        """
        self._model = model
        for type, editor in self._editor_dict.items():
            editor.setModel(self._model)

    def showEditor(self, typeInfo):
        """
        Set editor visible, others invisible.
        When certain node (for example "PointNode") is selected, point property window will be visible.
        However other type of window will be hidden)

        @param typeInfo: Node type
        @return:
        """
        for type, editor in self._editor_dict.items():
            if type == "Node":
                continue
            if type == typeInfo:
                editor.setVisible(True)
            else:
                editor.setVisible(False)

    def setSelection(self, current: QModelIndex, old: QModelIndex):
        """
        When mouse click a node in the treeview, this function will receive a current QModelIndex, corresponding window will popup.
        @param current: current modelIndex
        @param old: old modelIndex
        @return:
        """
        node = current.internalPointer()
        if node is not None:
            typeInfo = node.typeInfo()
            self.showEditor(typeInfo)
        for type, editor in self._editor_dict.items():
            editor.setSelection(current)


class NodeEditor(QWidget):
    """
    General property window. (Applied to all nodes)
    """

    def __init__(self, parent=None):
        super(NodeEditor, self).__init__(parent)
        self.ui = nodeProperty.Ui_uiNodeEditor()
        self.ui.setupUi(self)
        self._dataMapper = QDataWidgetMapper()

    def setModel(self, model):
        """
        Map the UI slot with the custom tree data structure
        (Check data/nodel.py or data/model.py for more information)
        @param model: tree model
        @return:
        """
        self._model = model
        self._dataMapper.setModel(model)
        self._dataMapper.addMapping(self.ui.uiName, 0)
        self._dataMapper.addMapping(self.ui.uiTypeInfo, 1)

    def setSelection(self, current: QModelIndex):
        parent = current.parent()
        self._dataMapper.setRootIndex(parent)
        self._dataMapper.setCurrentModelIndex(current)


class PointEditor(QWidget):
    """
    Point property editor.
    """

    def __init__(self, parent=None):
        super(PointEditor, self).__init__(parent)
        self.ui = viewPortProperty.Ui_Form()
        self.ui.setupUi(self)
        self._dataMapper = QDataWidgetMapper()

    def setModel(self, model):
        """
        Map UI with the tree model data structure
        @param model: tree model
        @return:
        """
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
    """
    Line property window
    """
    def __init__(self, parent=None):
        super(LineEditor, self).__init__(parent)
        self.ui = viewPortProperty.Ui_Form()
        self.ui.setupUi(self)
        self._dataMapper = QDataWidgetMapper()

    def setModel(self, model):
        """
              Map UI with the tree model data structure
              @param model: tree model
              @return:
              """
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
    """
    Bezier curve property window
    """
    def __init__(self, parent=None):
        super(BezierCurveEditor, self).__init__(parent)
        self.ui = viewPortProperty.Ui_Form()
        self.ui.setupUi(self)
        self._dataMapper = QDataWidgetMapper()

    def setModel(self, model):
        """
              Map UI with the tree model data structure
              @param model: tree model
              @return:
        """
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
    """
    Bspline property window
    """
    def __init__(self, parent=None):
        super(BsplineEditor, self).__init__(parent)
        self.ui = viewPortProperty.Ui_Form()
        self.ui.setupUi(self)
        self._dataMapper = QDataWidgetMapper()

    def setModel(self, model):
        """
              Map UI with the tree model data structure
              @param model: tree model
              @return:
        """
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





class SurfaceEditor(QWidget):
    """
    Base class for surface editor class
    """
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
        """
              Map UI with the tree model data structure
              @param model: tree model
              @return:
        """
        self._model = model
        self._dataMapper.setModel(model)

    """INPUTS: QModelIndex"""

    def setSelection(self, current):
        parent = current.parent()
        self._dataMapper.setRootIndex(parent)
        self._dataMapper.setCurrentModelIndex(current)

    # def setClippingPlane(self):
    #     # clip plane number one, by default xOy
    #     clip_plane_1 = Graphic3d_ClipPlane(gp_Pln(self.myCenter,gp_Dir(1., 0., 0.)))
    #     # set hatch on
    #     clip_plane_1.SetCapping(True)
    #     clip_plane_1.SetCappingHatch(True)
    #     # off by default, user will have to enable it
    #     clip_plane_1.SetOn(True)
    #     # set clip plane color
    #     aMat = clip_plane_1.CappingMaterial()
    #     aColor = Quantity_Color(0.5, 0.6, 0.7, Quantity_TOC_RGB)
    #     aMat.SetAmbientColor(aColor)
    #     aMat.SetDiffuseColor(aColor)
    #     clip_plane_1.SetCappingMaterial(aMat)
    #     self.clippingPlane = clip_plane_1
    #     self.myGeometry = Geom_Plane(self.clippingPlane.ToPlane())
    #     self.myGeometry.SetLocation(self.myCenter)
    #     self.myAIS_Plane = AIS_Plane(self.myGeometry)
    #     # self._surface.myContext.Display(self.myAIS_Plane, True)

    def clippingOn(self, checked):
        """
        set clipping plane on/off
        @param checked: bool
        @return:
        """
        self._surface.OnClippingPlane(checked)

    def changeClippingPlane(self):
        """
        Change clipping plane equation by choosing radio button.
        @return:
        """
        dir = gp_Dir(0., 0., 1.)
        checkedButton = self.ui.buttonGroup.checkedButton()
        if checkedButton == self.ui.xRadioButton:
            dir = gp_Dir(1., 0., 0.)
        elif checkedButton == self.ui.yRadioButton:
            dir = gp_Dir(0., 1., 0.)
        elif checkedButton == self.ui.zRadioButton:
            dir = gp_Dir(0., 0., 1.)
        self._surface.UpdateClippingPlane(dir)

    def animateClipping(self):
        """
        Animate clipping process
        @return:
        """
        if self.ui.checkBox.isChecked():
            h = 1.0
            direction = gp_Vec(0., 0., h)
            checkedButton = self.ui.buttonGroup.checkedButton().text()
            if checkedButton == "X":
                direction = gp_Vec(h, 0., 0.)
            elif checkedButton == "Y":
                direction = gp_Vec(0., h, 0.)

            for i in range(100): # the constant number means animation time.
                self._surface.TranslateClippingPlane(direction)

    def resetClipping(self):
        """
        Reset clipping plane to the initial position
        @return:
        """
        if self.ui.checkBox.isChecked():
            self.changeClippingPlane()


class RuledSurfaceEditor(SurfaceEditor):
    """Ruled surface editor (Inherited from Surface Editor)"""
    def __init__(self, parent=None):
        super(RuledSurfaceEditor, self).__init__(parent)

    def setSelection(self, current):
        super(RuledSurfaceEditor, self).setSelection(current)
        # node information can be obtained
        node = self._model.getNode(current)
        if type(node) == ExtrudedSurfaceNode:
            self._surface: Surface_LinearExtrusion = node.getSketchObject()


class BezierSurfaceEditor(SurfaceEditor):
    """Bezier surface editor (Inherited from Surface Editor)"""
    def __init__(self, parent=None):
        super(BezierSurfaceEditor, self).__init__(parent)

    def setSelection(self, current):
        super(BezierSurfaceEditor, self).setSelection(current)
        # node information can be obtained
        node = self._model.getNode(current)
        if type(node) == BezierSurfaceNode:
            self._surface = node.getSketchObject()
            self.changeClippingPlane()
class BsplineSurfaceEditor(SurfaceEditor):
    """Bspline surface editor (Inherited from Surface Editor)"""
    def __init__(self, parent=None):
        super(BsplineSurfaceEditor, self).__init__(parent)

    def setSelection(self, current):
        super(BsplineSurfaceEditor, self).setSelection(current)
        # node information can be obtained
        node = self._model.getNode(current)
        if type(node) == BsplineSurfaceNode:
            self._surface = node.getSketchObject()
            self.changeClippingPlane()

class RevolutedSurfaceEditor(SurfaceEditor):
    """Revolved surface editor (Inherited from Surface Editor)"""
    def __init__(self, parent=None):
        super(RevolutedSurfaceEditor, self).__init__(parent)

    def setSelection(self, current):
        super(RevolutedSurfaceEditor, self).setSelection(current)
        # node information can be obtained
        node = self._model.getNode(current)
        if type(node) == RevolvedSurfaceNode:
            self._surface = node.getSketchObject()
            self.changeClippingPlane()


class SweepSurfaceEditor(SurfaceEditor):
    """Sweep surface editor (Inherited from Surface Editor)"""
    def __init__(self, parent=None):
        super(SweepSurfaceEditor, self).__init__(parent)

    def setSelection(self, current):
        super(SweepSurfaceEditor, self).setSelection(current)
        # node information can be obtained
        node = self._model.getNode(current)
        if type(node) == SweepSurfaceNode:
            self._surface = node.getSketchObject()
            self.changeClippingPlane()

class ImportedSurfaceEditor(SurfaceEditor):
    """Import surface editor (Inherited from Surface Editor)"""
    def __init__(self, parent=None):
        super(ImportedSurfaceEditor, self).__init__(parent)

    def setSelection(self, current):
        super(ImportedSurfaceEditor, self).setSelection(current)
        # node information can be obtained
        node = self._model.getNode(current)
        if type(node) == ImportedSurfaceNode:
            self._surface = node.getSketchObject()
            self.changeClippingPlane()

class Sketch_NewSketchEditor(QWidget):
    """
    UI window for creation of new sketch plane
    """
    def __init__(self, parent=None, display=None):
        """

        @param parent: parent widget
        @param display: openGL display handle
        """
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
        offset = self.ui.uiOffset.value()
        if self.ui.uiXYPlane.isChecked():
            self.dir = gp_Dir(0.0, 0.0, 1.0)
            pnt = gp_Pnt(0.0, 0.0, offset)
            self._display.View_Top()
        if self.ui.uiXZPlane.isChecked():
            self.dir = gp_Dir(0.0, 1.0, 0.0)
            pnt = gp_Pnt(0.0, offset, 0.0)
            self._display.View_Front()
        if self.ui.uiYZPlane.isChecked():
            self.dir = gp_Dir(1.0, 0.0, 0.0)
            pnt = gp_Pnt(offset, 0.0, 0.0)
            self._display.View_Right()
        self._coordinate = gp_Ax3(pnt, self.dir)
        self._display.Viewer.SetPrivilegedPlane(self._coordinate)
        self.close()

    def getCoordinate(self):
        return self._coordinate
