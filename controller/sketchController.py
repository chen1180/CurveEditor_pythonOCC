from OCC.Core.Aspect import Aspect_GDM_Lines, Aspect_GT_Rectangular
from OCC.Core.Graphic3d import *
from OCC.Core.V3d import *
from OCC.Core.V3d import V3d_Viewer
from OCC.Core.gp import gp_Ax3
from PyQt5.QtCore import QModelIndex, QObject, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QStatusBar

from controller.editorController import Sketch_NewSketchEditor
from data.model import SceneGraphModel
from data.node import *
from data.sketch.gui.sketch_qtgui import Sketch_QTGUI
from data.sketch.sketch import Sketch
from data.sketch.sketch_type import *


class SketchController(QObject):
    modelUpdated = pyqtSignal(object)

    def __init__(self, display, parent=None):
        super(SketchController, self).__init__(parent)
        self._display = display
        self.actions = []
        self.statusBar: QStatusBar = parent.statusBar()

        self.sketchUI = Sketch_QTGUI()
        self.sketch = Sketch(self._display, self.sketchUI)
        self.model: SceneGraphModel = None
        self.currentSketchNode: SketchObjectNode = None
        self.createActions()

        self.setActionEnabled(False)

    def highlightCurrentNode(self, current: QModelIndex, old: QModelIndex):
        node: SketchObjectNode = current.internalPointer()
        if isinstance(node, SketchNode):
            self.selectSketchNode(node)
        elif isinstance(node, SketchObjectNode):
            self._display.Context.SetSelected(node.sketchObject.myAIS_InteractiveObject, True)

    def setStatusBar(self, theStatusBar):
        self.statusBar: QStatusBar = theStatusBar
        self.statusBar.showMessage("status bar setted")

    def createActions(self):
        self.action_createNewSketch = QAction(QIcon(":/newPlane.png"), "New sketch", self,
                                              statusTip="create a new sketch",
                                              triggered=self.createNewSketch)
        self.actions.append(self.action_createNewSketch)
        self.action_addPoint = QAction(QIcon(":/point.png"), "Point", self,
                                       statusTip="add points on sketch",
                                       triggered=self.sketchPoint)
        self.actions.append(self.action_addPoint)
        self.action_addLine = QAction(QIcon(":/inputLine.png"), "Line", self,
                                      statusTip="add a line",
                                      triggered=self.sketchLine)
        self.actions.append(self.action_addLine)
        self.action_addBezierCurve = QAction(QIcon(":/bezier.png"), "Bezier Curve", self,
                                             statusTip="Add a cubic Bezier curve",
                                             triggered=self.sketchBezier)
        self.actions.append(self.action_addBezierCurve)
        self.action_addBSpline = QAction(QIcon(":/spline.png"), "BSplines", self,
                                         statusTip="Add a B Spline curve",
                                         triggered=self.sketchBSpline)
        self.actions.append(self.action_addBSpline)
        self.action_addNurbsCircle = QAction(QIcon(":/nurbs.png"), "Nurbs Circle", self,
                                             statusTip="Add a 9 control points nurbs circle",
                                             triggered=self.sketchNurbCircle)
        self.actions.append(self.action_addNurbsCircle)
        self.action_pointsToBSpline = QAction(QIcon(""), "Interpolate BSpline", self,
                                              statusTip="Interpolate points with BSpline",
                                              triggered=self.sketchPointsToBSpline)
        self.actions.append(self.action_pointsToBSpline)
        self.action_addArc = QAction(QIcon(""), "Add Arc", self,
                                     statusTip="Add an arc",
                                     triggered=self.sketchArc3P)
        self.actions.append(self.action_addArc)
        self.action_addCircle = QAction(QIcon(""), "Add Circle", self,
                                        statusTip="Add a circle",
                                        triggered=self.sketchCircleCenterRadius)
        self.actions.append(self.action_addCircle)
        self.action_snapEnd = QAction(QIcon(""), "Snap End", self,
                                      statusTip="Snap to the end points",
                                      triggered=self.snapEnd)
        self.actions.append(self.action_snapEnd)
        self.action_snapCenter = QAction(QIcon(""), "Snap Center", self,
                                         statusTip="Snap to the center of circle or arc",
                                         triggered=self.snapCenter)
        self.actions.append(self.action_snapCenter)
        self.action_snapNearest = QAction(QIcon(""), "Snap Nearest", self,
                                          statusTip="Snap to the nearest points on the geometry",
                                          triggered=self.snapNearest)
        self.actions.append(self.action_snapNearest)
        self.action_snapNothing = QAction(QIcon(""), "No Snap", self,
                                          statusTip="No Snap mode",
                                          triggered=self.snapNothing)
        self.actions.append(self.action_snapNothing)

    def setActionEnabled(self, a0):
        for action in self.actions:
            action.setEnabled(a0)

    def setModel(self, model):
        self.model = model

    def setRootNode(self, root):
        self.rootNode: Node = root

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
        count = str(self.rootNode.childCount())
        name += count
        if self.currentSketchNode is None:
            self.setActionEnabled(True)
        self.currentSketchNode = SketchNode(name)
        coordinate_system: gp_Ax3 = self._display.Viewer.PrivilegedPlane()
        # Display normal axis of the plane
        # print(coordinate_system.Axis())
        # normal_axis=coordinate_system.Axis()
        # normal_geom_axis=Geom_Line(normal_axis)
        # ais_axis=AIS_Line(normal_geom_axis)
        # self._display.Context.Display(ais_axis,True)
        self.createDynamicGrid()
        self.currentSketchNode.setSketchPlane(coordinate_system)
        self.modelUpdated.emit(self.currentSketchNode)
        self.selectSketchNode(self.currentSketchNode)

    def createDynamicGrid(self):
        # camera attribute
        self.view: V3d_View = self._display.View
        # scale factor by mosue scroller
        self.camera: Graphic3d_Camera = self.view.Camera()
        canvas_size = max(self.view.Size())
        grid_interval = self.camera.Distance() // self.view.Scale() / 5
        self.displayGrid(0.0, 0.0, grid_interval, grid_interval, 0.0, canvas_size,
                         canvas_size, self.new_sketch.ui.uiOffset.value())

    def displayGrid(self, xOrigin, yOrigin, xStep, yStep, rotation, xSize, ySize, offset):
        self._display.Viewer.SetRectangularGridValues(xOrigin, yOrigin, xStep, yStep, rotation)
        self._display.Viewer.SetRectangularGridGraphicValues(xSize, ySize, offset)
        self._display.Viewer.ActivateGrid(Aspect_GT_Rectangular, Aspect_GDM_Lines)

    def selectSketchNode(self, node: SketchNode):
        assert isinstance(self._display.Viewer, V3d_Viewer)
        assert isinstance(self._display.View, V3d_View)
        self._display.Viewer.SetPrivilegedPlane(node.sketch_plane)
        self._display.Viewer.DisplayPrivilegedPlane(True, 1000)
        self.sketch.SetRootNode(node)
        self.sketch.SetCoordinateSystem(node.sketch_plane)

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

    def sketchNurbCircle(self):
        self.sketch.ObjectAction(Sketch_ObjectTypeOfMethod.NurbsCircle_Method)

    def sketchPointsToBSpline(self):
        self.sketch.ObjectAction(Sketch_ObjectTypeOfMethod.PointsToBSpline_Method)

    def OnMouseInputEvent(self, *kargs):
        self.sketch.OnMouseInputEvent(*kargs)
        self.model.layoutChanged.emit()

    def OnMouseMoveEvent(self, *kargs):
        self.sketch.OnMouseMoveEvent(*kargs)

    def OnMouseReleaseEvent(self, *kargs):
        self.sketch.OnMouseReleaseEvent(*kargs)

    def editGeometry(self):
        if self.currentSketchNode:
            self.sketch.ViewProperties()

    def OnCancel(self):
        self.sketch.OnCancel()

    def DeleteSelectedObject(self):
        self.sketch.DeleteSelectedObject()
