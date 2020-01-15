from .sketch_geometry import *


class Sketch_Point(Sketch_Geometry):
    IndexCounter = 0

    def __init__(self):
        super(Sketch_Point, self).__init__("Point")
        self.myGeometry: Geom_CartesianPoint = None
        self.myGeometry2d: Geom2d_CartesianPoint = None
        self.myAIS_InteractiveObject: AIS_Point = None
        self.myPointStyle = Aspect_TOM_RING1
        Sketch_Point.IndexCounter += 1
        self.myName = "Point" + str(self.IndexCounter)

    def Init(self, thePnt2d):
        self.myGeometry2d = Geom2d_CartesianPoint(thePnt2d)
        self.myGeometry = Geom_CartesianPoint(Pnt2dToPnt(thePnt2d, self.curCoordinateSystem))
        self.myAIS_InteractiveObject = AIS_Point(self.myGeometry)
        self.myAIS_InteractiveObject.SetMarker(self.myPointStyle)
        self.myContext.Display(self.myAIS_InteractiveObject, True)

    def DragTo(self, newPnt2d):
        self.myGeometry2d.SetPnt2d(newPnt2d)
        newPnt = Pnt2dToPnt(newPnt2d, self.curCoordinateSystem)
        self.myGeometry.SetPnt(newPnt)
        self.myAIS_InteractiveObject.Redisplay(True)

    def RemoveDisplay(self):
        self.myContext.Remove(self.myAIS_InteractiveObject, True)

    def GetGeometryType(self):
        return Sketch_GeometryType.PointSketchObject

    def GetTypeOfMethod(self):
        return Sketch_ObjectTypeOfMethod.Point_Method
