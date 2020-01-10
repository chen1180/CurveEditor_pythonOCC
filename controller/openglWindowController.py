from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from view.openglWindow import GLWidget
from controller import toolController
import logging
from data.sketch.sketch import *
from data.sketch.sketch_qtgui import Sketch_QTGUI
from data.sketch.sketch_type import *
from data.design.part import *

HAVE_PYQT_SIGNAL = hasattr(QtCore, 'pyqtSignal')
from OCC.Core.Geom import Geom_Axis2Placement, Geom_Plane, Geom_Line, Geom_CartesianPoint
from OCC.Core.Prs3d import *
from OCC.Core.Graphic3d import *
from controller.editorController import Sketch_NewSketchEditor
from data.node import *
from OCC.Core.V3d import V3d_Viewer

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger(__name__)


class OpenGLEditor(GLWidget):
    modelUpdated = QtCore.pyqtSignal(object)
    MODE_SKETCH = 0
    MODE_DESIGN = 1
    MODE_VIEW = 2

    def __init__(self, parent=None):
        super(OpenGLEditor, self).__init__(parent)
        try:
            self.InitDriver()
        except Exception as e:
            print(e)

        self.parent = parent
        # self._display.set_bg_gradient_color([206, 215, 222],[128, 128, 128])
        # Acitivate selection automaticlly
        self._display.Context.SetAutoActivateSelection(False)
        # self.sketchManager = toolController.SketchController(self._display)
        self.viewManager = toolController.ViewController(self._display)
        self.sketchUI = Sketch_QTGUI()
        self.sketch = Sketch(self._display, self.sketchUI)
        self.sketch.SetSnap(Sketcher_SnapType.SnapNearest)
        self.part = Part(self._display)

        # self.sketchManager.interactive.prepareContext_find_edge()
        # self._display.Context.RemoveFilters()
        # self._display.Context.Deactivate()
        # self._display.Context.Activate(0)
        self._state = self.MODE_VIEW

        self._mousePress_callback = []
        self._mouseMove_callback = []
        self._mouseRelease_callback = []

        # callback functions
        # self._display.register_select_callback(self.sketchManager.recognize_clicked)

        # self.register_mousePress_callback(self.sketchManager.mousePress)
        # self.register_mouseMove_callback(self.sketchManager.mouseMove)
        # self.register_mouseRelease_callback(self.sketchManager.mouseRelease)

        self.register_mousePress_callback(self.viewManager.selectAIS_Shape)
        self.register_mousePress_callback(self.viewManager.startTransform)

        # signals and slots
        # self.sketchManager.modelUpdate.connect(self.addNewItem)

        # self._key_map.setdefault(QtCore.Qt.Key_Escape, []).append(self.sketchManager.ExitDrawingMode)
        self._key_map.setdefault(QtCore.Qt.Key_Escape, []).append(self.viewManager.setDeactive)
        self._key_map.setdefault(QtCore.Qt.Key_Escape, []).append(self.sketch.OnCancel)
        self._key_map.setdefault(QtCore.Qt.Key_Delete, []).append(self.sketch.DeleteSelectedObject)
        # self._display.Test()
        self._cubeManip = AIS_ViewCube()
        self._cubeManip.SetTransformPersistence(Graphic3d_TMF_TriedronPers, gp_Pnt(1, 1, 100))
        # self._cubeManip.SetInfiniteState(True)
        self._display.Context.Display(self._cubeManip, True)
        self.setReferenceAxe()
        assert isinstance(self._display.Context, AIS_InteractiveContext)
        # self._display.View.SetBgGradientColors(Quantity_Color(Quantity_NOC_SKYBLUE), Quantity_Color(Quantity_NOC_GRAY), 2, True)

    def setReferenceAxe(self):
        geom_axe = Geom_Axis2Placement(gp_XOY())
        self._refrenceAxies = AIS_Trihedron(geom_axe)
        self._refrenceAxies.SetSelectionPriority(Prs3d_DP_XOYAxis, 3)
        self._display.Context.Display(self._refrenceAxies, True)
        origin = Geom_CartesianPoint(gp_Pnt(0, 0, 0))
        # ais_origin=AIS_Point(origin)
        # ais_x=AIS_Line(origin,Geom_CartesianPoint(gp_Pnt(50,0,0)))
        # ais_x.SetColor(Quantity_Color(1.0,0,0,Quantity_TOC_RGB))
        # ais_y = AIS_Line(origin,Geom_CartesianPoint(gp_Pnt(0,50,0)))
        # ais_y.SetColor(Quantity_Color(0, 1, 0, Quantity_TOC_RGB))
        # ais_z = AIS_Line(origin,Geom_CartesianPoint(gp_Pnt(0,0,50)))
        # ais_z.SetColor(Quantity_Color(0, 0, 1.0, Quantity_TOC_RGB))
        # self._display.Context.Display(ais_origin, True)
        # self._display.Context.Display(ais_x, True)
        # self._display.Context.Display(ais_y, True)
        # self._display.Context.Display(ais_z, True)

    def sketchPoint(self):
        self.sketch.ObjectAction(Sketch_ObjectTypeOfMethod.Point_Method)
        self.part.SetData(self.sketch.myData)

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

    def partRevolveSurface(self):
        self.part.ObjectAction(Part_ObjectTypeOfMethod.RevolvedSurface_Method)

    def partExtrudedSurface(self):
        self.part.ObjectAction(Part_ObjectTypeOfMethod.ExtrudedSurface_Method)

    def fitSelection(self):
        self._display.Context.FitSelected(self._display.View, 0.0, True)

    def createNewSketch(self):
        self.new_sketch = Sketch_NewSketchEditor(None, self._display)
        self.new_sketch.ui.uiOk.accepted.connect(self.createSketchNode)

    def createSketchNode(self):
        self.new_sketch.constructGrid()
        self._sketch = SketchNode("Sketch")
        self.modelUpdated.emit(self._sketch)
        assert isinstance(self._display.Viewer, V3d_Viewer)
        coordinate_system: gp_Ax3 = self._display.Viewer.PrivilegedPlane()
        direction = coordinate_system.Direction()
        # print(direction.X(), direction.Y(), direction.Z())
        self.sketch.SetCoordinateSystem(coordinate_system)
        # coordinate_system: gp_Ax3 = self.sketch.GetCoordinateSystem()
        # direction = coordinate_system.Direction()
        # print(direction.X(), direction.Y(), direction.Z())

    def setScene(self, scene):
        self._sceneGraph = scene

    def state(self):
        return self._state

    def setState(self, state):
        self._state = state
        self.update()

    def processActions(self):
        if self._state == self.MODE_VIEW:
            if self._display.Viewer.IsActive() == True:
                self._display.Viewer.DeactivateGrid()
        elif self._state == self.MODE_DESIGN:
            pass
        elif self._state == self.MODE_SKETCH:
            # self.sketchManager.EnterDrawingMode()
            pass
        self._display.Repaint()

    def paintEvent(self, event):
        super(OpenGLEditor, self).paintEvent(event)
        if self._inited:
            self._display.Context.UpdateCurrentViewer()
            self.sketch.RedrawAll()
            self.processActions()
            self.update()

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        code = event.key()
        if code in self._key_map:
            functions = self._key_map[code]
            # print(functions)
            if type(functions) == list:
                for func in functions:
                    func()
            else:
                functions()
        else:
            log.info('key: code %i not mapped to any function' % code)

    def wheelEvent(self, event):
        try:  # PyQt4/PySide
            delta = event.delta()
        except:  # PyQt5
            delta = event.angleDelta().y()
        if delta > 0:
            zoom_factor = 2.
        else:
            zoom_factor = 0.5
        self._display.ZoomFactor(zoom_factor)

    def mousePressEvent(self, event):
        self.setFocus()
        pt = event.pos()
        buttons = int(event.buttons())
        modifiers = event.modifiers()
        self.sketch.ViewProperties()
        if buttons == QtCore.Qt.MiddleButton:
            if modifiers != QtCore.Qt.ShiftModifier:
                self.dragStartPosX = pt.x()
                self.dragStartPosY = pt.y()
                self._display.StartRotation(self.dragStartPosX, self.dragStartPosY)
            else:
                self.dragStartPosX = pt.x()
                self.dragStartPosY = pt.y()
        if self._state == self.MODE_VIEW:
            pass
        elif self._state == self.MODE_DESIGN:
            pass
        elif self._state == self.MODE_SKETCH:
            pass
        for callback in self._mousePress_callback:
            callback(pt.x(), pt.y())

        self.sketch.OnMouseInputEvent(pt.x(), pt.y())
        self.part.OnMouseInputEvent(pt.x(), pt.y())

    def mouseReleaseEvent(self, event):
        pt = event.pos()
        modifiers = event.modifiers()

        if event.button() == QtCore.Qt.LeftButton:
            if self._select_area:
                if type(self._drawbox) == list:
                    [Xmin, Ymin, dx, dy] = self._drawbox
                    self._display.SelectArea(Xmin, Ymin, Xmin + dx, Ymin + dy)
                    self._select_area = False
                else:
                    self._display.Select(pt.x(), pt.y())
            else:
                # multiple select if shift is pressed
                if modifiers == QtCore.Qt.ShiftModifier:
                    self._display.ShiftSelect(pt.x(), pt.y())
                else:
                    # single select otherwise
                    self._display.Select(pt.x(), pt.y())

                    if (self._display.selected_shapes is not None) and HAVE_PYQT_SIGNAL:
                        self.sig_topods_selected.emit(self._display.selected_shapes)
            for callback in self._mouseRelease_callback:
                callback(pt.x(), pt.y())

        # elif event.button() == QtCore.Qt.RightButton:
        #     if self._zoom_area:
        #         [Xmin, Ymin, dx, dy] = self._drawbox
        #         self._display.ZoomArea(Xmin, Ymin, Xmin + dx, Ymin + dy)
        #         self._zoom_area = False

        self.cursor = "arrow"

    def DrawBox(self, event):
        tolerance = 2
        pt = event.pos()
        dx = pt.x() - self.dragStartPosX
        dy = pt.y() - self.dragStartPosY
        if abs(dx) <= tolerance and abs(dy) <= tolerance:
            return
        self._drawbox = [self.dragStartPosX, self.dragStartPosY, dx, dy]

    def mouseMoveEvent(self, evt):
        pt = evt.pos()
        buttons = int(evt.buttons())
        modifiers = evt.modifiers()
        self.sketch.OnMouseMoveEvent(pt.x(), pt.y())
        self.part.OnMouseMoveEvent(pt.x(), pt.y())
        for callback in self._mouseMove_callback:
            callback(pt.x(), pt.y())

        if buttons == QtCore.Qt.MiddleButton:
            if modifiers != QtCore.Qt.ShiftModifier:
                # ROTATE
                self.cursor = "rotate"
                self._display.Rotation(pt.x(), pt.y())
                self._drawbox = False
                if self._state == self.MODE_VIEW:
                    pass
                elif self._state == self.MODE_DESIGN:
                    pass
                elif self._state == self.MODE_SKETCH:
                    pass
                self.viewManager.transform(pt.x(), pt.y())
            # PAN
            elif modifiers == QtCore.Qt.ShiftModifier:
                dx = pt.x() - self.dragStartPosX
                dy = pt.y() - self.dragStartPosY
                self.dragStartPosX = pt.x()
                self.dragStartPosY = pt.y()
                self.cursor = "pan"
                self._display.Pan(dx, -dy)
                self._drawbox = False
        # # DYNAMIC ZOOM
        # elif (buttons == QtCore.Qt.RightButton and
        #       not modifiers == QtCore.Qt.ShiftModifier):
        #     self.cursor = "zoom"
        #     self._display.Repaint()
        #     self._display.DynamicZoom(abs(self.dragStartPosX),
        #                               abs(self.dragStartPosY), abs(pt.x()),
        #                               abs(pt.y()))
        #     self.dragStartPosX = pt.x()
        #     self.dragStartPosY = pt.y()
        #     self._drawbox = False

        # DRAW BOX
        # ZOOM WINDOW
        elif (buttons == QtCore.Qt.RightButton and
              modifiers == QtCore.Qt.ShiftModifier):
            self._zoom_area = True
            self.cursor = "zoom-area"
            self.DrawBox(evt)
            self.update()
        # SELECT AREA
        elif (buttons == QtCore.Qt.LeftButton and
              modifiers == QtCore.Qt.ShiftModifier):
            self._select_area = True
            self.DrawBox(evt)
            self.update()
        else:
            self._drawbox = False
            self._display.MoveTo(pt.x(), pt.y())
            self.cursor = "arrow"

    def register_mousePress_callback(self, callback):
        if not callable(callback):
            raise AssertionError("You must provide a callable to register the callback")
        else:
            self._mousePress_callback.append(callback)

    def register_mouseMove_callback(self, callback):
        if not callable(callback):
            raise AssertionError("You must provide a callable to register the callback")
        else:
            self._mouseMove_callback.append(callback)

    def register_mouseRelease_callback(self, callback):
        if not callable(callback):
            raise AssertionError("You must provide a callable to register the callback")
        else:
            self._mouseRelease_callback.append(callback)


# -----------------------------Debugging-----------------------------------#
if __name__ == '__main__':
    sys._excepthook = sys.excepthook


    def my_exception_hook(exctype, value, traceback):
        # Print the error and traceback
        print(exctype, value, traceback)
        # Call the normal Exception hook after
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)


    sys.excepthook = my_exception_hook
    application = QtWidgets.QApplication([])
    window = OpenGLEditor()  # Opengl window creation
    window.show()
    application.exec_()
