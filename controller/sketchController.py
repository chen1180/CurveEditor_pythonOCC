from OCC.Core.Aspect import *
from OCC.Core.Graphic3d import *
from OCC.Core.V3d import *
from OCC.Core.V3d import V3d_Viewer
from PyQt5.QtCore import QObject, pyqtSignal, QModelIndex
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QStatusBar

from controller.editorController import Sketch_NewSketchEditor
from data.model import SceneGraphModel
from data.node import *
from data.sketch.gui.sketch_qtgui import Sketch_QTGUI
from data.sketch.sketch import Sketch
from data.sketch.sketch_type import *
from OCC.Core.Quantity import *


class SketchController(QObject):
    sketchPlaneUpdated = pyqtSignal(object)
    sketchObjectUpdated = pyqtSignal(object)

    def __init__(self, display, parent=None):
        super(SketchController, self).__init__(parent)
        self._display = display
        self.actions = []
        self.statusBar: QStatusBar = parent.statusBar()

        self.sketchUI = Sketch_QTGUI()
        self.sketch = Sketch(self._display, self.sketchUI)
        self.model: SceneGraphModel = None
        self.currentSketchNode: SketchObjectNode = None
        self.currentSketchIndex = None
        self.createActions()

    def highlightCurrentNode(self, current: QModelIndex, old: QModelIndex):
        node: SketchObjectNode = current.internalPointer()
        if isinstance(node, SketchNode):
            self.selectSketchNode(node)
        elif isinstance(node, SketchObjectNode):
            self._display.Context.SetSelected(node.sketchObject.myAIS_InteractiveObject, True)
        # self._display.View.SetFront()
        self._display.Context.FitSelected(self._display.View)

    def setStatusBar(self, theStatusBar):
        self.statusBar: QStatusBar = theStatusBar
        self.statusBar.showMessage("status bar setup")

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
        self.action_addBezierCurve = QAction(QIcon(":/bezier_curve.png"), "Bezier Curve", self,
                                             statusTip="Add a cubic Bezier curve",
                                             triggered=self.sketchBezier)
        self.actions.append(self.action_addBezierCurve)
        self.action_addBSpline = QAction(QIcon(":/bspline_curve.png"), "BSplines", self,
                                         statusTip="Add a B Spline curve",
                                         triggered=self.sketchBSpline)
        self.actions.append(self.action_addBSpline)
        self.action_addNurbsCircle = QAction(QIcon(":/nurbs.png"), "Nurbs Circle", self,
                                             statusTip="Add a 9 control points nurbs circle",
                                             triggered=self.sketchNurbCircle)
        self.actions.append(self.action_addNurbsCircle)
        self.action_pointsToBSpline = QAction(QIcon(":/spline.png"), "Interpolate", self,
                                              statusTip="Interpolate points with BSpline",
                                              triggered=self.sketchPointsToBSpline)
        self.actions.append(self.action_pointsToBSpline)
        self.action_addArc = QAction(QIcon(":/arc.png"), "Add Arc", self,
                                     statusTip="Add an arc",
                                     triggered=self.sketchArc3P)
        self.actions.append(self.action_addArc)
        # for test
        # self.action_addCircle = QAction(QIcon(""), "Add Circle", self,
        #                                 statusTip="Add a circle",
        #                                 triggered=self.sketchCircleCenterRadius)
        # self.actions.append(self.action_addCircle)
        snap_action = []

        self.action_snapNothing = QAction(QIcon(""), "No Snap", self,
                                          statusTip="No Snap mode",
                                          triggered=self.snapNothing)
        snap_action.append(self.action_snapNothing)

        self.action_snapEnd = QAction(QIcon(""), "Snap to Point", self,
                                      statusTip="Snap to the end points",
                                      triggered=self.snapEnd)
        snap_action.append(self.action_snapEnd)

        self.action_snapCenter = QAction(QIcon(""), "Snap Center", self,
                                         statusTip="Snap to the center of circle or arc",
                                         triggered=self.snapCenter)
        snap_action.append(self.action_snapCenter)
        self.action_snapNearest = QAction(QIcon(""), "Snap Nearest", self,
                                          statusTip="Snap to the nearest points on the geometry",
                                          triggered=self.snapNearest)
        snap_action.append(self.action_snapNearest)
        self.actions.append(snap_action)

    def setModel(self, model):
        self.model = model
        self.sketch.SetModel(self.model)

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
        name = "Plane "
        count = str(self.rootNode.childCount())
        name += count
        self.currentSketchNode = SketchNode(name)
        coordinate_system: gp_Ax3 = self.new_sketch.getCoordinate()
        pnt = coordinate_system.Location()
        print(pnt.X(), pnt.Y(), pnt.Z())
        # Display normal axis of the plane
        # print(coordinate_system.Axis())
        # normal_axis=coordinate_system.Axis()
        # normal_geom_axis=Geom_Line(normal_axis)
        # ais_axis=AIS_Line(normal_geom_axis)
        # self._display.Context.Display(ais_axis,True)
        sketch_plane = Sketch_Plane(self._display.Context, coordinate_system)
        sketch_plane.Compute()
        self.createDynamicGrid()
        self.currentSketchNode.setSketchPlane(sketch_plane)
        self.sketchPlaneUpdated.emit(self.currentSketchNode)

        self.selectSketchNode(self.currentSketchNode)

    def createDynamicGrid(self):
        # camera attribute
        self.view: V3d_View = self._display.View
        # scale factor by mosue scroller
        self.camera: Graphic3d_Camera = self.view.Camera()
        canvas_size = max(self.view.Size())
        grid_interval = self.camera.Distance() // self.view.Scale() / 5
        self._display.Viewer.ActivateGrid(Aspect_GT_Rectangular, Aspect_GDM_Lines)
        self._display.Viewer.SetRectangularGridGraphicValues(canvas_size, canvas_size,
                                                             self.new_sketch.ui.uiOffset.value())
        self._display.Viewer.SetRectangularGridValues(0.0, 0.0, grid_interval, grid_interval, 0.0)

    def selectSketchNode(self, node: SketchNode):
        assert isinstance(self._display.Viewer, V3d_Viewer)
        assert isinstance(self._display.View, V3d_View)
        self._display.Viewer.SetPrivilegedPlane(node.getSketchPlane().GetCoordinate())
        # self._display.Viewer.DisplayPrivilegedPlane(True, 1000)
        self.sketch.SetRootNode(node)
        self.sketch.SetCoordinateSystem(node.getSketchPlane().GetCoordinate())

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
        if self.currentSketchNode:
            self.sketch.OnMouseInputEvent(*kargs)
        # self.model.layoutChanged.emit()
        # self.sketchObjectUpdated.emit(self.currentSketchNode)

    def OnMouseMoveEvent(self, *kargs):
        if self.currentSketchNode:
            self.sketch.OnMouseMoveEvent(*kargs)

    def OnMouseReleaseEvent(self, *kargs):
        if self.currentSketchNode:
            self.sketch.OnMouseReleaseEvent(*kargs)

    def editGeometry(self):
        if self.currentSketchNode:
            self.sketch.ViewProperties()

    def OnCancel(self):
        self.sketch.OnCancel()

    def DeleteSelectedObject(self):
        root: Node = self.currentSketchNode.parent()
        for i, planeNode in enumerate(root.children()):
            index = 0
            while index < planeNode.childCount():
                child = planeNode.child(index)
                myCurObject: Sketch_Geometry = child.getSketchObject()
                if self._display.Context.IsSelected(myCurObject.GetAIS_Object()):
                    myCurObject.RemoveDisplay()
                    myCurObject.RemoveLabel()
                    # get parent sketch node
                    planeIndex = self.model.index(i, 0, QModelIndex())
                    self.model.removeRow(index, planeIndex)
                else:
                    index += 1
        # inform model to update
        self.model.layoutChanged.emit()
