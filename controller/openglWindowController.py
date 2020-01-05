from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from view.openglWindow import GLWidget
from controller import toolController
import logging
from data.sketch.sketch import *
from data.sketch.sketch_gui import *
from data.sketch.sketch_type import *
from OCC.Core.gp import gp_Pnt2d
HAVE_PYQT_SIGNAL = hasattr(QtCore, 'pyqtSignal')

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger(__name__)


class OpenGLEditor(GLWidget):
    modelUpdated = QtCore.pyqtSignal(object)
    MODE_SKETCH = 0
    MODE_DESIGN = 1
    MODE_VIEW = 2

    def __init__(self, parent=None):
        super(OpenGLEditor, self).__init__(parent)
        print(self._display._window_handle)
        self._display.Context.SetAutoActivateSelection(False)
        self.sketchManager = toolController.SketchController(self._display)
        self.viewManager = toolController.ViewController(self._display)
        self.sketchUI = Sketch_GUI()
        self.sketch=Sketch(self._display,self.sketchUI)

        self._state = self.MODE_VIEW

        self._mousePress_callback = []
        self._mouseMove_callback = []
        self._mouseRelease_callback = []

        # callback functions
        self._display.register_select_callback(self.sketchManager.recognize_clicked)

        self.register_mousePress_callback(self.sketchManager.mousePress)
        self.register_mouseMove_callback(self.sketchManager.mouseMove)
        self.register_mouseRelease_callback(self.sketchManager.mouseRelease)


        self.register_mousePress_callback(self.viewManager.selectAIS_Shape)
        self.register_mousePress_callback(self.viewManager.startTransform)

        #signals and slots
        self.sketchManager.modelUpdate.connect(self.addNewItem)

        self._key_map.setdefault(QtCore.Qt.Key_Escape,[]).append(self.sketchManager.ExitDrawingMode)
        # self._key_map.setdefault(QtCore.Qt.Key_Escape, []).append(self.viewManager.setDeactive)
        self._key_map.setdefault(QtCore.Qt.Key_Escape, []).append(self.sketch.OnCancel)
        # self._display.Test()
    def sketchPoint(self):
        self.sketch.ObjectAction(Sketch_ObjectTypeOfMethod.Point_Method)
    def sketchLine(self):
        self.sketch.ObjectAction(Sketch_ObjectTypeOfMethod.Line2P_Method)
    def sketchBezier(self):
        self.sketch.ObjectAction(Sketch_ObjectTypeOfMethod.BezierCurve_Method)
    def sketchArc3P(self):
        self.sketch.ObjectAction(Sketch_ObjectTypeOfMethod.Arc3P_Method)
    def addNewItem(self, item):
        self.modelUpdated.emit(item)

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
            self.sketchManager.EnterDrawingMode()
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
            functions=self._key_map[code]
            if type(functions)==list:
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

    def mouseReleaseEvent(self, event):
        pt = event.pos()
        modifiers = event.modifiers()

        if event.button() == QtCore.Qt.LeftButton:
            if self._select_area:
                if type(self._drawbox)==list:
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
        for callback in self._mouseMove_callback:
            callback(pt.x(), pt.y())

        if buttons == QtCore.Qt.MiddleButton:
            if  modifiers != QtCore.Qt.ShiftModifier:
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
                self.viewManager.transform(pt.x(),pt.y())
            # PAN
            elif modifiers == QtCore.Qt.ShiftModifier:
                dx = pt.x() - self.dragStartPosX
                dy = pt.y() - self.dragStartPosY
                self.dragStartPosX = pt.x()
                self.dragStartPosY = pt.y()
                self.cursor = "pan"
                self._display.Pan(dx, -dy)
                self._drawbox = False
        # DYNAMIC ZOOM
        elif (buttons == QtCore.Qt.RightButton and
              not modifiers == QtCore.Qt.ShiftModifier):
            self.cursor = "zoom"
            self._display.Repaint()
            self._display.DynamicZoom(abs(self.dragStartPosX),
                                      abs(self.dragStartPosY), abs(pt.x()),
                                      abs(pt.y()))
            self.dragStartPosX = pt.x()
            self.dragStartPosY = pt.y()
            self._drawbox = False

        # DRAW BOX
        # ZOOM WINDOW
        elif (buttons == QtCore.Qt.RightButton and
              modifiers == QtCore.Qt.ShiftModifier):
            self._zoom_area = True
            self.cursor = "zoom-area"
            self.DrawBox(evt)
            self.update()
        #SELECT AREA
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
