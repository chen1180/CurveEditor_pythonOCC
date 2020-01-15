from .sketch_geometry import *
from .sketch_point import Sketch_Point
from .geom2d_edge import Geom2d_Edge


class Sketch_Line(Sketch_Geometry):
    IndexCounter = 0

    def __init__(self):
        super(Sketch_Line, self).__init__("Line")
        self.myGeometry: Geom_Line = None
        self.myGeometry2d: Geom2d_Edge = None
        self.myAIS_InteractiveObject: AIS_Shape = None
        Sketch_Line.IndexCounter += 1
        self.myName = "Line" + str(self.IndexCounter)
        self.myPoints = []

    def AddPoints(self, thePnt2d):
        sketch_point = Sketch_Point()
        sketch_point.SetAxis(self.curCoordinateSystem)
        sketch_point.SetContext(self.myContext)
        sketch_point.Init(thePnt2d)
        self.myPoints.append(sketch_point)

    def GetPoints(self):
        return self.myPoints

    def Compute(self):
        startPnt2d = self.myPoints[0].GetGeometry2d().Pnt2d()
        endPnt2d = self.myPoints[1].GetGeometry2d().Pnt2d()
        self.myGeometry2d = Geom2d_Edge()
        self.myGeometry2d.SetPoints(startPnt2d, endPnt2d)

        startPnt = self.myPoints[0].GetGeometry().Pnt()
        endPnt = self.myPoints[1].GetGeometry().Pnt()
        dir = gp_Dir(gp_Vec(startPnt, endPnt))
        self.myGeometry = Geom_Line(startPnt, dir)

        self.myAIS_InteractiveObject = AIS_Line(self.myPoints[0].GetGeometry(), self.myPoints[1].GetGeometry())
        self.myContext.Display(self.myAIS_InteractiveObject, True)

    def Recompute(self):
        startPnt2d = self.myPoints[0].GetGeometry2d().Pnt2d()
        endPnt2d = self.myPoints[1].GetGeometry2d().Pnt2d()
        self.myGeometry2d.SetPoints(startPnt2d, endPnt2d)

        startPnt = self.myPoints[0].GetGeometry().Pnt()
        endPnt = self.myPoints[1].GetGeometry().Pnt()
        dir = gp_Dir(gp_Vec(startPnt, endPnt))
        self.myGeometry.SetLocation(startPnt)
        self.myGeometry.SetDirection(dir)
        self.myAIS_InteractiveObject.SetPoints(self.myPoints[0].GetGeometry(), self.myPoints[1].GetGeometry())
        self.myAIS_InteractiveObject.Redisplay(True)

    def GetGeometryType(self):
        return Sketch_GeometryType.LineSketchObject

    def GetTypeOfMethod(self):
        return Sketch_ObjectTypeOfMethod.Line2P_Method
