from PyQt5.QtCore import *
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
        self.model:QSortFilterProxyModel = None
        self._currentSketchNode = None

    def setModel(self, model):
        self.model = model

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
        self.new_sketch.constructGrid()
        self._currentSketchNode = SketchNode("Sketch")
        self.sketch.SetRootNode(self._currentSketchNode)
        self.modelUpdated.emit(self._currentSketchNode)
        assert isinstance(self._display.Viewer, V3d_Viewer)
        coordinate_system: gp_Ax3 = self._display.Viewer.PrivilegedPlane()
        direction = coordinate_system.Direction()
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
        print(self.sketch.myNode)
        self.model.layoutChanged.emit()

    def OnMouseMoveEvent(self, *kargs):
        self.sketch.OnMouseMoveEvent(*kargs)

    def OnCancel(self):
        self.sketch.OnCancel()

    def DeleteSelectedObject(self):
        self.sketch.DeleteSelectedObject()

    def setRootNode(self, root):
        self._root = root
