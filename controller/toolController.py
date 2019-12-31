from OCC.Core.gp import gp_Pnt2d,gp_Pnt,gp_Pln,gp_Dir,gp_Ax3,gp_Ax2,gp_Vec
from OCC.Core.Geom import Geom_BezierCurve,Geom_BSplineCurve,Geom_Circle
from OCC.Core.GeomAPI import GeomAPI_PointsToBSpline
from OCC.Core.Aspect import Aspect_GDM_Lines, Aspect_GT_Rectangular
from OCC.Core.TColgp import TColgp_Array1OfPnt
from PyQt5.QtCore import *
from controller.editorController import Sketch_NewSketchEditor
from data.node import *
class SketchController(QObject):
    modelUpdate=pyqtSignal(object)
    DRAW_END = 0
    DRAW_START=1

    CURVE_BEZIER = 10
    CURVE_BSPLINE=11
    CURVE_CIRCLE=12
    def __init__(self,display):
        super(SketchController, self).__init__()
        self._display=display
        self._currentPos=None
        self._clickedPos=[]
        self._state=None
        self._shape_type=None
    def action_bezierCurve(self):
        self._state = self.DRAW_START
        self._shape_type=self.CURVE_BEZIER

    def action_bSpline(self):
        self._state = self.DRAW_START
        self._shape_type = self.CURVE_BSPLINE

    def action_circle(self):
        self._state=self.DRAW_START
        self._shape_type=self.CURVE_CIRCLE

    def makeBezierCurve(self):
        array = TColgp_Array1OfPnt(1, len(self._clickedPos))
        for i, p in enumerate(self._clickedPos):
            array.SetValue(i + 1, p)
        bezier_curve = Geom_BezierCurve(array)
        self._display.DisplayShape(bezier_curve)

    def makeBSpline(self):
        array = TColgp_Array1OfPnt(1, len(self._clickedPos))
        for i, p in enumerate(self._clickedPos):
            array.SetValue(i + 1, p)
        bspline = GeomAPI_PointsToBSpline(array).Curve()
        self._display.DisplayShape(bspline)

    def makeCircle(self):
        axe=gp_Ax2(self._clickedPos[0],self.new_sketch.dir)
        radius=self._clickedPos[0].Distance(self._clickedPos[1])
        circle=Geom_Circle(axe,radius)
        self._display.DisplayShape(circle)

    def EnterDrawingMode(self):
        if self._state==self.DRAW_START:
            if self._shape_type==self.CURVE_BEZIER:
                # the first bezier curve
                if self._currentPos:
                    self._display.DisplayShape(self._currentPos)
            elif self._shape_type==self.CURVE_BSPLINE:
                # the first bezier curve
                if self._currentPos:
                    self._display.DisplayShape(self._currentPos)
            elif self._shape_type==self.CURVE_CIRCLE:
                # the first bezier curve
                if self._currentPos:
                    self._display.DisplayShape(self._currentPos)
        else:
            try:
                if self._shape_type==self.CURVE_BEZIER:
                    self.makeBezierCurve()
                elif self._shape_type==self.CURVE_BSPLINE:
                    self.makeBSpline()
                elif self._shape_type==self.CURVE_CIRCLE:
                    self.makeCircle()
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

    def createNewSketch(self):
        self.new_sketch=Sketch_NewSketchEditor(None,self._display)
        self.new_sketch.show()
        self.new_sketch.ui.uiOk.accepted.connect(self.createSketchNode)

    def createSketchNode(self):
        self.new_sketch.acceptData()
        self._sketch = SketchNode("Sketch")
        self.modelUpdate.emit(self._sketch)




