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


SKETCH_DEGREE = 2


class Sketch_CommandPointToBSpline(Sketch_Command):
    def __init__(self):
        super(Sketch_CommandPointToBSpline, self).__init__("BSplineCurve.")
        self.IndexCounter = 1
        self.myDegree = SKETCH_DEGREE
        self.tempPnt2d = gp.Origin2d()
        self.myFirstgp_Pnt = gp.Origin()
        self.tempPnt = gp.Origin()
        self.curEdge = TopoDS_Edge()

        self.myBSplineCurveAction = BSplineCurveAction.Nothing
        curgp_Array1CurvePoles2d = TColgp_Array1OfPnt2d(1, 3)
        curgp_Array1CurvePoles2d.SetValue(1, self.myFirstgp_Pnt2d)
        curgp_Array1CurvePoles2d.SetValue(2, self.tempPnt2d)
        curgp_Array1CurvePoles2d.SetValue(3, gp.Origin2d())

        curgp_Array1CurveMulti = TColStd_Array1OfInteger(1, 6)
        curgp_Array1CurveMulti.SetValue(1, 1)
        curgp_Array1CurveMulti.SetValue(2, 1)
        curgp_Array1CurveMulti.SetValue(3, 1)
        curgp_Array1CurveMulti.SetValue(4, 1)
        curgp_Array1CurveMulti.SetValue(5, 1)
        curgp_Array1CurveMulti.SetValue(6, 1)

        curgp_Array1CurveKnots = TColStd_Array1OfReal(1, 6)
        curgp_Array1CurveKnots.SetValue(1, 1)
        curgp_Array1CurveKnots.SetValue(2, 1)
        curgp_Array1CurveKnots.SetValue(3, 1)
        curgp_Array1CurveKnots.SetValue(4, 1)
        curgp_Array1CurveKnots.SetValue(5, 1)
        curgp_Array1CurveKnots.SetValue(6, 1)

        self.myGeom2d_BSplineCurve = Geom2d_BSplineCurve(curgp_Array1CurvePoles2d, curgp_Array1CurveKnots,
                                                         curgp_Array1CurveMulti, self.myDegree)

        curgp_Array1CurvePoles = TColgp_Array1OfPnt(1, 3)
        curgp_Array1CurvePoles.SetValue(1, self.myFirstgp_Pnt)
        curgp_Array1CurvePoles.SetValue(2, self.tempPnt)
        curgp_Array1CurvePoles.SetValue(3, gp.Origin())

        self.myGeom_BSplineCurve = Geom_BSplineCurve(curgp_Array1CurvePoles2d, curgp_Array1CurveKnots,
                                                     curgp_Array1CurveMulti, self.myDegree)

        self.myRubberAIS_Shape = AIS_Shape(self.curEdge)
        self.myRubberAIS_Shape.SetColor(Quantity_Color(Quantity_NOC_LIGHTPINK1))

    def Action(self):
        self.myBSplineCurveAction = BSplineCurveAction.Input_1Point

    def MouseInputEvent(self, thePnt2d: gp_Pnt2d):
        self.curPnt2d = self.myAnalyserSnap.MouseInput(thePnt2d)

        if self.myBSplineCurveAction == BSplineCurveAction.Nothing:
            pass
        elif self.myBSplineCurveAction == BSplineCurveAction.Input_1Point:
            self.myFirstgp_Pnt2d = gp_Pnt2d(self.curPnt2d.X(), self.curPnt2d.Y())
            self.myFirstgp_Pnt = elclib.To3d(self.curCoordinateSystem.Ax2(), self.curPnt2d)
            self.myFirstPoint.SetPnt(self.myFirstgp_Pnt)
            self.myRubberLine.SetPoints(self.myFirstPoint, self.myFirstPoint)

            myGeom2d_Point = Geom2d_CartesianPoint(self.curPnt2d)
            myAIS_Point = AIS_Point(self.myFirstPoint)
            self.myContext.Display(myAIS_Point, True)
            self.AddObject(myGeom2d_Point, myAIS_Point, Sketch_GeometryType.PointSketcherObject)

            self.myContext.Display(self.myRubberLine, True)
            self.myBSplineCurveAction = BSplineCurveAction.Input_2Point
            self.IndexCounter = 2

        elif self.myBSplineCurveAction == BSplineCurveAction.Input_2Point:
            self.myGeom2d_BSplineCurve.SetPole(1, self.myFirstgp_Pnt2d)
            self.myGeom2d_BSplineCurve.SetPole(self.IndexCounter, self.curPnt2d)

            self.tempPnt = elclib.To3d(self.curCoordinateSystem.Ax2(), self.curPnt2d)
            self.myGeom_BSplineCurve.SetPole(1, self.myFirstgp_Pnt)
            self.myGeom_BSplineCurve.SetPole(self.IndexCounter, self.tempPnt)

            self.mySecondPoint.SetPnt(self.tempPnt)
            ME = BRepBuilderAPI_MakeEdge(self.myGeom_BezierCurve, self.myFirstgp_Pnt, self.tempPnt)
            if ME.IsDone():
                self.storePoles()
                self.curEdge = ME.Edge()
                self.myRubberAIS_Shape.Set(self.curEdge)
                self.myContext.Remove(self.myRubberLine, True)
                self.myContext.Display(self.myRubberAIS_Shape, True)

                self.myGeom2d_BezierCurve.InsertPoleAfter(self.IndexCounter, self.curPnt2d)
                self.myGeom_BezierCurve.InsertPoleAfter(self.IndexCounter, self.tempPnt)

                self.IndexCounter += 1
                self.myBSplineCurveAction = BSplineCurveAction.Input_OtherPoints
        elif self.myBSplineCurveAction == BSplineCurveAction.Input_OtherPoints:
            self.myGeom2d_BezierCurve.SetPole(self.IndexCounter, self.curPnt2d)

            self.tempPnt = elclib.To3d(self.curCoordinateSystem.Ax2(), self.curPnt2d)
            self.myGeom_BezierCurve.SetPole(self.IndexCounter, self.tempPnt)

            self.mySecondPoint.SetPnt(self.tempPnt)
            ME = BRepBuilderAPI_MakeEdge(self.myGeom_BezierCurve, self.myFirstgp_Pnt, self.tempPnt)
            if ME.IsDone():
                self.storePoles()
                self.curEdge = ME.Edge()
                if self.IndexCounter > MAXIMUMPOLES:
                    self.closeBezierCurve()
                else:
                    self.myRubberAIS_Shape.Set(self.curEdge)
                    self.myContext.Redisplay(self.myRubberAIS_Shape, True)

                    self.myGeom2d_BezierCurve.InsertPoleAfter(self.IndexCounter, self.curPnt2d)
                    self.myGeom_BezierCurve.InsertPoleAfter(self.IndexCounter, self.tempPnt)
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
            self.myGeom2d_BezierCurve.SetPole(self.IndexCounter, self.curPnt2d)
            self.mySecondPoint.SetPnt(elclib.To3d(self.curCoordinateSystem.Ax2(), self.curPnt2d))
            self.myGeom_BezierCurve.SetPole(self.IndexCounter, self.mySecondPoint.Pnt())
            ME = BRepBuilderAPI_MakeEdge(self.myGeom_BezierCurve, self.myFirstgp_Pnt, self.mySecondPoint.Pnt())
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
            self.myContext.Remove(self.myRubberLine)
        elif self.myBSplineCurveAction == BSplineCurveAction.Input_OtherPoints:
            self.myGeom2d_BezierCurve.RemovePole(self.IndexCounter)
            self.myGeom_BezierCurve.RemovePole(self.IndexCounter)
            ME = BRepBuilderAPI_MakeEdge(self.myGeom_BezierCurve, self.myFirstgp_Pnt, self.tempPnt)
            if ME.IsDone():
                self.curEdge = ME.Edge()
                self.IndexCounter -= 1
                self.closeBezierCurve()
        self.myBSplineCurveAction = BSplineCurveAction.Nothing

    def GetTypeOfMethod(self):
        return Sketch_ObjectTypeOfMethod.BezierCurve_Method

    def storePoles(self):
        myGeom2d_Point = Geom2d_CartesianPoint(self.curPnt2d)
        self.mySecondPoint.SetPnt(elclib.To3d(self.curCoordinateSystem.Ax2(), self.curPnt2d))
        myAIS_Point = AIS_Point(self.mySecondPoint)
        self.myContext.Display(myAIS_Point, True)
        self.AddObject(myGeom2d_Point, myAIS_Point, Sketch_GeometryType.PointSketcherObject)

    def closeBezierCurve(self):
        self.myContext.Remove(self.myRubberAIS_Shape, True)
        myAIS_Shape = AIS_Shape(self.curEdge)
        self.AddObject(self.myGeom2d_BezierCurve, myAIS_Shape, Sketch_GeometryType.CurveSketcherObject)
        self.myContext.Display(myAIS_Shape, True)
        for idx in range(self.IndexCounter, 2, -1):
            self.myGeom2d_BezierCurve.RemovePole(idx)
            self.myGeom_BezierCurve.RemovePole(idx)
        self.myBSplineCurveAction = BSplineCurveAction.Input_1Point
