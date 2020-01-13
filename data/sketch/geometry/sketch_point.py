from .sketch_geometry import *


class Sketch_Point(Sketch_Geometry):
    def __init__(self):
        super(Sketch_Point, self).__init__()
        self.myGeometry: Geom_CartesianPoint = None
        self.myAIS_InteractiveObject: AIS_Point = None
        self.myPointStyle=Aspect_TOM_RING1

    def Init(self, thePnt2d):
        self.myGeometry = Geom_CartesianPoint(Pnt2dToPnt(thePnt2d, self.curCoordinateSystem))
        self.myAIS_InteractiveObject = AIS_Point(self.myGeometry)
        self.myAIS_InteractiveObject.SetMarker(self.myPointStyle)
        self.myContext.Display(self.myAIS_InteractiveObject, True)


    def DragTo(self, newPnt2d):
        newPnt = Pnt2dToPnt(newPnt2d, self.curCoordinateSystem)
        self.myGeometry.SetPnt(newPnt)
        self.myAIS_InteractiveObject.Redisplay(True)
