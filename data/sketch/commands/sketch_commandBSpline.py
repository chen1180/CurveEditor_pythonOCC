from data.sketch.commands.sketch_command import *
from data.sketch.geometry.geom2d_edge import Geom2d_Edge
from OCC.Core.ElCLib import elclib
from OCC.Core.AIS import AIS_Point
from OCC.Core.Geom2d import Geom2d_CartesianPoint, Geom2d_BSplineCurve
from OCC.Core.Geom import Geom_BSplineCurve
from OCC.Core.GeomAPI import GeomAPI_PointsToBSpline
from enum import Enum
from OCC.Core.TopoDS import TopoDS_Edge
from OCC.Core.TColgp import TColgp_Array1OfPnt2d, TColgp_Array1OfPnt
from OCC.Core.TColStd import TColStd_Array1OfReal, TColStd_Array1OfInteger
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge


class BSplineCurveAction(Enum):
    Nothing = 0
    Input_1Point = 1
    Input_2Point = 2
    Input_OtherPoints = 3


def point_list_to_TColgp_Array1OfPnt(li):
    pts = TColgp_Array1OfPnt(1, len(li))
    for n, i in enumerate(li):
        pts.SetValue(n + 1, i)
    return pts


def point_list_to_TColgp_Array1OfPnt2d(li):
    pts = TColgp_Array1OfPnt2d(1, len(li))
    for n, i in enumerate(li):
        pts.SetValue(n + 1, i)
    return pts


def int_list_to_TColStd_Array1OfInteger(li):
    pts = TColStd_Array1OfInteger(1, len(li))
    for n, i in enumerate(li):
        pts.SetValue(n + 1, i)
    return pts


def float_list_to_TColStd_Array1OfReal(li):
    pts = TColStd_Array1OfReal(1, len(li))
    for n, i in enumerate(li):
        pts.SetValue(n + 1, i)
    return pts


SKETCH_DEGREE = 2
MAXIMUMPOLES = 16


