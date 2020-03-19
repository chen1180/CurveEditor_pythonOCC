from .sketch_geometry import *


class Sketch_Point(Sketch_Geometry):
    IndexCounter = 0

    def __init__(self, theContext, theAxis):
        super(Sketch_Point, self).__init__("Point", theContext, theAxis)
        self.myGeometry: Geom_CartesianPoint = None
        self.myGeometry2d: Geom2d_CartesianPoint = None
        self.myAIS_InteractiveObject: AIS_Shape = None
        Sketch_Point.IndexCounter += 1
        self.myName = "Point" + str(self.IndexCounter)

    def Compute(self, thePnt2d):
        self.myGeometry2d = Geom2d_CartesianPoint(thePnt2d)
        self.myGeometry = Geom_CartesianPoint(Pnt2dToPnt(thePnt2d, self.curCoordinateSystem))
        vertex = BRepBuilderAPI_MakeVertex(self.myGeometry.Pnt())
        self.myAIS_InteractiveObject = AIS_Shape(vertex.Shape())
        self.myAIS_InteractiveObject.SetAttributes(self.myDrawer)
        self.myContext.Display(self.myAIS_InteractiveObject, True)

        # Text label
        coordinate = "({},{})".format(round(thePnt2d.X(), 1), round(thePnt2d.Y(), 1))
        self.myAIS_Coordinate = self.CreateLabel(coordinate, Quantity_NOC_GREEN)
        self.myAIS_Name = self.CreateLabel(self.myName, Quantity_NOC_BLUE1, offset=gp_Vec(-50, -50, -50))

    def CreateLabel(self, text: str, color, offset=gp_Vec(50, 50, 50)):
        # Text label
        myAIS_Text = AIS_TextLabel()
        myAIS_Text.SetText(
            TCollection_ExtendedString(text))
        myAIS_Text.SetPosition(self.myGeometry.Pnt().Translated(offset))
        myAIS_Text.SetColor(Quantity_Color(color))
        myAIS_Text.SetHeight(30)
        self.myContext.Deactivate(myAIS_Text)
        return myAIS_Text

    def DragTo(self, newPnt2d):
        self.myGeometry2d.SetPnt2d(newPnt2d)
        newPnt = Pnt2dToPnt(newPnt2d, self.curCoordinateSystem)
        self.myGeometry.SetPnt(newPnt)
        vertex = BRepBuilderAPI_MakeVertex(self.myGeometry.Pnt())
        self.myAIS_InteractiveObject.SetShape(vertex.Shape())
        self.myAIS_InteractiveObject.Redisplay(True)
        # update text label
        coordinate = "({},{})".format(round(newPnt2d.X(), 1), round(newPnt2d.Y(), 1))
        self.myAIS_Coordinate.SetText(TCollection_ExtendedString(coordinate))
        self.myAIS_Coordinate.SetPosition(self.myGeometry.Pnt().Translated(gp_Vec(50, 50, 50)))
        self.myAIS_Name.SetPosition(self.myGeometry.Pnt().Translated(gp_Vec(-50, -50, -50)))
        self.myAIS_Coordinate.Redisplay(True)
        self.myAIS_Name.Redisplay(True)

    def GetGeometryType(self):
        return Sketch_GeometryType.PointSketchObject

    def GetTypeOfMethod(self):
        return Sketch_ObjectTypeOfMethod.Point_Method

    def DisplayName(self):
        if self.showViewportName:
            self.myContext.Display(self.myAIS_Name, True)
        else:
            self.myContext.Erase(self.myAIS_Name, True)

    def DisplayCoordinate(self):
        if self.showViewportCoordinate:
            self.myContext.Display(self.myAIS_Coordinate, True)
        else:
            self.myContext.Erase(self.myAIS_Coordinate, True)

    def RemoveLabel(self):
        self.myContext.Remove(self.myAIS_Coordinate, True)
        self.myContext.Remove(self.myAIS_Name, True)

    def GetStyle(self):
        return self.myPointStyle

    def SetStyle(self, theStyle):
        self.myPointStyle = theStyle

    def GetColor(self):
        return self.myPointColor

    def SetColor(self, theColor):
        self.myPointColor = theColor
        self.myPointAspect.SetColor(theColor)

    def GetWidth(self):
        return self.myPointWidth

    def SetWidth(self, theWidth):
        self.myPointWidth = theWidth
