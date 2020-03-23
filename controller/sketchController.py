from OCC.Core.V3d import *
from PyQt5.QtCore import QObject, pyqtSignal, QModelIndex
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QStatusBar

from controller.editorController import Sketch_NewSketchEditor
from data.model import SceneGraphModel
from data.node import *
from data.sketch.gui.sketch_qtgui import Sketch_QTGUI
from data.sketch.sketch import Sketch
from data.sketch.sketch_type import *

class SketchController(QObject):
    sketchPlaneUpdated = pyqtSignal(object)

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

    def highlightCurrentNode(self, current: QModelIndex, old: QModelIndex):
        node: SketchObjectNode = current.internalPointer()
        if isinstance(node, SketchNode):
            self.selectSketchNode(node)
            self._display.Context.SetSelected(node.getSketchPlane().GetAIS_Object(),True)
        elif isinstance(node, SketchObjectNode):
            self._display.Context.SetSelected(node.getSketchObject().GetAIS_Object(), True)
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
        bspline_action = []
        self.action_addBSpline = QAction(QIcon(":/bspline_curve.png"), "BSplines", self,
                                         statusTip="Add a B Spline curve",
                                         triggered=self.sketchBSpline)
        bspline_action.append(self.action_addBSpline)
        self.action_pointsToBSpline = QAction(QIcon(":/spline.png"), "Interpolate", self,
                                              statusTip="Interpolate points with BSpline",
                                              triggered=self.sketchPointsToBSpline)
        bspline_action.append(self.action_pointsToBSpline)
        self.actions.append(bspline_action)
        nurbCircle_action=[]
        self.action_addNurbsCircle_Square = QAction(QIcon(":/nurbs.png"), "Nurbs Circle 1", self,
                                             statusTip="Add a 9 control points nurbs circle",
                                             triggered=self.sketchNurbCircleSquare)
        nurbCircle_action.append(self.action_addNurbsCircle_Square)
        self.action_addNurbsCircle_Triangle= QAction(QIcon(":/nurbs.png"), "Nurbs Circle 2", self,
                                                    statusTip="Add a 7 control points nurbs circle",
                                                    triggered=self.sketchNurbCircleTriangle)
        nurbCircle_action.append(self.action_addNurbsCircle_Triangle)
        self.actions.append(nurbCircle_action)

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
        self.action_snapToGrid = QAction(QIcon(""), "Snap to Grid", self,
                                         statusTip="Snap to the nearest point on the grid",
                                         triggered=self.snapGrid)
        snap_action.append(self.action_snapToGrid)

        self.action_snapEnd = QAction(QIcon(""), "Snap to EndPoint", self,
                                      statusTip="Snap to the end points of a curve",
                                      triggered=self.snapEnd)
        snap_action.append(self.action_snapEnd)

        self.action_snapCenter = QAction(QIcon(""), "Snap to Center", self,
                                         statusTip="Snap to the center of circle or arc",
                                         triggered=self.snapCenter)
        snap_action.append(self.action_snapCenter)
        self.action_snapNearest = QAction(QIcon(""), "Snap to Nearest", self,
                                          statusTip="Snap to the nearest point on a curve",
                                          triggered=self.snapNearest)
        snap_action.append(self.action_snapNearest)
        self.actions.append(snap_action)

    def setModel(self, model):
        self.model = model
        self.sketch.SetModel(self.model)

    def setRootNode(self, root):
        self.rootNode: Node = root

    def snapEnd(self):
        self.sketch.SnapToGridPoint = False
        self.sketch.SetSnap(Sketcher_SnapType.SnapEnd)

    def snapNearest(self):
        self.sketch.SnapToGridPoint = False
        self.sketch.SetSnap(Sketcher_SnapType.SnapNearest)

    def snapCenter(self):
        self.sketch.SnapToGridPoint = False
        self.sketch.SetSnap(Sketcher_SnapType.SnapCenter)

    def snapNothing(self):
        self.sketch.SnapToGridPoint = False
        self.sketch.SetSnap(Sketcher_SnapType.SnapNothing)

    def snapGrid(self):
        self.sketch.SnapToGridPoint = True

    def createNewSketch(self):
        self.new_sketch = Sketch_NewSketchEditor(None, self._display)
        self.new_sketch.ui.uiOk.accepted.connect(self.createSketchNode)

    def createSketchNode(self):
        name = "Sketch "
        count = str(self.rootNode.childCount())
        name += count
        self.currentSketchNode = SketchNode(name,self.rootNode)
        coordinate_system: gp_Ax3 = self.new_sketch.getCoordinate()
        sketch_plane = Sketch_Plane(self._display, coordinate_system)
        sketch_plane.Compute()
        sketch_plane.CreateDynamicGrid(self.new_sketch.ui.uiOffset.value())
        self.currentSketchNode.setSketchPlane(sketch_plane)
        self.sketchPlaneUpdated.emit(self.currentSketchNode)
        self.selectSketchNode(self.currentSketchNode)

    def selectSketchNode(self, node: SketchNode):
        assert isinstance(self._display.Viewer, V3d_Viewer)
        assert isinstance(self._display.View, V3d_View)
        self._display.Viewer.SetPrivilegedPlane(node.getSketchPlane().GetCoordinate())
        # self._display.Viewer.DisplayPrivilegedPlane(True, 1000)
        node.getSketchPlane().DisplayGrid()
        self.sketch.SetRootNode(node)
        self.sketch.SetCoordinateSystem(node.getSketchPlane().GetCoordinate())


    def sketchPoint(self):
        self.sketch.ObjectAction(Sketch_ObjectTypeOfMethod.Point_Method)

    def sketchLine(self):
        self.sketch.ObjectAction(Sketch_ObjectTypeOfMethod.Line2P_Method)

    def sketchBezier(self):
        self.sketch.ObjectAction(Sketch_ObjectTypeOfMethod.BezierCurve_Method)

    def sketchArc3P(self):
        self.sketch.ObjectAction(Sketch_ObjectTypeOfMethod.ArcCenter2P_Method)

    def sketchCircleCenterRadius(self):
        self.sketch.ObjectAction(Sketch_ObjectTypeOfMethod.CircleCenterRadius_Method)

    def sketchBSpline(self):
        self.sketch.ObjectAction(Sketch_ObjectTypeOfMethod.BSpline_Method)

    def sketchNurbCircleSquare(self):
        self.sketch.ObjectAction(Sketch_ObjectTypeOfMethod.NurbsCircleSquare_Method)

    def sketchNurbCircleTriangle(self):
        self.sketch.ObjectAction(Sketch_ObjectTypeOfMethod.NurbsCircleTriangle_Method)

    def sketchPointsToBSpline(self):
        self.sketch.ObjectAction(Sketch_ObjectTypeOfMethod.PointsToBSpline_Method)

    def OnMouseInputEvent(self, *kargs):
        if self.currentSketchNode:
            self.sketch.OnMouseInputEvent(*kargs)

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

    def HideSketchNodeChildren(self, node):
        index = 0
        while index < node.childCount():
            child = node.child(index)
            myCurObject: Sketch_Geometry = child.getSketchObject()
            myCurObject.RemoveDisplay()
            index += 1

    def DeleteSelectedObject(self):
        if self.currentSketchNode:
            root: Node = self.currentSketchNode.parent()
            for i, planeNode in enumerate(root.children()):
                index = 0
                # planeNode.getSketchPlane().RemoveDisplay()
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
                # self.model.removeRow(i,QModelIndex())
            # inform model to update
            self.model.layoutChanged.emit()
