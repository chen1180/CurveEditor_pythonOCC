from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
from view import lightProperty, nodeProperty, property, transformProperty, cameraProperty, curveProperty, \
    newSketchProperty, lineProperty
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
        self.addEditor(self._nodeEditor, "Node")
        self.addEditor(self._pointEditor, "Point")
        self.addEditor(self._lineEditor, "Line")
        self.addEditor(self._bezierCurveEditor, "Bezier curve")

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
        # self.poles_list = QTreeWidgetItem(self.ui.treeWidget)
        # self.poles_list.setText(0, "Points")
        # self.poles_list.setText(1, str(point_size))
        # for i in range(point_size):
        #     pole = QTreeWidgetItem(self.poles_list)
        #     pole.setText(0, "Point" + str(i + 1))
        #     pole_display = QLineEdit()
        #     pole_display.setDisabled(True)
        #     self.ui.treeWidget.setItemWidget(pole, 1, pole_display)
        #     coorinate_x_item = QTreeWidgetItem(pole)
        #     coorinate_x_item.setText(0, "x")
        #     coorinate_y_item = QTreeWidgetItem(pole)
        #     coorinate_y_item.setText(0, "y")
        #     x_spinbox = QDoubleSpinBox()
        #     x_spinbox.setRange(-10000, 10000)
        #     y_spinbox = QDoubleSpinBox()
        #     y_spinbox.setRange(-10000, 10000)
        #     self.ui.treeWidget.setItemWidget(coorinate_x_item, 1, x_spinbox)
        #     self.ui.treeWidget.setItemWidget(coorinate_y_item, 1, y_spinbox)

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
        # count = 5 + self.weights_list.childCount()
        # for i in range(1, self.poles_list.childCount() + 1, 2):
        #     poles = self.poles_list.child(i - 1)
        #     self._dataMapper.addMapping(self.ui.treeWidget.itemWidget(poles.child(0), 1), count + i)
        #     self._dataMapper.addMapping(self.ui.treeWidget.itemWidget(poles.child(1), 1), count + i + 1)
        #     print(count + i, count + i + 1)

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


from OCC.Core.gp import gp_Pnt, gp_Pln, gp_Dir, gp_Ax3, gp
from OCC.Core.Aspect import Aspect_GDM_Lines, Aspect_GT_Rectangular
from OCC.Core.V3d import V3d_Viewer


class Sketch_NewSketchEditor(QWidget):
    def __init__(self, parent=None, display=None):
        super(Sketch_NewSketchEditor, self).__init__(parent)
        self.ui = newSketchProperty.Ui_newSketchEditor()
        self.ui.setupUi(self)
        self._display = display
        self.ui.uiOk.accepted.connect(self.constructGrid)
        self.ui.uiOk.rejected.connect(self.close)
        self.setWindowModality(Qt.ApplicationModal)
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
