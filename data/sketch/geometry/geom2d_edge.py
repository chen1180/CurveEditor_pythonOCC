from OCC.Core.ElCLib import elclib
from OCC.Core.AIS import AIS_Point
from OCC.Core.Geom2d import Geom2d_CartesianPoint,Geom2d_Line
from OCC.Core.gp import gp_Pnt2d,gp_Dir2d,gp,gp_Vec2d
from OCC.Core._Geom2d import Geom2d_Line_swigregister
class Geom2d_Edge(Geom2d_Line):
    def __init__(self):
        super(Geom2d_Edge, self).__init__(gp.Origin2d(),gp.DX2d())
        self.StartPnt=gp_Pnt2d()
        self.EndPnt=gp_Pnt2d()
    def SetPoints(self,p1:gp_Pnt2d,p2:gp_Pnt2d):
        if p1.IsEqual(p2,0)==False:
            self.SetDirection(gp_Dir2d(gp_Vec2d(p1,p2)))
            self.SetLocation(p1)
            self.StartPnt=p1
            self.EndPnt=p2
            return True
        else:
            return False
    def GetStart_Pnt(self):
        return self.StartPnt
    def GetEnd_Pnt(self):
        return self.EndPnt
    def MiddlePnt(self):
        return self.StartPnt.Scaled(self.EndPnt,0.5)
    def StartParameter(self):
        return elclib.Parameter(self.Lin2d(),self.StartPnt)
    def EndParameter(self):
        return elclib.Parameter(self.Lin2d(), self.EndPnt)
# Register Geom2d_Line in _Geom2d:
Geom2d_Line_swigregister(Geom2d_Edge)
