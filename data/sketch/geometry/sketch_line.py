from .sketch_geometry import *
from .sketch_point import Sketch_Point
from .geom2d_edge import Geom2d_Edge


class Sketch_Line(Sketch_Geometry):
    IndexCounter = 0

    def __init__(self, theContext, theAxis):
        super(Sketch_Line, self).__init__("Line", theContext, theAxis)
        self.myGeometry: Geom_Line = None
        self.myGeometry2d: Geom2d_Edge = None
        self.myAIS_InteractiveObject: AIS_Shape = None
        Sketch_Line.IndexCounter += 1
        self.myName = "Line" + str(self.IndexCounter)
        self.myPoles = []

    def AddPoints(self, thePnt2d):
        sketch_point = Sketch_Point(self.myContext, self.curCoordinateSystem)
        sketch_point.Compute(thePnt2d)
        self.myPoles.append(sketch_point)

    def GetPoles(self):
        return self.myPoles

    def Compute(self):
        startPnt2d = self.myPoles[0].GetGeometry2d().Pnt2d()
        endPnt2d = self.myPoles[1].GetGeometry2d().Pnt2d()
        self.myGeometry2d = Geom2d_Edge()
        self.myGeometry2d.SetPoints(startPnt2d, endPnt2d)

        startPnt = self.myPoles[0].GetGeometry().Pnt()
        endPnt = self.myPoles[1].GetGeometry().Pnt()
        dir = gp_Dir(gp_Vec(startPnt, endPnt))
        self.myGeometry = Geom_Line(startPnt, dir)

        self.myAIS_InteractiveObject = AIS_Line(self.myPoles[0].GetGeometry(), self.myPoles[1].GetGeometry())
        self.myAIS_InteractiveObject.SetAttributes(self.myDrawer)
        self.myContext.Display(self.myAIS_InteractiveObject, True)

    def Recompute(self):
        startPnt2d = self.myPoles[0].GetGeometry2d().Pnt2d()
        endPnt2d = self.myPoles[1].GetGeometry2d().Pnt2d()
        self.myGeometry2d.SetPoints(startPnt2d, endPnt2d)

        startPnt = self.myPoles[0].GetGeometry().Pnt()
        endPnt = self.myPoles[1].GetGeometry().Pnt()
        dir = gp_Dir(gp_Vec(startPnt, endPnt))
        self.myGeometry.SetLocation(startPnt)
        self.myGeometry.SetDirection(dir)
        self.myAIS_InteractiveObject.SetPoints(self.myPoles[0].GetGeometry(), self.myPoles[1].GetGeometry())
        self.myAIS_InteractiveObject.Redisplay(True)

    def DragTo(self, index, newPnt2d):
        self.myPoles[index].DragTo(newPnt2d)
        startPnt2d = self.myPoles[0].GetGeometry2d().Pnt2d()
        endPnt2d = self.myPoles[1].GetGeometry2d().Pnt2d()
        self.myGeometry2d.SetPoints(startPnt2d, endPnt2d)

        startPnt = self.myPoles[0].GetGeometry().Pnt()
        endPnt = self.myPoles[1].GetGeometry().Pnt()
        dir = gp_Dir(gp_Vec(startPnt, endPnt))
        self.myGeometry.SetLocation(startPnt)
        self.myGeometry.SetDirection(dir)
        self.myAIS_InteractiveObject.SetPoints(self.myPoles[0].GetGeometry(), self.myPoles[1].GetGeometry())
        self.myAIS_InteractiveObject.Redisplay(True)

    def RemoveDisplay(self):
        super(Sketch_Line, self).RemoveDisplay()
        for point in self.myPoles:
            point.RemoveDisplay()

    def GetGeometryType(self):
        return Sketch_GeometryType.LineSketchObject

    def GetTypeOfMethod(self):
        return Sketch_ObjectTypeOfMethod.Line2P_Method

    def DisplayName(self):
        if self.showViewportName:
            for point in self.myPoles:
                self.myContext.Display(point.myAIS_Name, True)
        else:
            for point in self.myPoles:
                self.myContext.Erase(point.myAIS_Name, True)

    def DisplayCoordinate(self):
        if self.showViewportCoordinate:
            for point in self.myPoles:
                self.myContext.Display(point.myAIS_Coordinate, True)
        else:
            for point in self.myPoles:
                self.myContext.Erase(point.myAIS_Coordinate, True)

    def DisplayAuxiliryLine(self):
        if self.showVieportAuxilirayLine:
            for point in self.myPoles:
                self.myContext.Display(point.GetAIS_Object(), True)
        else:
            for point in self.myPoles:
                self.myContext.Erase(point.GetAIS_Object(), True)

    def RemoveLabel(self):
        for point in self.myPoles:
            point.RemoveLabel()

    def GetStyle(self):
        return self.myLineStyle

    def SetStyle(self, theStyle):
        self.myLineStyle = theStyle

    def GetWidth(self):
        return self.myLineWidth

    def SetWidth(self, theWidth):
        self.myLineWidth = theWidth

    def GetColor(self):
        return self.myLineColor

    def SetColor(self, theColor):
        self.myLineColor = theColor
