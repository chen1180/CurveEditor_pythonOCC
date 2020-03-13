from __future__ import print_function
import sys
from OCC.Display.backend import load_any_qt_backend, get_qt_modules
load_any_qt_backend()
QtCore, QtGui, QtWidgets, QtOpenGL = get_qt_modules()
from OCC.Display.qtDisplay import qtViewer3d
class GLWidget(qtViewer3d):
    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)
if __name__ == '__main__':
    def TestOverPainting():
        class AppFrame(QtWidgets.QWidget):
            def __init__(self, parent=None):
                QtWidgets.QWidget.__init__(self, parent)
                self.setWindowTitle(self.tr("qtDisplay3d overpainting example"))
                self.resize(1280, 1024)
                self.canva = GLWidget(self)
                mainLayout = QtWidgets.QHBoxLayout()
                mainLayout.addWidget(self.canva)
                mainLayout.setContentsMargins(0, 0, 0, 0)
                self.setLayout(mainLayout)

            def runTests(self):
                self.canva._display.Test()

        app = QtWidgets.QApplication(sys.argv)
        frame = AppFrame()
        frame.show()
        frame.runTests()
        app.exec_()

    TestOverPainting()