from OCC.Core.ElCLib import elclib
from OCC.Core.AIS import AIS_Point
from OCC.Core.Geom2d import Geom2d_CartesianPoint, Geom2d_Line, Geom2d_Circle,_swig_repr,_Geom2d
from OCC.Core.gp import gp_Pnt2d, gp_Dir2d, gp, gp_Vec2d, gp_Circ2d, gp_Circ,gp_Ax2d
from OCC.Core.Geom import Geom_Circle
from OCC.Core.AIS import AIS_Circle
from OCC.Display.SimpleGui import init_display
M_PI = 3.14
from OCC.Core.Geom2dGcc import Geom2dGcc_Circ2d3Tan, Geom2dGcc_QualifiedCurve
from OCC.Core.GccEnt import gccent_Unqualified
from OCC.Core.gce import gce_MakeCirc, gce_Done

class Geom2d_Arc(Geom2d_Circle):
    def __init__(self, C: gp_Circ2d):
        super(Geom2d_Arc, self).__init__(C)
        self.myFirstParam = 0.0
        self.myLastParam = 2.0 * M_PI
    def SetParam(self, start: gp_Pnt2d, mid: gp_Pnt2d, end: gp_Pnt2d):
        self.myFirstParam = elclib.Parameter(gp_Circ2d(), start)
        self.myLastParam = elclib.Parameter(gp_Circ2d(), end)
        u = elclib.Parameter(gp_Circ2d(), mid)
        self.CheckParam()
        if self.myFirstParam < u and u < self.myLastParam or self.myLastParam < u + 2 * M_PI and u + 2 * M_PI < self.myLastParam:
            pass
        else:
            if self.myLastParam > 2 * M_PI:
                self.myLastParam -= 2 * M_PI
                u = self.myFirstParam
            else:
                u = self.myFirstParam + 2 * M_PI
            self.myFirstParam = self.myLastParam
            self.myLastParam = u

    def SetFirstParam(self, u1):
        if type(u1) == float:
            self.myFirstParam = u1
        elif type(u1) == gp_Pnt2d:
            self.myFirstParam = elclib.Parameter(gp_Circ2d(), u1)
        self.CheckParam()

    def SetLastParam(self, u2):
        if type(u2) == float:
            self.myLastParam = u2
        elif type(u2) == gp_Pnt2d:
            self.myLastParam = elclib.Parameter(gp_Circ2d(), u2)
        self.CheckParam()

    def FirstParameter(self):
        return self.myFirstParam

    def LastParameter(self):
        return self.myLastParam

    def FirstPnt(self):
        return elclib.Value(self.myFirstParam, gp_Circ2d())

    def LastPnt(self):
        return elclib.Value(self.myLastParam, gp_Circ2d())

    def MiddlePnt(self):
        return elclib.Value((self.myLastParam + self.myFirstParam) / 2, gp_Circ2d())

    def CheckParam(self):
        while self.myFirstParam > 2 * M_PI:
            self.myFirstParam -= 2 * M_PI
        while self.myLastParam > 2 * M_PI or self.myLastParam - self.myFirstParam > 2 * M_PI:
            self.myLastParam -= 2 * M_PI
        while self.myFirstParam > self.myLastParam:
            self.myLastParam += 2 * M_PI

class Circle(Geom_Circle):
    def __init__(self,circle):
        super(Circle, self).__init__(circle)
circle=gp_Circ2d()
circle.SetRadius(10)
circle.SetXAxis(gp_Ax2d(gp_Pnt2d(0,0),gp_Dir2d(1,0)))
arc=Geom2d_Arc(circle)
arc.SetParam(gp_Pnt2d(2,0),gp_Pnt2d(2,1),gp_Pnt2d(2,5))
tempGcc_Circ2d3Tan = Geom2dGcc_Circ2d3Tan(gp_Pnt2d(2,0),gp_Pnt2d(2,1),gp_Pnt2d(2,5), 1.0e-10)

geom_circle=Circle(tempGcc_Circ2d3Tan.ThisSolution(1))
ais_circle=AIS_Circle(geom_circle)
display, start_display, add_menu, add_function_to_menu = init_display()
display.Context.Display(ais_circle,False)
start_display()