from PyQt5 import QtCore,QtGui,QtWidgets
from OpenGL.GL import *
import sys
from view.openglWindow import Ui_GLWindow
from controller import drawController
class OpenGLEditor(Ui_GLWindow):
    modelUpdated=QtCore.pyqtSignal(object)
    def __init__(self, parent=None):
        super(OpenGLEditor, self).__init__(parent)
        self._sceneObjects=None
        self._drawController=drawController.DrawController()
        self._sceneObjects=None
        self._selection=None
    def setScene(self,scene):
        self._sceneObjects=scene
    def drawBox(self, painter):
        """ overpaint a rectangle on top of the viewport, when selecting with
        Shift + right mouse button
        """
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0), 1))
        tolerance = 2

        dx, dy = self.delta_mouse_event_pos

        if abs(dx) <= tolerance and abs(dy) <= tolerance:
            pass

        else:
            rect = QtCore.QRect(self.point_on_mouse_press[0],
                                self.point_on_mouse_press[1], -dx, -dy)
            painter.drawRect(rect)
    def paintEvent(self, event):
        super(Ui_GLWindow, self).paintEvent(event)
        if self._inited:
            # actions like panning, zooming and rotating the view invoke
            # redrawing it
            # therefore, these actions need to be performed in the paintEvent
            # method
            # this way, redrawing the view takes place synchronous with the
            # overpaint action
            # not respecting this order would lead to a jittering view
            if not self._dispatch_camera_command_actions():
                # if no camera actions took place, invoke a redraw of
                # the viewport
                self._display.View.Redraw()

            if self.context().isValid():
                # acquire the OpenGL context
                self.makeCurrent()
                # swap the buffer before overpainting it
                self.swapBuffers()
                # perform overpainting
                self.paintGL()
                # hand over the OpenGL context
                self.doneCurrent()
            else:
                print('invalid OpenGL context: Qt cannot overpaint viewer')
    def initializeGL(self) -> None:
        super(OpenGLEditor, self).initializeGL()
        print(self.getOpenglInfo())
    def resizeGL(self, w: int, h: int) -> None:
        super(OpenGLEditor, self).resizeGL(w, h)
        side = min(w, h)
        glViewport((w - h) // 2, (w - h) // 2, side, side)
        self.resized = True

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
