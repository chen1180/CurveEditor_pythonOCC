from OCC.Core.Geom import *
from OCC.Core.AIS import AIS_Plane
from OCC.Core.gp import *


class Sketch_PlaneType:
    XY = 0
    YZ = 1
    XZ = 2


class Sketch_Plane(object):

    def __init__(self, theContext, theCoordinate):
        self.myContext = theContext
        self.myCoordinate = theCoordinate
        self.myGeometry: Geom_Plane = None
        self.myAIS_InteractiveObject: AIS_Plane = None

    def Compute(self):
        self.myGeometry = Geom_Plane(self.myCoordinate)
        self.myAIS_InteractiveObject = AIS_Plane(self.myGeometry, True)
        # minValue=-500
        # maxValue=500
        # if self.myPlaneType==Sketch_PlaneType.XY:
        #     min,max=gp_Pnt(minValue,minValue,0),gp_Pnt(maxValue,maxValue,0)
        # elif self.myPlaneType==Sketch_PlaneType.YZ:
        #     min, max = gp_Pnt(0,minValue, minValue), gp_Pnt(0,maxValue, maxValue)
        # else:
        #     min, max = gp_Pnt(minValue,0,  minValue), gp_Pnt( maxValue, 0,maxValue)
        # self.myAIS_InteractiveObject.SetPlaneAttributes(self.myGeometry, gp_Pnt(0, 0, 0), min,max)
        self.myContext.Display(self.myAIS_InteractiveObject, True)

    def Recompute(self):
        pass

    def GetCoordinate(self):
        return self.myCoordinate
