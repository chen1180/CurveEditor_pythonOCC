from data.sketch.commands.sketch_command import *
from data.sketch.geometry.geom2d_edge import *
from OCC.Core.ElCLib import elclib
from OCC.Core.AIS import AIS_Point
from OCC.Core.Geom2d import Geom2d_CartesianPoint, Geom2d_BezierCurve
from OCC.Core.Geom import Geom_CartesianPoint, Geom_BezierCurve
from enum import Enum
from OCC.Core.TopoDS import TopoDS_Edge
from OCC.Core.TColgp import TColgp_Array1OfPnt2d, TColgp_Array1OfPnt
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge

MAXIMUMPOLES = 16


class BezierCurveAction(Enum):
    Nothing = 0
    Input_1Point = 1
    Input_2Point = 2
    Input_OtherPoints = 3


class Sketch_CommandBezierCurve(Sketch_Command):
    def __init__(self):
        super(Sketch_CommandBezierCurve, self).__init__("BezierCurve.")
        self.IndexCounter = 0
        self.tempPnt2d = gp_Pnt2d(gp.Origin2d())
        self.myFirstgp_Pnt = gp_Pnt(gp.Origin())
        self.tempPnt = gp_Pnt(gp.Origin())
        self.curEdge = TopoDS_Edge()

        self.myBezierCurveAction = BezierCurveAction.Nothing
        curgp_Array1CurvePoles2d = TColgp_Array1OfPnt2d(1, 2)
        curgp_Array1CurvePoles2d.SetValue(1, self.myFirstgp_Pnt2d)
        curgp_Array1CurvePoles2d.SetValue(2, self.tempPnt2d)
        self.myGeom2d_BezierCurve = Geom2d_BezierCurve(curgp_Array1CurvePoles2d)

        curgp_Array1CurvePoles = TColgp_Array1OfPnt(1, 2)
        curgp_Array1CurvePoles.SetValue(1, self.myFirstgp_Pnt)
        curgp_Array1CurvePoles.SetValue(2, self.tempPnt)
        self.myGeom_BezierCurve = Geom_BezierCurve(curgp_Array1CurvePoles)

        self.myRubberAIS_Shape = AIS_Shape(self.curEdge)

    def Action(self):
        self.myBezierCurveAction = BezierCurveAction.Input_1Point

    def MouseInputEvent(self, thePnt2d: gp_Pnt2d):
        self.curPnt2d = self.myAnalyserSnap.MouseInput(thePnt2d)

        if self.myBezierCurveAction == BezierCurveAction.Nothing:
            pass
        elif self.myBezierCurveAction == BezierCurveAction.Input_1Point:
            self.myFirstgp_Pnt2d = self.curPnt2d
            self.myFirstgp_Pnt = elclib.To3d(self.curCoordinateSystem.Ax2(), self.curPnt2d)
            self.myFirstPoint.SetPnt(self.myFirstgp_Pnt)
            self.myRubberLine.SetPoints(self.myFirstgp_Pnt, self.myFirstgp_Pnt)

            myGeom2d_Point = Geom2d_CartesianPoint(self.curPnt2d)
            myAIS_Point = AIS_Point(myGeom2d_Point)
            self.myContext.Display(myAIS_Point, True)
            self.AddObject(myGeom2d_Point, myAIS_Point, Sketch_GeometryType.PointSketcherObject)

            self.myContext.Display(self.myRubberLine, False)
            self.myBezierCurveAction = BezierCurveAction.Input_2Point
            self.IndexCounter = 2

        elif self.myBezierCurveAction == BezierCurveAction.Input_2Point:
            self.myGeom2d_BezierCurve.SetPole(1, self.myFirstgp_Pnt2d)
            self.myGeom2d_BezierCurve.SetPole(self.IndexCounter, self.curPnt2d)

            self.tempPnt = elclib.To3d(self.curCoordinateSystem.Ax2(), self.curPnt2d)
            self.myGeom_BezierCurve.SetPole(1, self.myFirstgp_Pnt)
            self.myGeom_BezierCurve.SetPole(self.IndexCounter, self.tempPnt)

            self.mySecondPoint.SetPnt(self.tempPnt)
            ME = BRepBuilderAPI_MakeEdge(self.myGeom_BezierCurve, self.myFirstgp_Pnt, self.tempPnt)
            if ME.IsDone():
                self.storePoles()
                self.curEdge = ME.Edge()
                self.myRubberAIS_Shape.Set(self.curEdge)
                self.myContext.Remove(self.myRubberLine, True)
                self.myContext.Display(self.myRubberAIS_Shape, False)

                self.myGeom2d_BezierCurve.InsertPoleAfter(self.IndexCounter, self.curPnt2d)
                self.myGeom_BezierCurve.InsertPoleAfter(self.IndexCounter, self.tempPnt)

                self.IndexCounter += 1
                self.myBezierCurveAction = BezierCurveAction.Input_OtherPoints
        elif self.myBezierCurveAction == BezierCurveAction.Input_OtherPoints:
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
                    self.myContext.Redisplay(self.myRubberAIS_Shape)

                    self.myGeom2d_BezierCurve.InsertPoleAfter(self.IndexCounter, self.curPnt2d)
                    self.myGeom_BezierCurve.InsertPoleAfter(self.IndexCounter, self.tempPnt)
                    self.tempPnt2d=self.curPnt2d
                    self.IndexCounter += 1
        return False
    def MouseMoveEvent(self, thePnt2d: gp_Pnt2d):
        self.curPnt2d = self.myAnalyserSnap.MouseInput(thePnt2d)
        if self.myBezierCurveAction == BezierCurveAction.Nothing:
            pass
        elif self.myBezierCurveAction == BezierCurveAction.Input_1Point:
            pass
        elif self.myBezierCurveAction == BezierCurveAction.Input_2Point:
            self.mySecondPoint = elclib.To3d(self.curCoordinateSystem.Ax2(), self.curPnt2d)
            


        elif self.myBezierCurveAction == BezierCurveAction.Input_OtherPoints:
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
                    self.myContext.Redisplay(self.myRubberAIS_Shape)

                    self.myGeom2d_BezierCurve.InsertPoleAfter(self.IndexCounter, self.curPnt2d)
                    self.myGeom_BezierCurve.InsertPoleAfter(self.IndexCounter, self.tempPnt)
                    self.tempPnt2d=self.curPnt2d
                    self.IndexCounter += 1
        return False

    def storePoles(self):
        myGeom2d_Point = Geom2d_CartesianPoint(self.curPnt2d)
        self.mySecondPoint.SetPnt(elclib.To3d(self.curCoordinateSystem.Ax2(), self.curPnt2d))
        myAIS_Point = AIS_Point(self.mySecondPoint)
        self.myContext.Display(myAIS_Point, True)
        self.AddObject(myGeom2d_Point, myAIS_Point, Sketch_GeometryType.PointSketcherObject)

    def closeBezierCurve(self):
        self.myContext.Remove(self.myRubberAIS_Shape)
        myAIS_Shape = AIS_Shape(self.curEdge)
        self.AddObject(self.myGeom2d_BezierCurve, myAIS_Shape, Sketch_GeometryType.CurveSketcherObject)

        self.myContext.Display(myAIS_Shape, True)
        for idx in range(self.IndexCounter, 2, -1):
            self.myGeom2d_BezierCurve.RemovePole(idx)
            self.myGeom_BezierCurve.RemovePole(idx)
        self.myBezierCurveAction = BezierCurveAction.Input_1Point
