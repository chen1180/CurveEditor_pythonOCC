from data.sketch.commands.sketch_command import *
from data.sketch.geometry.geom2d_edge import Geom2d_Edge
from OCC.Core.ElCLib import elclib
from OCC.Core.AIS import AIS_Point
from OCC.Core.Geom2d import Geom2d_CartesianPoint, Geom2d_BezierCurve
from OCC.Core.Geom import Geom_BezierCurve
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
        self.IndexCounter = 1
        self.tempPnt2d = gp.Origin2d()
        self.myFirstgp_Pnt = gp.Origin()
        self.tempPnt = gp.Origin()
        self.curEdge = TopoDS_Edge()

        self.myBezierCurveAction = BezierCurveAction.Nothing
        curgp_Array1CurvePoles2d = TColgp_Array1OfPnt2d(1, 2)
        curgp_Array1CurvePoles2d.SetValue(1, gp.Origin2d())
        curgp_Array1CurvePoles2d.SetValue(2, gp.Origin2d())
        self.myGeom2d_BezierCurve = Geom2d_BezierCurve(curgp_Array1CurvePoles2d)

        curgp_Array1CurvePoles = TColgp_Array1OfPnt(1, 2)
        curgp_Array1CurvePoles.SetValue(1, gp.Origin())
        curgp_Array1CurvePoles.SetValue(2, gp.Origin())
        self.myGeom_BezierCurve = Geom_BezierCurve(curgp_Array1CurvePoles)

        self.myRubberAIS_Shape = AIS_Shape(self.curEdge)

    def Action(self):
        self.myBezierCurveAction = BezierCurveAction.Input_1Point

    def MouseInputEvent(self, thePnt2d: gp_Pnt2d, buttons, modifier):
        self.curPnt2d = self.myAnalyserSnap.MouseInput(thePnt2d)

        if self.myBezierCurveAction == BezierCurveAction.Nothing:
            pass
        elif self.myBezierCurveAction == BezierCurveAction.Input_1Point:
            # calculate first 2d and 3d point
            self.myFirstgp_Pnt2d = gp_Pnt2d(self.curPnt2d.X(), self.curPnt2d.Y())
            self.myFirstgp_Pnt = elclib.To3d(self.curCoordinateSystem.Ax2(), self.curPnt2d)
            # save first point
            self.myFirstPoint.SetPnt(self.myFirstgp_Pnt)
            # draw first point
            self.myRubberLine.SetPoints(self.myFirstPoint, self.myFirstPoint)
            # initialize bezier curve data structure created in sketch geometry
            self.bezier_curve = Sketch_BezierCurve(self.myContext, self.curCoordinateSystem)
            # render the first point and auxiliry line
            self.bezier_curve.AddPoles(self.curPnt2d)
            # render the rubber line
            self.myContext.Display(self.myRubberLine, True)
            # ready for 2nd point input
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
                self.bezier_curve.AddPoles(self.curPnt2d)
                self.curEdge = ME.Edge()
                self.myRubberAIS_Shape.Set(self.curEdge)
                self.myContext.Remove(self.myRubberLine, True)
                self.myContext.Display(self.myRubberAIS_Shape, True)

                self.myGeom2d_BezierCurve.InsertPoleAfter(self.IndexCounter, self.curPnt2d)
                self.myGeom_BezierCurve.InsertPoleAfter(self.IndexCounter, self.tempPnt)

                self.IndexCounter += 1
                self.myBezierCurveAction = BezierCurveAction.Input_OtherPoints
        elif self.myBezierCurveAction == BezierCurveAction.Input_OtherPoints:
            self.myGeom2d_BezierCurve.SetPole(self.IndexCounter, self.curPnt2d)

            self.tempPnt = elclib.To3d(self.curCoordinateSystem.Ax2(), self.curPnt2d)
            self.myGeom_BezierCurve.SetPole(self.IndexCounter, self.tempPnt)

            self.mySecondPoint.SetPnt(self.tempPnt)
            ME = BRepBuilderAPI_MakeEdge(self.myGeom_BezierCurve)
            if ME.IsDone():
                self.bezier_curve.AddPoles(self.curPnt2d)
                self.curEdge = ME.Edge()
                if self.IndexCounter > MAXIMUMPOLES:
                    self.CloseBezierCurve()
                else:
                    self.myRubberAIS_Shape.Set(self.curEdge)
                    self.myContext.Redisplay(self.myRubberAIS_Shape, True)

                    self.myGeom2d_BezierCurve.InsertPoleAfter(self.IndexCounter, self.curPnt2d)
                    self.myGeom_BezierCurve.InsertPoleAfter(self.IndexCounter, self.tempPnt)
                    self.tempPnt2d = gp_Pnt2d(self.curPnt2d.X(), self.curPnt2d.Y())
                    self.IndexCounter += 1
        return False

    def MouseMoveEvent(self, thePnt2d: gp_Pnt2d, buttons, modifiers):
        self.curPnt2d = self.myAnalyserSnap.MouseMove(thePnt2d)
        if self.myBezierCurveAction == BezierCurveAction.Nothing:
            pass
        elif self.myBezierCurveAction == BezierCurveAction.Input_1Point:
            pass
        elif self.myBezierCurveAction == BezierCurveAction.Input_2Point:
            self.mySecondPoint.SetPnt(elclib.To3d(self.curCoordinateSystem.Ax2(), self.curPnt2d))
            self.myRubberLine.SetPoints(self.myFirstPoint, self.mySecondPoint)
            self.myContext.Redisplay(self.myRubberLine, True)
        elif self.myBezierCurveAction == BezierCurveAction.Input_OtherPoints:
            self.myGeom2d_BezierCurve.SetPole(self.IndexCounter, self.curPnt2d)
            self.mySecondPoint.SetPnt(elclib.To3d(self.curCoordinateSystem.Ax2(), self.curPnt2d))
            self.myGeom_BezierCurve.SetPole(self.IndexCounter, self.mySecondPoint.Pnt())
            ME = BRepBuilderAPI_MakeEdge(self.myGeom_BezierCurve)
            if ME.IsDone():
                self.curEdge = ME.Edge()
                self.myRubberAIS_Shape.Set(self.curEdge)
                self.myContext.Redisplay(self.myRubberAIS_Shape, True)
            else:
                self.IndexCounter -= 1

    def CancelEvent(self):
        if self.myBezierCurveAction == BezierCurveAction.Nothing:
            pass
        elif self.myBezierCurveAction == BezierCurveAction.Input_1Point:
            pass
        elif self.myBezierCurveAction == BezierCurveAction.Input_2Point:
            self.rootNode.removeChild(self.rootNode.childCount() - 1)
            self.myContext.Remove(self.myRubberLine, True)
            self.bezier_curve.RemoveLabel()
        elif self.myBezierCurveAction == BezierCurveAction.Input_OtherPoints:
            self.myGeom2d_BezierCurve.RemovePole(self.IndexCounter)
            self.myGeom_BezierCurve.RemovePole(self.IndexCounter)
            ME = BRepBuilderAPI_MakeEdge(self.myGeom_BezierCurve, self.myFirstgp_Pnt, self.tempPnt)
            if ME.IsDone():
                self.curEdge = ME.Edge()
                self.IndexCounter -= 1
                self.CloseBezierCurve()
        self.myBezierCurveAction = BezierCurveAction.Nothing

    def GetTypeOfMethod(self):
        return Sketch_ObjectTypeOfMethod.BezierCurve_Method

    def CloseBezierCurve(self):
        self.myContext.Remove(self.myRubberAIS_Shape, True)
        self.bezier_curve.Compute()
        self.bezierNode = BezierNode(self.bezier_curve.GetName(), self.rootNode)
        self.bezierNode.setSketchObject(self.bezier_curve)
        self.AddObject(self.bezier_curve.GetGeometry2d(), self.bezier_curve.GetAIS_Object(),
                       Sketch_GeometryType.CurveSketchObject)
        # create new object
        curgp_Array1CurvePoles2d = TColgp_Array1OfPnt2d(1, 2)
        curgp_Array1CurvePoles2d.SetValue(1, gp.Origin2d())
        curgp_Array1CurvePoles2d.SetValue(2, gp.Origin2d())
        self.myGeom2d_BezierCurve = Geom2d_BezierCurve(curgp_Array1CurvePoles2d)
        curgp_Array1CurvePoles = TColgp_Array1OfPnt(1, 2)
        curgp_Array1CurvePoles.SetValue(1, gp.Origin())
        curgp_Array1CurvePoles.SetValue(2, gp.Origin())
        self.myGeom_BezierCurve = Geom_BezierCurve(curgp_Array1CurvePoles)
        self.IndexCounter = 1
        self.myBezierCurveAction = BezierCurveAction.Input_1Point
