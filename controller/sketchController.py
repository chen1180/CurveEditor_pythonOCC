from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon
from data.sketch.sketch import Sketch
from data.sketch.sketch_qtgui import Sketch_QTGUI
from data.sketch.sketch_type import *
from controller.editorController import Sketch_NewSketchEditor
from data.node import *
from data.model import SceneGraphModel
from OCC.Core.V3d import V3d_Viewer
from OCC.Core.gp import gp_Ax3


class SketchController(QObject):
    modelUpdated = pyqtSignal(object)

    def __init__(self, display, parent=None):
        super(SketchController, self).__init__(parent)
        self._display = display
        self.sketchUI = Sketch_QTGUI()
        self.sketch = Sketch(self._display, self.sketchUI)
        self.model: SceneGraphModel = None
        self.currentSketchNode = None
        self.sketch_list = []
        self.createActions()
        self.setActionEnabled(False)

    def createActions(self):
        self.action_createNewSketch = QAction(QIcon(""), "create a new sketch", self,
                                              statusTip="create a new sketch",
                                              triggered=self.createNewSketch)
        self.action_addPoint = QAction(QIcon(""), "add points", self,
                                       statusTip="add points on sketch",
                                       triggered=self.sketchPoint)
        self.action_addLine = QAction(QIcon(""), "add lines", self,
                                      statusTip="add a line",
                                      triggered=self.sketchLine)
        self.action_addBezierCurve = QAction(QIcon(""), "Add Bezier Curve", self,
                                             statusTip="Add a cubic Bezier curve",
                                             triggered=self.sketchBezier)
        self.action_addBSpline = QAction(QIcon(""), "Add BSpline Curve", self,
                                         statusTip="Add a B Spline curve",
                                         triggered=self.sketchBSpline)
        self.action_pointsToBSpline = QAction(QIcon(""), "Interpolate BSpline", self,
                                              statusTip="Interpolate points with BSpline",
                                              triggered=self.sketchPointsToBSpline)
        self.action_addArc = QAction(QIcon(""), "Add Arc", self,
                                     statusTip="Add an arc",
                                     triggered=self.sketchArc3P)
        self.action_addCircle = QAction(QIcon(""), "Add Circle", self,
                                        statusTip="Add a circle",
                                        triggered=self.sketchCircleCenterRadius)
        self.action_snapEnd = QAction(QIcon(""), "Snap End", self,
                                      statusTip="Snap to the end points",
                                      triggered=self.snapEnd)
        self.action_snapCenter = QAction(QIcon(""), "Snap Center", self,
                                         statusTip="Snap to the center of circle or arc",
                                         triggered=self.snapCenter)
        self.action_snapNearest = QAction(QIcon(""), "Snap Nearest", self,
                                          statusTip="Snap to the nearest points on the geometry",
                                          triggered=self.snapNearest)
        self.action_snapNothing = QAction(QIcon(""), "No Snap", self,
                                          statusTip="No Snap mode",
                                          triggered=self.snapNothing)

    def setActionEnabled(self, a0):
        self.action_addPoint.setEnabled(a0)
        self.action_addLine.setEnabled(a0)
        self.action_addBezierCurve.setEnabled(a0)
        self.action_addBSpline.setEnabled(a0)
        self.action_pointsToBSpline.setEnabled(a0)
        self.action_addArc.setEnabled(a0)
        self.action_addCircle.setEnabled(a0)
        self.action_snapEnd.setEnabled(a0)
        self.action_snapCenter.setEnabled(a0)
        self.action_snapNearest.setEnabled(a0)
        self.action_snapNothing.setEnabled(a0)

    def setModel(self, model):
        self.model = model

    def setRootNode(self, root):
        self._root: Node = root

    def snapEnd(self):
        self.sketch.SetSnap(Sketcher_SnapType.SnapEnd)

    def snapNearest(self):
        self.sketch.SetSnap(Sketcher_SnapType.SnapNearest)

    def snapCenter(self):
        self.sketch.SetSnap(Sketcher_SnapType.SnapCenter)

    def snapNothing(self):
        self.sketch.SetSnap(Sketcher_SnapType.SnapNothing)

    def createNewSketch(self):
        self.new_sketch = Sketch_NewSketchEditor(None, self._display)
        self.new_sketch.ui.uiOk.accepted.connect(self.createSketchNode)

    def createSketchNode(self):
        name = "Sketch "
        count = str(len(self.sketch_list))
        name += count
        if self.currentSketchNode is None:
            self.setActionEnabled(True)

        self.currentSketchNode = SketchNode(name)
        self.sketch_list.append(self.currentSketchNode)
        self.new_sketch.constructGrid()
        self.sketch.SetRootNode(self.currentSketchNode)
        self.modelUpdated.emit(self.currentSketchNode)
        assert isinstance(self._display.Viewer, V3d_Viewer)
        coordinate_system: gp_Ax3 = self._display.Viewer.PrivilegedPlane()
        # direction = coordinate_system.Direction()
        # print(direction.X(), direction.Y(), direction.Z())
        self.sketch.SetCoordinateSystem(coordinate_system)
        # coordinate_system: gp_Ax3 = self.sketch.GetCoordinateSystem()
        # direction = coordinate_system.Direction()
        # print(direction.X(), direction.Y(), direction.Z())

    def sketchPoint(self):
        self.sketch.ObjectAction(Sketch_ObjectTypeOfMethod.Point_Method)

    def sketchLine(self):
        self.sketch.ObjectAction(Sketch_ObjectTypeOfMethod.Line2P_Method)

    def sketchBezier(self):
        self.sketch.ObjectAction(Sketch_ObjectTypeOfMethod.BezierCurve_Method)

    def sketchArc3P(self):
        self.sketch.ObjectAction(Sketch_ObjectTypeOfMethod.Arc3P_Method)

    def sketchCircleCenterRadius(self):
        self.sketch.ObjectAction(Sketch_ObjectTypeOfMethod.CircleCenterRadius_Method)

    def sketchBSpline(self):
        self.sketch.ObjectAction(Sketch_ObjectTypeOfMethod.BSpline_Method)

    def sketchPointsToBSpline(self):
        self.sketch.ObjectAction(Sketch_ObjectTypeOfMethod.PointsToBSpline_Method)

    def OnMouseInputEvent(self, *kargs):
        self.sketch.OnMouseInputEvent(*kargs)
        self.model.layoutChanged.emit()

    def OnMouseMoveEvent(self, *kargs):
        self.sketch.OnMouseMoveEvent(*kargs)

    def OnCancel(self):
        self.sketch.OnCancel()

    def DeleteSelectedObject(self):
        self.sketch.DeleteSelectedObject()
