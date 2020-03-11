from OCC.Core.Geom import Geom_Plane
from OCC.Core.AIS import AIS_Plane
from OCC.Core.gp import *


class Sketch_Plane(object):

    def __init__(self, theContext, theCoordinate):
        self.myContext = theContext
        self.myCoordinate = theCoordinate
        self.myGeometry: Geom_Plane = None
        self.myAIS_InteractiveObject: AIS_Plane = None

    def Compute(self):
        self.myGeometry = Geom_Plane(self.myCoordinate)
        self.myAIS_InteractiveObject= AIS_Plane(self.myGeometry, True)
        # plane=self.myGeometry.Pln().Location()
        self.myAIS_InteractiveObject.SetPlaneAttributes(self.myGeometry, gp_Pnt(0,0,0), gp_Pnt(-1000,-1000,0), gp_Pnt(1000,1000,0))
        # self.myContext.Display(self.myAIS_InteractiveObject, True)

    def Recompute(self):
        pass

    def GetCoordinate(self):
        return self.myCoordinate