class Sketch_CommandBSpline(Sketch_Command):
    def __init__(self):
        super(Sketch_CommandBSpline, self).__init__("BSplineCurve.")
        self.IndexCounter = 1
        self.myDegree = SKETCH_DEGREE
        self.tempPnt2d = gp.Origin2d()
        self.myFirstgp_Pnt = gp.Origin()
        self.tempPnt = gp.Origin()
        self.curEdge = TopoDS_Edge()

        self.myBSplineCurveAction = BSplineCurveAction.Nothing
        self.Poles2d = [gp.Origin2d()] * 2
        self.Poles = [gp.Origin()] * 2
        self.Multi = [1] * 5
        self.Knots = [float(i) for i in range(5)]

        curgp_Array1CurvePoles2d = point_list_to_TColgp_Array1OfPnt2d(self.Poles2d)
        curgp_Array1CurveMulti = int_list_to_TColStd_Array1OfInteger(self.Multi)
        curgp_Array1CurveKnots = float_list_to_TColStd_Array1OfReal(self.Knots)
        self.myGeom2d_BSplineCurve = Geom2d_BSplineCurve(curgp_Array1CurvePoles2d, curgp_Array1CurveKnots,
                                                         curgp_Array1CurveMulti, self.myDegree)

        curgp_Array1CurvePoles = point_list_to_TColgp_Array1OfPnt(self.Poles)
        self.myGeom_BSplineCurve = Geom_BSplineCurve(curgp_Array1CurvePoles, curgp_Array1CurveKnots,
                                                     curgp_Array1CurveMulti, self.myDegree)

        self.myRubberAIS_Shape = AIS_Shape(self.curEdge)
        self.myRubberAIS_Shape.SetColor(Quantity_Color(Quantity_NOC_LIGHTPINK1))

    def Action(self):
        self.myBSplineCurveAction = BSplineCurveAction.Input_1Point

    def find_new_bspline(self):
        curgp_Array1CurvePoles2d = point_list_to_TColgp_Array1OfPnt2d(self.Poles2d)
        curgp_Array1CurveMulti = int_list_to_TColStd_Array1OfInteger(self.Multi)
        curgp_Array1CurveKnots = float_list_to_TColStd_Array1OfReal(self.Knots)
        self.myGeom2d_BSplineCurve = Geom2d_BSplineCurve(curgp_Array1CurvePoles2d, curgp_Array1CurveKnots,
                                                         curgp_Array1CurveMulti, self.myDegree)
        curgp_Array1CurvePoles = point_list_to_TColgp_Array1OfPnt(self.Poles)
        self.myGeom_BSplineCurve = Geom_BSplineCurve(curgp_Array1CurvePoles, curgp_Array1CurveKnots,
                                                     curgp_Array1CurveMulti, self.myDegree)

    def MouseInputEvent(self, thePnt2d: gp_Pnt2d):
        self.curPnt2d = self.myAnalyserSnap.MouseInput(thePnt2d)

        if self.myBSplineCurveAction == BSplineCurveAction.Nothing:
            pass
        elif self.myBSplineCurveAction == BSplineCurveAction.Input_1Point:
            self.myFirstgp_Pnt2d = gp_Pnt2d(self.curPnt2d.X(), self.curPnt2d.Y())
            self.myFirstgp_Pnt = elclib.To3d(self.curCoordinateSystem.Ax2(), self.curPnt2d)
            self.myFirstPoint.SetPnt(self.myFirstgp_Pnt)
            self.myRubberLine.SetPoints(self.myFirstPoint, self.myFirstPoint)

            self.Poles2d[0]=gp_Pnt2d(self.curPnt2d.X(), self.curPnt2d.Y())
            self.Poles[0]=gp_Pnt(self.myFirstgp_Pnt.X(),self.myFirstgp_Pnt.Y(),self.myFirstgp_Pnt.Z())
            self.find_new_bspline()

            myGeom2d_Point = Geom2d_CartesianPoint(self.curPnt2d)
            myAIS_Point = AIS_Point(self.myFirstPoint)
            self.myContext.Display(myAIS_Point, True)
            self.AddObject(myGeom2d_Point, myAIS_Point, Sketch_GeometryType.PointSketcherObject)

            self.myContext.Display(self.myRubberLine, True)
            self.myBSplineCurveAction = BSplineCurveAction.Input_2Point
            self.IndexCounter = 2

        elif self.myBSplineCurveAction == BSplineCurveAction.Input_2Point:
            self.Poles2d[1] = self.curPnt2d
            self.tempPnt = elclib.To3d(self.curCoordinateSystem.Ax2(), self.curPnt2d)
            self.Poles[1]=self.tempPnt
            self.mySecondPoint.SetPnt(self.tempPnt)
            self.find_new_bspline()

            ME = BRepBuilderAPI_MakeEdge(self.myFirstgp_Pnt, self.tempPnt)
            if ME.IsDone():
                self.storePoles()
                self.curEdge = ME.Edge()
                self.myRubberAIS_Shape.Set(self.curEdge)
                self.myContext.Remove(self.myRubberLine, True)
                self.myContext.Display(self.myRubberAIS_Shape, True)

                self.IndexCounter += 1

                self.Poles2d.append(self.curPnt2d)
                self.Multi.append(1)
                self.Knots.append(float(len(self.Multi) - 1))
                self.Poles.append(self.tempPnt)
                self.find_new_bspline()

                self.myBSplineCurveAction = BSplineCurveAction.Input_OtherPoints
        elif self.myBSplineCurveAction == BSplineCurveAction.Input_OtherPoints:
            self.Poles2d[self.IndexCounter-1] = self.curPnt2d
            self.tempPnt = elclib.To3d(self.curCoordinateSystem.Ax2(), self.curPnt2d)
            self.Poles[self.IndexCounter-1] = self.tempPnt
            self.find_new_bspline()

            self.mySecondPoint.SetPnt(self.tempPnt)
            ME = BRepBuilderAPI_MakeEdge(self.myGeom_BSplineCurve)
            if ME.IsDone():
                self.storePoles()
                self.curEdge = ME.Edge()
                if self.IndexCounter > MAXIMUMPOLES:
                    self.closeBSpline()
                else:
                    self.myRubberAIS_Shape.Set(self.curEdge)
                    self.myContext.Redisplay(self.myRubberAIS_Shape, True)

                    self.Poles2d.append(self.curPnt2d)
                    self.Multi.append(1)
                    self.Knots.append(float(len(self.Multi) - 1))
                    self.Poles.append(self.tempPnt)
                    self.find_new_bspline()
                    self.tempPnt2d = gp_Pnt2d(self.curPnt2d.X(), self.curPnt2d.Y())
                    self.IndexCounter += 1
        return False

    def MouseMoveEvent(self, thePnt2d: gp_Pnt2d):
        self.curPnt2d = self.myAnalyserSnap.MouseMove(thePnt2d)
        if self.myBSplineCurveAction == BSplineCurveAction.Nothing:
            pass
        elif self.myBSplineCurveAction == BSplineCurveAction.Input_1Point:
            pass
        elif self.myBSplineCurveAction == BSplineCurveAction.Input_2Point:
            self.mySecondPoint.SetPnt(elclib.To3d(self.curCoordinateSystem.Ax2(), self.curPnt2d))
            self.myRubberLine.SetPoints(self.myFirstPoint, self.mySecondPoint)
            self.myContext.Redisplay(self.myRubberLine, True)
        elif self.myBSplineCurveAction == BSplineCurveAction.Input_OtherPoints:
            self.myGeom2d_BSplineCurve.SetPole(self.IndexCounter, self.curPnt2d)
            self.mySecondPoint.SetPnt(elclib.To3d(self.curCoordinateSystem.Ax2(), self.curPnt2d))
            self.myGeom_BSplineCurve.SetPole(self.IndexCounter, self.mySecondPoint.Pnt())
            ME = BRepBuilderAPI_MakeEdge(self.myGeom_BSplineCurve)
            if ME.IsDone():
                self.curEdge = ME.Edge()
                self.myRubberAIS_Shape.Set(self.curEdge)
                self.myContext.Redisplay(self.myRubberAIS_Shape, True)
            else:
                self.IndexCounter -= 1

    def CancelEvent(self):
        if self.myBSplineCurveAction == BSplineCurveAction.Nothing:
            pass
        elif self.myBSplineCurveAction == BSplineCurveAction.Input_1Point:
            pass
        elif self.myBSplineCurveAction == BSplineCurveAction.Input_2Point:
            self.myContext.Remove(self.myRubberLine,True)
        elif self.myBSplineCurveAction == BSplineCurveAction.Input_OtherPoints:
            ME = BRepBuilderAPI_MakeEdge(self.myGeom_BSplineCurve)
            if ME.IsDone():
                self.curEdge = ME.Edge()
                self.IndexCounter -= 1
                self.closeBSpline()
        self.myBSplineCurveAction = BSplineCurveAction.Nothing

    def GetTypeOfMethod(self):
        return Sketch_ObjectTypeOfMethod.BSpline_Method

    def storePoles(self):
        myGeom2d_Point = Geom2d_CartesianPoint(self.curPnt2d)
        self.mySecondPoint.SetPnt(elclib.To3d(self.curCoordinateSystem.Ax2(), self.curPnt2d))
        myAIS_Point = AIS_Point(self.mySecondPoint)
        self.myContext.Display(myAIS_Point, True)
        self.AddObject(myGeom2d_Point, myAIS_Point, Sketch_GeometryType.PointSketcherObject)

    def closeBSpline(self):
        self.myContext.Remove(self.myRubberAIS_Shape, True)
        myAIS_Shape = AIS_Shape(self.curEdge)
        self.AddObject(self.myGeom2d_BSplineCurve.Copy(), myAIS_Shape, Sketch_GeometryType.CurveSketcherObject)
        self.myContext.Display(myAIS_Shape, True)

        self.Poles2d = [gp.Origin2d()] * 2
        self.Poles = [gp.Origin()] * 2
        self.Multi = [1] * 5
        self.Knots = [float(i) for i in range(5)]
        self.myBSplineCurveAction = BSplineCurveAction.Input_1Point
