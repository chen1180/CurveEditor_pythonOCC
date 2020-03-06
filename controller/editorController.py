from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from view import nodeProperty, property, curveProperty, \
    newSketchProperty, clippingPlaneProperty
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
        self._bezierSurfaceEditor = BezierSurfaceEditor(self)
        self._ruledSurfaceEditor = RuledSurfaceEditor(self)
        self._revolutedSurfaceEditor = RevolutedSurfaceEditor(self)
        self._sweepSurfaceEditor = SweepSurfaceEditor(self)
        self.addEditor(self._nodeEditor, "Node")
        self.addEditor(self._pointEditor, "Point")
        self.addEditor(self._lineEditor, "Line")
        self.addEditor(self._bezierCurveEditor, "Bezier Curve")
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


class CurveEditor(QWidget):
    def __init__(self, parent=None):
        super(CurveEditor, self).__init__(parent)
        self.ui = curveProperty.Ui_uiCurveEditor()
        self.ui.setupUi(self)
        self._dataMapper = QDataWidgetMapper()
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


from view.geometryProperty import Ui_SketchProperty


class PointEditor(QWidget):
    def __init__(self, parent=None):
        super(PointEditor, self).__init__(parent)
        self.ui = Ui_SketchProperty()
        self.ui.setupUi(self)
        self._dataMapper = QDataWidgetMapper()
        self.setupUI(1)

    def setupUI(self, point_size):
        self.poles_list = QTreeWidgetItem(self.ui.treeWidget)
        self.poles_list.setText(0, "Point")
        for i in range(point_size):
            coorinate_x_item = QTreeWidgetItem(self.poles_list)
            coorinate_x_item.setText(0, "x")
            coorinate_y_item = QTreeWidgetItem(self.poles_list)
            coorinate_y_item.setText(0, "y")
            x_spinbox = QDoubleSpinBox()
            x_spinbox.setRange(-10000, 10000)
            y_spinbox = QDoubleSpinBox()
            y_spinbox.setRange(-10000, 10000)
            self.ui.treeWidget.setItemWidget(coorinate_x_item, 1, x_spinbox)
            self.ui.treeWidget.setItemWidget(coorinate_y_item, 1, y_spinbox)

    def setModel(self, model):
        self._model: SceneGraphModel = model
        self._dataMapper.setModel(model)
        for i in range(self.poles_list.childCount()):
            currentItem = self.poles_list.child(i)
            # x: 2
            # y: 3
            self._dataMapper.addMapping(self.ui.treeWidget.itemWidget(currentItem, 1), 2 + i)

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
        self.ui = Ui_SketchProperty()
        self.ui.setupUi(self)
        self._dataMapper = QDataWidgetMapper()
        self.setupUI(2)

    def setupUI(self, point_size):
        self.poles_list = QTreeWidgetItem(self.ui.treeWidget)
        self.poles_list.setText(0, "Points")
        self.poles_list.setText(1, "2")
        for i in range(point_size):
            pole = QTreeWidgetItem(self.poles_list)
            pole.setText(0, "Point" + str(i + 1))
            pole_display = QLineEdit()
            pole_display.setDisabled(True)
            self.ui.treeWidget.setItemWidget(pole, 1, pole_display)
            coorinate_x_item = QTreeWidgetItem(pole)
            coorinate_x_item.setText(0, "x")
            coorinate_y_item = QTreeWidgetItem(pole)
            coorinate_y_item.setText(0, "y")
            x_spinbox = QDoubleSpinBox()
            x_spinbox.setRange(-10000, 10000)
            y_spinbox = QDoubleSpinBox()
            y_spinbox.setRange(-10000, 10000)
            self.ui.treeWidget.setItemWidget(coorinate_x_item, 1, x_spinbox)
            self.ui.treeWidget.setItemWidget(coorinate_y_item, 1, y_spinbox)

    def setModel(self, model):
        self._model: SceneGraphModel = model
        self._dataMapper.setModel(model)
        count = 0
        for i in range(self.poles_list.childCount()):
            poles = self.poles_list.child(i)
            self._dataMapper.addMapping(self.ui.treeWidget.itemWidget(poles, 1), 2 + count)
            count += 1
            for index in range(poles.childCount()):
                self._dataMapper.addMapping(self.ui.treeWidget.itemWidget(poles.child(index), 1), 2 + count)
                count += 1

    """INPUTS: QModelIndex"""

    def setSelection(self, current):
        parent: QModelIndex = current.parent()
        self._dataMapper.setRootIndex(parent)
        self._dataMapper.setCurrentModelIndex(current)


