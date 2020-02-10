from .sketch_geometry import *


class Sketch_Point(Sketch_Geometry):
    IndexCounter = 0

    def __init__(self, theContext, theAxis):
        super(Sketch_Point, self).__init__("Point", theContext, theAxis)
        self.myGeometry: Geom_CartesianPoint = None
        self.myGeometry2d: Geom2d_CartesianPoint = None
        self.myAIS_InteractiveObject: AIS_Point = None
        # self.myAIS_Text:AIS_TextLabel=None
        self.myPointStyle = Aspect_TOM_O_POINT
        Sketch_Point.IndexCounter += 1
        self.myName = "Point" + str(self.IndexCounter)

    def Compute(self, thePnt2d):
        self.myGeometry2d = Geom2d_CartesianPoint(thePnt2d)
        self.myGeometry = Geom_CartesianPoint(Pnt2dToPnt(thePnt2d, self.curCoordinateSystem))
        self.myAIS_InteractiveObject = AIS_Point(self.myGeometry)
        self.myAIS_InteractiveObject.SetMarker(self.myPointStyle)
        self.myContext.Display(self.myAIS_InteractiveObject, True)
        #Text label
        # self.myAIS_Text = AIS_TextLabel()
        # self.myAIS_Text.SetText(TCollection_ExtendedString("({},{})".format(thePnt2d.X(),thePnt2d.Y())))
        # self.myAIS_Text.SetPosition(self.myGeometry.Pnt())
        # self.myAIS_Text.SetColor(Quantity_Color(Quantity_NOC_GREEN))
        # self.myContext.Display(self.myAIS_Text, True)

    def DragTo(self, newPnt2d):
        self.myGeometry2d.SetPnt2d(newPnt2d)
        newPnt = Pnt2dToPnt(newPnt2d, self.curCoordinateSystem)
        self.myGeometry.SetPnt(newPnt)
        self.myAIS_InteractiveObject.Redisplay(True)

    def GetGeometryType(self):
        return Sketch_GeometryType.PointSketchObject

    def GetTypeOfMethod(self):
        return Sketch_ObjectTypeOfMethod.Point_Method
