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
        self.myRubberAIS_Shape.SetColor(Quantity_Color(Quantity_NOC_LIGHTPINK1))

    def Action(self):
        self.myBezierCurveAction = BezierCurveAction.Input_1Point

    def MouseInputEvent(self, thePnt2d: gp_Pnt2d, buttons, modifier):
        self.curPnt2d = self.myAnalyserSnap.MouseInput(thePnt2d)

        if self.myBezierCurveAction == BezierCurveAction.Nothing:
            pass
        elif self.myBezierCurveAction == BezierCurveAction.Input_1Point:
            self.myFirstgp_Pnt2d = gp_Pnt2d(self.curPnt2d.X(), self.curPnt2d.Y())
            self.myFirstgp_Pnt = elclib.To3d(self.curCoordinateSystem.Ax2(), self.curPnt2d)
            self.myFirstPoint.SetPnt(self.myFirstgp_Pnt)
            self.myRubberLine.SetPoints(self.myFirstPoint, self.myFirstPoint)

            myGeom2d_Point = Geom2d_CartesianPoint(self.curPnt2d)
            # myAIS_Point = AIS_Point(self.myFirstPoint)
            # self.myContext.Display(myAIS_Point, True)
            self.bezier_curve = Sketch_BezierCurve()
            self.bezier_curve.SetContext(self.myContext)
            self.bezier_curve.SetAxis(self.curCoordinateSystem)
            self.bezier_curve.AddPoles(self.curPnt2d)
            self.bezierNode = BezierNode(self.objectName + str(self.objectCounter), self.rootNode)
            # poleObject = self.AddObject(myGeom2d_Point, myAIS_Point, Sketch_GeometryType.PointSketchObject)
            # poleNode = PointNode("poles" + str(self.IndexCounter), self.bezierNode)
            # poleNode.setSketchObject(poleObject)
            self.myContext.Display(self.myRubberLine, True)

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
            ME = BRepBuilderAPI_MakeEdge(self.myGeom_BezierCurve, self.myFirstgp_Pnt, self.mySecondPoint.Pnt())
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
            self.rootNode.removeChild(self.rootNode.childCount() - 1)
            del self.bezierNode
        elif self.myBezierCurveAction == BezierCurveAction.Input_2Point:
            self.myContext.Remove(self.myRubberLine, True)
            self.rootNode.removeChild(self.rootNode.childCount() - 1)
            del self.bezierNode
        elif self.myBezierCurveAction == BezierCurveAction.Input_OtherPoints:
            self.myGeom2d_BezierCurve.RemovePole(self.IndexCounter)
            self.myGeom_BezierCurve.RemovePole(self.IndexCounter)
            ME = BRepBuilderAPI_MakeEdge(self.myGeom_BezierCurve, self.myFirstgp_Pnt, self.tempPnt)
            if ME.IsDone():
                self.curEdge = ME.Edge()
                self.IndexCounter -= 1
                self.closeBezierCurve()
        self.myBezierCurveAction = BezierCurveAction.Nothing

    def GetTypeOfMethod(self):
        return Sketch_ObjectTypeOfMethod.BezierCurve_Method

    def storePoles(self):
        # myGeom2d_Point = Geom2d_CartesianPoint(self.curPnt2d)
        # self.mySecondPoint.SetPnt(elclib.To3d(self.curCoordinateSystem.Ax2(), self.curPnt2d))
        # myGeom_Point = Geom_CartesianPoint(elclib.To3d(self.curCoordinateSystem.Ax2(), self.curPnt2d))
        # myAIS_Point = AIS_Point(myGeom_Point)
        # self.myContext.Display(myAIS_Point, True)
        #
        # poleObject = self.AddObject(myGeom2d_Point, myAIS_Point, Sketch_GeometryType.PointSketchObject)
        # poleNode = PointNode("poles" + str(self.IndexCounter), self.bezierNode)
        # poleNode.setSketchObject(poleObject)
        self.bezier_curve.AddPoles(self.curPnt2d)

    def closeBezierCurve(self):
        self.myContext.Remove(self.myRubberAIS_Shape, True)
        self.bezier_curve.Compute()
        self.bezierNode.setSketchObject(self.bezier_curve)
        # myGeom2d_BezierCurve: Geom2d_BezierCurve = Geom2d_BezierCurve.DownCast(self.myGeom2d_BezierCurve.Copy())
        # myAIS_Shape = AIS_Shape(self.curEdge)
        # bezierObject = self.AddObject(myGeom2d_BezierCurve, myAIS_Shape, Sketch_GeometryType.CurveSketchObject)
        # self.bezierNode.setSketchObject(bezierObject)
        #
        # self.myContext.Display(myAIS_Shape, True)
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
