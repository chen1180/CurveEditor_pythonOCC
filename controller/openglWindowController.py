from PyQt5 import QtCore,QtGui,QtWidgets
from OpenGL.GL import *
import sys
from view.openglWindow import GLWidget
from controller import toolController

import logging

HAVE_PYQT_SIGNAL = hasattr(QtCore, 'pyqtSignal')

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger(__name__)
class OpenGLEditor(GLWidget):
    modelUpdated=QtCore.pyqtSignal(object)
    def __init__(self, parent=None):
        super(OpenGLEditor, self).__init__(parent)
        self._objects=[]
        self.shape_drawer=toolController.ToolController()
        #callback functions
        self._display.register_select_callback(self.coordinate_clicked)
        self.shape_drawer.objectAdded.connect(self.addNewItem)

    def addNewItem(self,item):
        self._objects.append(item)
        self._display.DisplayShape(item,update=True)
    def setScene(self,scene):
        self._objects=scene

    def paintEvent(self, event):
        super(OpenGLEditor, self).paintEvent(event)
        self.shape_drawer.EnterDrawingMode()
        self.update()

    def coordinate_clicked(self,shp, *kwargs):
        """ This function is called whenever a vertex is selected
        """
        for shape in shp:
            print("Shape selected: ", shape)
        point_2d=kwargs
        x, y, z, vx, vy, vz = self._display.View.ConvertWithProj(kwargs[0],kwargs[1])
        self.shape_drawer.setMousePos(x, y, z)
    def keyPressEvent(self, event):
        code = event.key()
        if code in self._key_map:
            self._key_map[code]()
        elif code in range(256):
            log.info('key: "%s"(code %i) not mapped to any function' % (chr(code), code))
        else:
            log.info('key: code %i not mapped to any function' % code)
        if code==QtCore.Qt.Key_Escape:
            self.shape_drawer.ExitDrawingMode()

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
        ev = event.pos()
        self.dragStartPosX = ev.x()
        self.dragStartPosY = ev.y()
        self._display.StartRotation(self.dragStartPosX, self.dragStartPosY)

    def mouseReleaseEvent(self, event):
        pt = event.pos()
        modifiers = event.modifiers()

        if event.button() == QtCore.Qt.LeftButton:
            if self._select_area:
                [Xmin, Ymin, dx, dy] = self._drawbox
                self._display.SelectArea(Xmin, Ymin, Xmin + dx, Ymin + dy)
                self._select_area = False
            else:
                # multiple select if shift is pressed
                if modifiers == QtCore.Qt.ShiftModifier:
                    self._display.ShiftSelect(pt.x(), pt.y())
                else:
                    # single select otherwise
                    self._display.Select(pt.x(), pt.y())

                    if (self._display.selected_shapes is not None) and HAVE_PYQT_SIGNAL:
                        self.sig_topods_selected.emit(self._display.selected_shapes)


        elif event.button() == QtCore.Qt.RightButton:
            if self._zoom_area:
                [Xmin, Ymin, dx, dy] = self._drawbox
                self._display.ZoomArea(Xmin, Ymin, Xmin + dx, Ymin + dy)
                self._zoom_area = False

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
        # ROTATE
        if (buttons == QtCore.Qt.LeftButton and
                not modifiers == QtCore.Qt.ShiftModifier):
            self.cursor = "rotate"
            self._display.Rotation(pt.x(), pt.y())
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
        # PAN
        elif buttons == QtCore.Qt.MidButton:
            dx = pt.x() - self.dragStartPosX
            dy = pt.y() - self.dragStartPosY
            self.dragStartPosX = pt.x()
            self.dragStartPosY = pt.y()
            self.cursor = "pan"
            self._display.Pan(dx, -dy)
            self._drawbox = False
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
    def getOpenglInfo(self):
        info = """ 
      Vendor: {0} 
      Renderer: {1} 
      OpenGL Version: {2} 
      Shader Version: {3} 
     """.format(
            glGetString(GL_VENDOR),
            glGetString(GL_RENDERER),
            glGetString(GL_VERSION),
            glGetString(GL_SHADING_LANGUAGE_VERSION)
        )
        return info
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