class BezierCurveEditor(QWidget):
    def __init__(self, parent=None):
        super(BezierCurveEditor, self).__init__(parent)
        self.ui = Ui_SketchProperty()
        self.ui.setupUi(self)
        self._dataMapper = QDataWidgetMapper()
        self.setupUI()
        self.generateUI(20)
        self.pole_size = 0

    def setupUI(self):
        self.degree = QTreeWidgetItem(self.ui.treeWidget, ["degree"])
        degree_display = QLineEdit()
        degree_display.setDisabled(True)
        self.ui.treeWidget.setItemWidget(self.degree, 1, degree_display)

        self.closed = QTreeWidgetItem(self.ui.treeWidget, ["Is closed"])
        closed_display = QLineEdit()
        closed_display.setDisabled(True)
        self.ui.treeWidget.setItemWidget(self.closed, 1, closed_display)

        self.rational = QTreeWidgetItem(self.ui.treeWidget, ["Is rational"])
        rational_display = QLineEdit()
        rational_display.setDisabled(True)
        self.ui.treeWidget.setItemWidget(self.rational, 1, rational_display)

        self.continuity = QTreeWidgetItem(self.ui.treeWidget, ["Continuity"])
        continuity_display = QLineEdit()
        continuity_display.setDisabled(True)
        self.ui.treeWidget.setItemWidget(self.continuity, 1, continuity_display)

    def generateUI(self, point_size):
        self.weights_list = QTreeWidgetItem(self.ui.treeWidget)
        self.weights_list.setText(0, "Weights")
        self.weights_list.setText(1, str(point_size))
        for i in range(point_size):
            weights = QTreeWidgetItem(self.weights_list)
            weights.setText(0, str(i + 1))
            weight_display = QDoubleSpinBox()
            weight_display.setSingleStep(0.1)
            weight_display.setRange(0.1, 1.0)
            self.ui.treeWidget.setItemWidget(weights, 1, weight_display)

    def updateUI(self, point_size):
        self.weights_list.setText(1, str(point_size))
        # self.poles_list.setText(1, str(point_size))
        for i in range(0, self.weights_list.childCount()):
            if i < point_size:
                self.weights_list.child(i).setHidden(False)
                # self.poles_list.child(i).setHidden(False)
            else:
                self.weights_list.child(i).setHidden(True)
                # self.poles_list.child(i).setHidden(True)

    def setModel(self, model):
        self._model: SceneGraphModel = model
        self._dataMapper.setModel(model)
        self._dataMapper.addMapping(self.ui.treeWidget.itemWidget(self.degree, 1), 2)
        self._dataMapper.addMapping(self.ui.treeWidget.itemWidget(self.rational, 1), 3)
        self._dataMapper.addMapping(self.ui.treeWidget.itemWidget(self.closed, 1), 4)
        self._dataMapper.addMapping(self.ui.treeWidget.itemWidget(self.continuity, 1), 5)
        for i in range(1, self.weights_list.childCount() + 1):
            weight = self.weights_list.child(i - 1)
            self._dataMapper.addMapping(self.ui.treeWidget.itemWidget(weight, 1), 5 + i)

    """INPUTS: QModelIndex"""

    def setSelection(self, current):
        parent: QModelIndex = current.parent()
        self._dataMapper.setRootIndex(parent)
        self._dataMapper.setCurrentModelIndex(current)
        # node information can be obtained
        node: BezierNode = self._model.getNode(current)
        if type(node) == BezierNode:
            object: Sketch_BezierCurve = node.getSketchObject()
            point_size = len(object.GetPoles())
            if self.pole_size != point_size:
                self.updateUI(point_size)
                self.poles_size = point_size


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
        if self.ui.uiXYPlane.isChecked():
            self.dir = gp_Dir(0.0, 0.0, 1.0)
            self._display.View_Top()
        if self.ui.uiXZPlane.isChecked():
            self.dir = gp_Dir(0.0, 1.0, 0.0)
            self._display.View_Front()
        if self.ui.uiYZPlane.isChecked():
            self.dir = gp_Dir(1.0, 0.0, 0.0)
            self._display.View_Right()
        self._plane = gp_Pln(gp_Pnt(0.0, 0.0, 0.0), self.dir)
        ax3 = gp_Ax3(self._plane.Location(), self._plane.Axis().Direction())
        self._display.Viewer.SetPrivilegedPlane(ax3)
        self.close()

    def plane(self):
        return self._plane
