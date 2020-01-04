from __future__ import print_function
import sys
from OCC.Display.backend import load_any_qt_backend, get_qt_modules
load_any_qt_backend()
QtCore, QtGui, QtWidgets, QtOpenGL = get_qt_modules()
from OCC.Display.qtDisplay import qtViewer3d
from OCC.Core.AIS import *
from OCC.Core.Graphic3d import *
from OCC.Core.gp import *
from OCC.Core.Quantity import Quantity_Color,Quantity_NOC_SKYBLUE,Quantity_NOC_GRAY
from OCC.Core.Geom import Geom_Axis2Placement,Geom_Plane,Geom_Line,Geom_CartesianPoint
from OCC.Core.Quantity import *
class GLWidget(qtViewer3d):
    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)
        self.InitDriver()
        self._cubeManip=AIS_ViewCube()
        self._cubeManip.SetTransformPersistence(Graphic3d_TMF_TriedronPers, gp_Pnt(1, 1, 100))
        self._display.Context.Display(self._cubeManip,True)
        self.setReferenceAxe()
        assert isinstance(self._display.Context, AIS_InteractiveContext)
        # self._display.View.SetBgGradientColors(Quantity_Color(Quantity_NOC_SKYBLUE), Quantity_Color(Quantity_NOC_GRAY), 2, True)
    def setReferenceAxe(self):
        # axe = gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1))
        # geom_axe = Geom_Axis2Placement(axe)
        # self._refrenceAxies = AIS_Trihedron(geom_axe)
        # self._display.Context.Display(self._refrenceAxies,True)
        origin=Geom_CartesianPoint(gp_Pnt(0,0,0))
        ais_origin=AIS_Point(origin)
        ais_x=AIS_Line(origin,Geom_CartesianPoint(gp_Pnt(50,0,0)))
        ais_x.SetColor(Quantity_Color(1.0,0,0,Quantity_TOC_RGB))
        ais_y = AIS_Line(origin,Geom_CartesianPoint(gp_Pnt(0,50,0)))
        ais_y.SetColor(Quantity_Color(0, 1, 0, Quantity_TOC_RGB))
        ais_z = AIS_Line(origin,Geom_CartesianPoint(gp_Pnt(0,0,50)))
        ais_z.SetColor(Quantity_Color(0, 0, 1.0, Quantity_TOC_RGB))
        self._display.Context.Display(ais_origin, True)
        self._display.Context.Display(ais_x, True)
        self._display.Context.Display(ais_y, True)
        self._display.Context.Display(ais_z, True)
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