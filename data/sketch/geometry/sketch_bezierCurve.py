from .sketch_geometry import *
from .sketch_point import Sketch_Point


class Sketch_BezierCurve(Sketch_Geometry):
    IndexCounter = 0

    def __init__(self):
        super(Sketch_BezierCurve, self).__init__("Bezier curve")
        self.myGeometry: Geom_BezierCurve = None
        self.myGeometry2d: Geom2d_BezierCurve = None
        self.myAis_shape: AIS_Shape = None
        self.myPoles = []
        Sketch_BezierCurve.IndexCounter += 1
        self.myName = "Bezier curve" + str(self.IndexCounter)

    def AddPoles(self, thePnt2d):
        sketch_point = Sketch_Point()
        sketch_point.SetAxis(self.curCoordinateSystem)
        sketch_point.SetContext(self.myContext)
        sketch_point.Init(thePnt2d)
        self.myPoles.append(sketch_point)

    def GetPoles(self):
        return self.myPoles

    def Compute(self):
        poles2d_list = [pole.GetGeometry2d().Pnt2d() for pole in self.myPoles]
        arrayOfPoles2d = point_list_to_TColgp_Array1OfPnt2d(poles2d_list)
        self.myGeometry2d = Geom2d_BezierCurve(arrayOfPoles2d)

        poles_list = [pole.GetGeometry().Pnt() for pole in self.myPoles]
        arrayOfPoles = point_list_to_TColgp_Array1OfPnt(poles_list)
        self.myGeometry = Geom_BezierCurve(arrayOfPoles)

        edge = BRepBuilderAPI_MakeEdge(self.myGeometry)
        self.myAis_shape = AIS_Shape(edge.Edge())
        self.myContext.Display(self.myAis_shape, True)

    def Recompute(self):
        poles2d_list = [pole.GetGeometry2d().Pnt2d() for pole in self.myPoles]
        for index, pole2d in enumerate(poles2d_list):
            self.myGeometry2d.SetPole(index + 1, pole2d)
        poles_list = [pole.GetGeometry().Pnt() for pole in self.myPoles]
        for index, pole in enumerate(poles_list):
            self.myGeometry.SetPole(index + 1, pole)

        edge = BRepBuilderAPI_MakeEdge(self.myGeometry)
        self.myAis_shape.SetShape(edge.Edge())
        self.myAis_shape.Redisplay(True)
