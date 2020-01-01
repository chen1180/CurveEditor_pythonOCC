from OCC.Core.gp import gp_Pnt2d,gp_Pnt,gp_Pln,gp_Dir,gp_Ax3,gp_Ax2,gp_Vec,gp_Ax1
from OCC.Core.Geom import Geom_BezierCurve,Geom_BSplineCurve,Geom_Circle,Geom_SurfaceOfRevolution,Geom_Curve
from OCC.Core.GeomAPI import GeomAPI_PointsToBSpline
from OCC.Core.GeomAbs import *
from OCC.Core.Aspect import Aspect_GDM_Lines, Aspect_GT_Rectangular
from OCC.Core.TopAbs import *
from OCC.Core.TColgp import TColgp_Array1OfPnt
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Core.BRepAdaptor import BRepAdaptor_Curve
from OCC.Core.BRep import BRep_Tool
from OCC.Core.TopoDS import topods_Edge
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
    SURFACE_REVOLUTED=20
    def __init__(self,display):
        super(SketchController, self).__init__()
        self._display=display
        self._currentPos=None
        self._clickedPos=[]
        self._state=None
        self._shape_type=None
        self._selectedShape=None
    def action_bezierCurve(self):
        self._state = self.DRAW_START
        self._shape_type=self.CURVE_BEZIER

    def action_bSpline(self):
        self._state = self.DRAW_START
        self._shape_type = self.CURVE_BSPLINE

    def action_circle(self):
        self._state=self.DRAW_START
        self._shape_type=self.CURVE_CIRCLE
    def action_revolutedSurface(self):
        self._state=self.DRAW_START
        self._shape_type=self.SURFACE_REVOLUTED

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
        bspline = GeomAPI_PointsToBSpline(array)
        self._display.DisplayShape(bspline.Curve())

    def makeCircle(self):
        axe=gp_Ax2(self._clickedPos[0],self.new_sketch.dir)
        radius=self._clickedPos[0].Distance(self._clickedPos[1])
        circle=Geom_Circle(axe,radius)
        self._display.DisplayShape(circle)
    def makeSurfaceOfRevolution(self):
        # the first bezier curve
        surface=Geom_SurfaceOfRevolution(self._selectedShape,gp_Ax1(gp_Pnt(0.0,0.0,0.0),gp_Dir(1.0,0.0,0.0)))
        self._display.DisplayShape(surface)
        self.ExitDrawingMode()
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
            elif self._shape_type==self.SURFACE_REVOLUTED:
                pass
        else:
            try:
                if self._shape_type==self.CURVE_BEZIER:
                    self.makeBezierCurve()
                elif self._shape_type==self.CURVE_BSPLINE:
                    self.makeBSpline()
                elif self._shape_type==self.CURVE_CIRCLE:
                    self.makeCircle()
                elif self._shape_type==self.SURFACE_REVOLUTED:
                    self.makeSurfaceOfRevolution()
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
    def setSelectedShape(self,shp,*kargs):
        pass

    def recognize_clicked(self,shp, *kwargs):
        """ This is the function called every time
        a face is clicked in the 3d view
        """
        for shape in shp:
            if shape.ShapeType() == TopAbs_SOLID:
                print("solid selected")
            if shape.ShapeType() == TopAbs_EDGE:
                self.recognize_edge(topods_Edge(shape))
            if shape.ShapeType() == TopAbs_FACE:
                print("face selected")

    def recognize_edge(self,a_edge):
        """ Takes a TopoDS shape and tries to identify its nature
        whether it is a plane a cylinder a torus etc.
        if a plane, returns the normal
        if a cylinder, returns the radius
        """
        curve = BRepAdaptor_Curve(a_edge)
        curve_type = curve.GetType()
        if curve_type == GeomAbs_BezierCurve:
            print("--> Bezier")
            self._selectedShape=curve.Bezier()
        elif curve_type == GeomAbs_BSplineCurve:
            print("--> BSpline")
            self._selectedShape=curve.BSpline()
        elif curve_type == GeomAbs_Circle:
            print("--> Circle")
            self._selectedShape=Geom_Circle(curve.Circle())
        else:
            # TODO there are plenty other type that can be checked
            # see documentation for the BRepAdaptor class
            # https://www.opencascade.com/doc/occt-6.9.1/refman/html/class_b_rep_adaptor___surface.html
            print("not implemented")
    def createNewSketch(self):
        self.new_sketch=Sketch_NewSketchEditor(None,self._display)
        self.new_sketch.show()
        self.new_sketch.ui.uiOk.accepted.connect(self.createSketchNode)

    def createSketchNode(self):
        self.new_sketch.acceptData()
        self._sketch = SketchNode("Sketch")
        self.modelUpdate.emit(self._sketch)




