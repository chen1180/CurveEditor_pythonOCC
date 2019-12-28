from OCC.Core.gp import gp_Pnt2d,gp_Pnt
from OCC.Core.Geom import Geom_BezierCurve,Geom_BSplineCurve
from OCC.Core.GeomAPI import GeomAPI_PointsToBSpline
from OCC.Core.TColgp import TColgp_Array1OfPnt
from PyQt5.QtCore import *
import random
class ToolController(QObject):
    objectAdded=pyqtSignal(object)
    DRAW_END = 0
    DRAW_START=1

    CURVE_BEZIER = 10
    CURVE_NURBS = 11
    CURVE_BSPLINE=12
    def __init__(self):
        super(ToolController, self).__init__()
        self._currentPos=None
        self._clickedPos=[]
        self._state=None
        self._shape_type=None
    def EnterDrawingMode(self):
        if self._state==self.DRAW_START:
            if self._shape_type==self.CURVE_BEZIER:
                # the first bezier curve
                if self._currentPos:
                    self.objectAdded.emit(self._currentPos)
            elif self._shape_type==self.CURVE_BSPLINE:
                # the first bezier curve
                if self._currentPos:
                    self.objectAdded.emit(self._currentPos)
        else:
            try:
                if self._shape_type==self.CURVE_BEZIER:
                    array=TColgp_Array1OfPnt(1, len(self._clickedPos))
                    for i,p in enumerate(self._clickedPos):
                        array.SetValue(i+1,p)
                    bezier_curve=Geom_BezierCurve(array)
                    self.objectAdded.emit(bezier_curve)
                elif self._shape_type==self.CURVE_BSPLINE:
                    array=TColgp_Array1OfPnt(1, len(self._clickedPos))
                    for i,p in enumerate(self._clickedPos):
                        array.SetValue(i+1,p)
                    bspline=GeomAPI_PointsToBSpline(array).Curve()
                    self.objectAdded.emit(bspline)
            except Exception as e:
                print(e)
            finally:
                self.resetState()


    def ExitDrawingMode(self):
        self._state=self.DRAW_END
        self._currentPos=None

    def resetState(self):
        self._currentPos=None
        self._clickedPos.clear()
        self._shape_type=None

    def setMousePos(self,x,y,z):
        if self._state==self.DRAW_START:
            pos=gp_Pnt(x,y,z)
            self._currentPos=pos
            self._clickedPos.append(pos)

    def drawBezierCurve(self):
        self._state = self.DRAW_START
        self._shape_type=self.CURVE_BEZIER

    def drawBSpline(self):
        self._state = self.DRAW_START
        self._shape_type = self.CURVE_BSPLINE

    def drawNurbs(self):
        pass
#For debug purpose
if __name__ == '__main__':
    sys._excepthook = sys.excepthook
    def my_exception_hook(exctype, value, traceback):
        # Print the error and traceback
        print(exctype, value, traceback)
        # Call the normal Exception hook after
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)
    sys.excepthook = my_exception_hook
    application=QApplication([])
    # The follow format can set up the OPENGL context
    window = SceneDockWidget() #Opengl window creation
    window.addItem(Bezier(window,"asd",[QVector3D(0,0,0),QVector3D(0,0,2)]))
    window.show()
    application.exec_()