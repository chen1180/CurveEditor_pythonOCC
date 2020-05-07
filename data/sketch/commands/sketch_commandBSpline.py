from data.sketch.commands.sketch_command import *
from data.sketch.geometry.geom2d_edge import Geom2d_Edge
from OCC.Core.ElCLib import elclib
from OCC.Core.AIS import AIS_Point
from OCC.Core.Geom2d import Geom2d_CartesianPoint, Geom2d_BSplineCurve
from OCC.Core.Geom import Geom_BSplineCurve
from enum import Enum
from OCC.Core.TopoDS import TopoDS_Edge

from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge

SKETCH_DEGREE = 2
MAXIMUMPOLES = 16


class BSplineCurveAction(Enum):
    Nothing = 0
    Input_1Point = 1
    Input_2Point = 2
    Input_OtherPoints = 3


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
        self.Multi, self.Knots = setQuasiUniformKnots(len(self.Poles), self.myDegree)

        curgp_Array1CurvePoles2d = point_list_to_TColgp_Array1OfPnt2d(self.Poles2d)
        curgp_Array1CurveMulti = int_list_to_TColStd_Array1OfInteger(self.Multi)
        curgp_Array1CurveKnots = float_list_to_TColStd_Array1OfReal(self.Knots)
        self.myGeom2d_BSplineCurve = Geom2d_BSplineCurve(curgp_Array1CurvePoles2d, curgp_Array1CurveKnots,
                                                         curgp_Array1CurveMulti, self.myDegree)

        curgp_Array1CurvePoles = point_list_to_TColgp_Array1OfPnt(self.Poles)
        self.myGeom_BSplineCurve = Geom_BSplineCurve(curgp_Array1CurvePoles, curgp_Array1CurveKnots,
                                                     curgp_Array1CurveMulti, self.myDegree)

        self.myRubberAIS_Shape = AIS_Shape(self.curEdge)

    def Action(self):
        self.myBSplineCurveAction = BSplineCurveAction.Input_1Point

    def CreateBspline(self):
        curgp_Array1CurvePoles2d = point_list_to_TColgp_Array1OfPnt2d(self.Poles2d)
        curgp_Array1CurveMulti = int_list_to_TColStd_Array1OfInteger(self.Multi)
        curgp_Array1CurveKnots = float_list_to_TColStd_Array1OfReal(self.Knots)
        self.myGeom2d_BSplineCurve = Geom2d_BSplineCurve(curgp_Array1CurvePoles2d, curgp_Array1CurveKnots,
                                                         curgp_Array1CurveMulti, self.myDegree)
        curgp_Array1CurvePoles = point_list_to_TColgp_Array1OfPnt(self.Poles)
        self.myGeom_BSplineCurve = Geom_BSplineCurve(curgp_Array1CurvePoles, curgp_Array1CurveKnots,
                                                     curgp_Array1CurveMulti, self.myDegree)

    def MouseInputEvent(self, thePnt2d: gp_Pnt2d, buttons, modifier):
        self.curPnt2d = self.myAnalyserSnap.MouseInput(thePnt2d)

        if self.myBSplineCurveAction == BSplineCurveAction.Nothing:
            pass
        elif self.myBSplineCurveAction == BSplineCurveAction.Input_1Point:
            self.myFirstgp_Pnt2d = gp_Pnt2d(self.curPnt2d.X(), self.curPnt2d.Y())
            self.myFirstgp_Pnt = elclib.To3d(self.curCoordinateSystem.Ax2(), self.curPnt2d)
            self.myFirstPoint.SetPnt(self.myFirstgp_Pnt)
            # self.myRubberLine.SetPoints(self.myFirstPoint, self.myFirstPoint)

            self.Poles2d[0] = gp_Pnt2d(self.curPnt2d.X(), self.curPnt2d.Y())
            self.Poles[0] = gp_Pnt(self.myFirstgp_Pnt.X(), self.myFirstgp_Pnt.Y(), self.myFirstgp_Pnt.Z())
            self.CreateBspline()

            self.bspline = Sketch_Bspline(self.myContext, self.curCoordinateSystem)
            self.bspline.AddPoles(self.curPnt2d)

            # self.myContext.Display(self.myRubberLine, True)
            self.myBSplineCurveAction = BSplineCurveAction.Input_2Point
            self.IndexCounter = 2

        elif self.myBSplineCurveAction == BSplineCurveAction.Input_2Point:
            self.Poles2d[1] = gp_Pnt2d(self.curPnt2d.X(), self.curPnt2d.Y())
            self.tempPnt = elclib.To3d(self.curCoordinateSystem.Ax2(), self.curPnt2d)
            self.Poles[1] = gp_Pnt(self.tempPnt.X(), self.tempPnt.Y(), self.tempPnt.Z())
            self.mySecondPoint.SetPnt(self.tempPnt)
            self.CreateBspline()

            ME = BRepBuilderAPI_MakeEdge(self.myFirstgp_Pnt, self.mySecondPoint.Pnt())
            if ME.IsDone():
                self.bspline.AddPoles(self.curPnt2d)
                self.curEdge = ME.Edge()
                self.myRubberAIS_Shape.Set(self.curEdge)
                # self.myContext.Remove(self.myRubberLine, True)
                self.myContext.Display(self.myRubberAIS_Shape, True)

                self.IndexCounter += 1

                self.Poles2d.append(self.curPnt2d)
                self.Poles.append(self.tempPnt)
                self.Multi, self.Knots = setQuasiUniformKnots(len(self.Poles), self.myDegree)
                self.CreateBspline()

                self.myBSplineCurveAction = BSplineCurveAction.Input_OtherPoints
        elif self.myBSplineCurveAction == BSplineCurveAction.Input_OtherPoints:
            self.Poles2d[self.IndexCounter - 1] = gp_Pnt2d(self.curPnt2d.X(), self.curPnt2d.Y())
            self.tempPnt = elclib.To3d(self.curCoordinateSystem.Ax2(), self.curPnt2d)
            self.Poles[self.IndexCounter - 1] = gp_Pnt(self.tempPnt.X(), self.tempPnt.Y(), self.tempPnt.Z())
            self.CreateBspline()

            self.mySecondPoint.SetPnt(self.tempPnt)
            ME = BRepBuilderAPI_MakeEdge(self.myGeom_BSplineCurve)
            if ME.IsDone():
                self.bspline.AddPoles(self.curPnt2d)
                self.curEdge = ME.Edge()
                if self.IndexCounter > MAXIMUMPOLES:
                    self.closeBSpline()
                else:
                    self.myRubberAIS_Shape.Set(self.curEdge)
                    self.myContext.Redisplay(self.myRubberAIS_Shape, True)

                    self.Poles2d.append(self.curPnt2d)
                    self.Poles.append(self.tempPnt)
                    self.Multi, self.Knots = setQuasiUniformKnots(len(self.Poles), self.myDegree)
                    self.CreateBspline()
                    self.tempPnt2d = gp_Pnt2d(self.curPnt2d.X(), self.curPnt2d.Y())
                    self.IndexCounter += 1
        return False

    def MouseMoveEvent(self, thePnt2d: gp_Pnt2d, buttons, modifiers):
        self.curPnt2d = self.myAnalyserSnap.MouseMove(thePnt2d)
        if self.myBSplineCurveAction == BSplineCurveAction.Nothing:
            pass
        elif self.myBSplineCurveAction == BSplineCurveAction.Input_1Point:
            pass
        elif self.myBSplineCurveAction == BSplineCurveAction.Input_2Point:
            # self.mySecondPoint.SetPnt(elclib.To3d(self.curCoordinateSystem.Ax2(), self.curPnt2d))
            # self.myRubberLine.SetPoints(self.myFirstPoint, self.mySecondPoint)
            # self.myContext.Redisplay(self.myRubberLine, True)
            pass
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
            self.bspline.RemoveLabel()
            del self.bspline
        elif self.myBSplineCurveAction == BSplineCurveAction.Input_OtherPoints:
            if len(self.Poles)<=3:
                self.bspline.RemoveLabel()
                del self.bspline
                self.myContext.Remove(self.myRubberAIS_Shape, True)
            # remove the last pole
            del self.Poles2d[-1]
            del self.Poles[-1]
            self.Multi, self.Knots = setQuasiUniformKnots(len(self.Poles), self.myDegree)
            self.CreateBspline()
            ME = BRepBuilderAPI_MakeEdge(self.myGeom_BSplineCurve)
            if ME.IsDone():
                self.curEdge = ME.Edge()
                self.closeBSpline()
                self.IndexCounter -= 1
        self.myBSplineCurveAction = BSplineCurveAction.Nothing

    def GetTypeOfMethod(self):
        return Sketch_ObjectTypeOfMethod.BSpline_Method

    def closeBSpline(self):
        self.myContext.Remove(self.myRubberAIS_Shape, True)
        self.bspline_node = BsplineNode(self.bspline.GetName(), self.rootNode)
        self.bspline.SetKnots(self.Knots)
        self.bspline.SetMultiplicities(self.Multi)
        self.bspline.SetDegree(self.myDegree)
        self.bspline.Compute()
        self.bspline_node.setSketchObject(self.bspline)
        self.AddObject(self.bspline.GetGeometry2d(), self.bspline.GetAIS_Object(),
                       Sketch_GeometryType.CurveSketchObject)
        self.Poles2d = [gp.Origin2d()] * 2
        self.Poles = [gp.Origin()] * 2
        self.Multi, self.Knots = setQuasiUniformKnots(len(self.Poles), self.myDegree)
        self.myBSplineCurveAction = BSplineCurveAction.Input_1Point
