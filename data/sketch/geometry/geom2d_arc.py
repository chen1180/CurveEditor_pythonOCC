from OCC.Core.ElCLib import elclib
from OCC.Core.Geom2d import Geom2d_Circle
from OCC.Core.gp import gp_Pnt2d, gp_Dir2d, gp, gp_Vec2d, gp_Circ2d, gp_Circ

M_PI = 3.14

class Geom2d_Arc(Geom2d_Circle):
    def __init__(self, C: gp_Circ2d):
        super(Geom2d_Arc, self).__init__(C)
        self.myFirstParam = 0.0
        self.myLastParam = 2.0 * M_PI

    def SetParam(self, start: gp_Pnt2d, end: gp_Pnt2d):
        self.myFirstParam = elclib.Parameter(self.Circ2d(), start)
        self.myLastParam = elclib.Parameter(self.Circ2d(), end)
        # u = elclib.Parameter(self.Circ2d(), mid)
        self.CheckParam()
        # if self.myFirstParam < u and u < self.myLastParam or self.myLastParam < u + 2 * M_PI and u + 2 * M_PI < self.myLastParam:
        #     pass
        # else:
        #     if self.myLastParam > 2 * M_PI:
        #         self.myLastParam -= 2 * M_PI
        #         u = self.myFirstParam
        #     else:
        #         u = self.myFirstParam + 2 * M_PI
        #     self.myFirstParam = self.myLastParam
        #     self.myLastParam = u

    def SetFirstParam(self, u1):
        if type(u1) == float:
            self.myFirstParam = u1
        elif type(u1) == gp_Pnt2d:
            self.myFirstParam = elclib.Parameter(self.Circ2d(), u1)
        self.CheckParam()

    def SetLastParam(self, u2):
        if type(u2) == float:
            self.myLastParam = u2
        elif type(u2) == gp_Pnt2d:
            self.myLastParam = elclib.Parameter(self.Circ2d(), u2)
        self.CheckParam()

    def FirstParameter(self):
        return self.myFirstParam

    def LastParameter(self):
        return self.myLastParam

    def FirstPnt(self):
        return elclib.Value(self.myFirstParam, self.Circ2d())

    def LastPnt(self):
        return elclib.Value(self.myLastParam, self.Circ2d())



    # def MiddlePnt(self):
    #     return elclib.Value((self.myLastParam + self.myFirstParam) / 2, self.Circ2d())

    def CheckParam(self):
        while self.myFirstParam > 2 * M_PI:
            self.myFirstParam -= 2 * M_PI
        while self.myLastParam > 2 * M_PI or self.myLastParam - self.myFirstParam > 2 * M_PI:
            self.myLastParam -= 2 * M_PI
        while self.myFirstParam > self.myLastParam:
            self.myLastParam += 2 * M_PI
