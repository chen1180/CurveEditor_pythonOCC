from data.sketch.commands.sketch_command import *
from OCC.Core.ElCLib import elclib
from OCC.Core.AIS import AIS_Point
from OCC.Core.Geom2d import Geom2d_CartesianPoint, Geom2d_Line, Geom2d_Circle
from OCC.Core.Geom import Geom_CartesianPoint, Geom_BezierCurve
from enum import Enum
from OCC.Core.TopoDS import TopoDS_Edge
from OCC.Core.TColgp import TColgp_Array1OfPnt2d, TColgp_Array1OfPnt
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from OCC.Core.Geom import Geom_Circle
from OCC.Core.Geom2dAdaptor import Geom2dAdaptor_Curve
from data.sketch.geometry.geom2d_edge import Geom2d_Edge
from data.sketch.geometry.geom2d_arc import Geom2d_Arc
from OCC.Core.Geom2dGcc import Geom2dGcc_Circ2d3Tan, Geom2dGcc_QualifiedCurve
from OCC.Core.GccEnt import gccent_Unqualified
from OCC.Core.gce import gce_MakeCirc, gce_Done


class Arc3PAction(Enum):
    Nothing = 0
    Input_1ArcPoint = 1
    Input_2ArcPoint = 2
    Input_3ArcPoint = 3
    Input_PolylineArc = 4





class Sketch_CommandArc3P(Sketch_Command):
    def __init__(self):
        super(Sketch_CommandArc3P, self).__init__("Arc3P.")
        self.myArc3PAction = Arc3PAction.Nothing
        self.tempGeom_Circle = Geom_Circle(self.curCoordinateSystem.Ax2(), SKETCH_RADIUS)
        self.myRubberCircle = AIS_Circle(self.tempGeom_Circle)
        self.temp2d_Circ = gp_Circ2d()
        self.temp_Circ = gp_Circ(self.curCoordinateSystem.Ax2(), SKETCH_RADIUS)
        self.temp2dAdaptor_Curve = Geom2dAdaptor_Curve()

        self.mySecondgp_Pnt2d = gp.Origin2d()
        self.third_Pnt = gp.Origin()
        self.midpoint2d = gp.Origin2d()
        self.tempu1_pnt2d = gp.Origin2d()
        self.tempu2_pnt2d = gp.Origin2d()

        self.tempGeom2d_Line = Geom2d_Line(self.tempu1_pnt2d, gp.DX2d())
        self.tempGeom2d_Circle = Geom2d_Circle(self.temp2d_Circ)

        self.FirstGeom2d_Point = Geom2d_CartesianPoint(self.tempu1_pnt2d)
        self.TempGeom2d_Point = Geom2d_CartesianPoint(self.tempu2_pnt2d)

        self.u1 =0
        self.u2 = 0
        self.temp_u1=0
        self.temp_u2 = 0
        self.dist1=0
        self.dist2 = 0

    def Action(self):
        self.myArc3PAction = Arc3PAction.Input_1ArcPoint
        self.temp_Circ.SetPosition(self.curCoordinateSystem.Ax2())

    def MouseInputEvent(self, thePnt2d: gp_Pnt2d, buttons, modifier):
        self.curPnt2d = self.myAnalyserSnap.MouseInput(thePnt2d)
        if self.myArc3PAction == Arc3PAction.Nothing:
            pass
        elif self.myArc3PAction == Arc3PAction.Input_1ArcPoint:
            self.myFirstgp_Pnt2d = gp_Pnt2d(self.curPnt2d.X(),self.curPnt2d.Y())
            self.myFirstPoint.SetPnt(elclib.To3d(self.curCoordinateSystem.Ax2(), self.curPnt2d))
            if not self.myPolylineMode:
                self.myRubberLine.SetPoints(self.myFirstPoint, self.myFirstPoint)
                self.myContext.Display(self.myRubberLine, True)
                self.myArc3PAction = Arc3PAction.Input_2ArcPoint
            else:
                self.findlastSObject()
                self.myContext.Display(self.myRubberCircle, True)
        elif self.myArc3PAction == Arc3PAction.Input_2ArcPoint:
            self.mySecondgp_Pnt2d =  gp_Pnt2d(self.curPnt2d.X(),self.curPnt2d.Y())
            self.mySecondPoint.SetPnt(elclib.To3d(self.curCoordinateSystem.Ax2(), self.curPnt2d))
            self.temp_Circ.SetLocation(self.myFirstPoint.Pnt().Scaled(self.mySecondPoint.Pnt(), 0.5))
            self.temp_Circ.SetRadius(self.myFirstgp_Pnt2d.Distance(self.curPnt2d) / 2)

            self.tempGeom_Circle.SetCirc(self.temp_Circ)
            self.myRubberCircle.SetCircle(self.tempGeom_Circle)

            self.u1 = elclib.Parameter(self.temp_Circ, self.myFirstPoint.Pnt())
            self.u2 = elclib.Parameter(self.temp_Circ, self.mySecondPoint.Pnt())

            if self.u1 > self.u2:
                self.myRubberCircle.SetFirstParam(self.u2)
                self.myRubberCircle.SetLastParam(self.u1)
            else:
                self.myRubberCircle.SetFirstParam(self.u1)
                self.myRubberCircle.SetLastParam(self.u2)

            self.myContext.Remove(self.myRubberLine, True)
            self.myContext.Display(self.myRubberCircle, True)
            self.myContext.Redisplay(self.myRubberCircle, True)
            self.myArc3PAction = Arc3PAction.Input_3ArcPoint

        elif self.myArc3PAction == Arc3PAction.Input_3ArcPoint:
            Geom2d_Point1 = Geom2d_CartesianPoint(self.myFirstgp_Pnt2d)
            Geom2d_Point2 = Geom2d_CartesianPoint(self.mySecondgp_Pnt2d)
            Geom2d_Point3 = Geom2d_CartesianPoint(self.curPnt2d)
            tempGcc_Circ2d3Tan = Geom2dGcc_Circ2d3Tan(Geom2d_Point1, Geom2d_Point2, Geom2d_Point3, 1.0e-10)
            if tempGcc_Circ2d3Tan.IsDone() and tempGcc_Circ2d3Tan.NbSolutions() > 0:
                myGeom2d_Arc = Geom2d_Arc(tempGcc_Circ2d3Tan.ThisSolution(1))
                myGeom2d_Arc.SetParam(self.myFirstgp_Pnt2d, self.mySecondgp_Pnt2d, self.curPnt2d)

                Geom_Circle1 = Geom_Circle(elclib.To3d(self.curCoordinateSystem.Ax2(), myGeom2d_Arc.Circ2d()))
                myAIS_Circle = AIS_Circle(Geom_Circle1)

                myAIS_Circle.SetFirstParam(myGeom2d_Arc.FirstParameter())
                myAIS_Circle.SetLastParam(myGeom2d_Arc.LastParameter())

                self.AddObject(myGeom2d_Arc, myAIS_Circle, Sketch_GeometryType.ArcSketchObject)
                self.myContext.Remove(self.myRubberCircle, True)
                self.myContext.Display(myAIS_Circle, True)

                self.myArc3PAction = Arc3PAction.Input_1ArcPoint
            # self.third_Pnt = elclib.To3d(self.curCoordinateSystem.Ax2(), self.curPnt2d)
            # tempMakeCirc = gce_MakeCirc(self.myFirstPoint.Pnt(), self.mySecondPoint.Pnt(), self.third_Pnt)
            # if tempMakeCirc.Status() == gce_Done:
            #
            #     Geom_Circle1 = Geom_Circle(tempMakeCirc.Value())
            #     myAIS_Circle = AIS_Circle(Geom_Circle1)
            #
            #     myAIS_Circle.SetFirstParam(
            #         elclib.Parameter(Geom_Circle1.Circ(), self.myFirstPoint.Pnt()))
            #     myAIS_Circle.SetLastParam(elclib.Parameter(Geom_Circle1.Circ(), self.third_Pnt))
            #
            #     self.AddObject(Geom_Circle, myAIS_Circle, Sketch_ObjectTypeOfMethod.Arc3P_Method)
            #     self.myContext.Remove(self.myRubberCircle, True)
            #     self.myContext.Display(myAIS_Circle, True)
            #     self.myArc3PAction = Arc3PAction.Input_1ArcPoint

        elif self.myArc3PAction == Arc3PAction.Input_PolylineArc:
            self.TempGeom2d_Point.SetPnt2d(self.curPnt2d)
            temp2d_QualifiedCurve = Geom2dGcc_QualifiedCurve(self.temp2dAdaptor_Curve, gccent_Unqualified)
            tempGcc_Circ2d3Tan = Geom2dGcc_Circ2d3Tan(temp2d_QualifiedCurve, self.FirstGeom2d_Point,
                                                      self.TempGeom2d_Point, 1.0e-6, 0)
            if (tempGcc_Circ2d3Tan.IsDone() and tempGcc_Circ2d3Tan.NbSolutions() > 0):
                self.temp2d_Circ = tempGcc_Circ2d3Tan.ThisSolution(1)
                self.u1 = elclib.Parameter(self.temp2d_Circ, self.myFirstgp_Pnt2d)
                self.u2 = elclib.Parameter(self.temp2d_Circ, self.curPnt2d)

                self.temp_u1 = self.u1 + (self.u2 - self.u1) / 100
                self.temp_u2 = self.u1 - (self.u2 - self.u1) / 100

                self.tempu1_pnt2d = elclib.Value(self.temp_u1, self.temp2d_Circ)
                self.tempu2_pnt2d = elclib.Value(self.temp_u2, self.temp2d_Circ)

                self.dist1 = self.tempu1_pnt2d.Distance(self.midpoint2d)
                self.dist2 = self.tempu2_pnt2d.Distance(self.midpoint2d)

                if self.dist1 < self.dist2:
                    self.tempu1_pnt2d = self.tempu2_pnt2d
                myGeom2d_Arc = Geom2d_Arc(self.temp2d_Circ)
                myGeom2d_Arc.SetParam(self.myFirstgp_Pnt2d, self.tempu1_pnt2d, self.curPnt2d)

                Geom_Circle1 = Geom_Circle(elclib.To3d(self.curCoordinateSystem.Ax2(), myGeom2d_Arc.Circ2d()))
                myAIS_Circle = AIS_Circle(Geom_Circle1)
                myAIS_Circle.SetFirstParam(myGeom2d_Arc.FirstParameter())
                myAIS_Circle.SetLastParam(myGeom2d_Arc.LastParameter())
                self.myContext.Display(myAIS_Circle, True)

                self.AddObject(myGeom2d_Arc, myAIS_Circle, Sketch_GeometryType.ArcSketchObject)

                self.midpoint2d = myGeom2d_Arc.MiddlePnt()
                self.tempGeom2d_Circle.SetCirc2d(myGeom2d_Arc.Circ2d())
                self.temp2dAdaptor_Curve.Load(self.tempGeom2d_Circle)

                self.myFirstgp_Pnt2d = self.curPnt2d
                self.FirstGeom2d_Point.SetPnt2d(self.myFirstgp_Pnt2d)
                self.myFirstPoint.SetPnt(elclib.To3d(self.curCoordinateSystem.Ax2(), self.curPnt2d))

                self.tempGeom_Circle.SetRadius(0)
                self.myRubberCircle.SetCircle(self.tempGeom_Circle)
                self.myContext.Redisplay(self.myRubberCircle, True)
        return False

    def MouseMoveEvent(self, thePnt2d: gp_Pnt2d, buttons, modifiers):
        self.curPnt2d = self.myAnalyserSnap.MouseMove(thePnt2d)
        if self.myArc3PAction == Arc3PAction.Nothing:
            pass
        elif self.myArc3PAction == Arc3PAction.Input_1ArcPoint:
            self.curPnt2d = self.myAnalyserSnap.MouseMove(thePnt2d)
        elif self.myArc3PAction == Arc3PAction.Input_2ArcPoint:
            self.mySecondPoint.SetPnt(elclib.To3d(self.curCoordinateSystem.Ax2(), self.curPnt2d))
            self.myRubberLine.SetPoints(self.myFirstPoint, self.mySecondPoint)
            self.myContext.Redisplay(self.myRubberLine, True)
        elif self.myArc3PAction == Arc3PAction.Input_3ArcPoint:
            self.third_Pnt = elclib.To3d(self.curCoordinateSystem.Ax2(), self.curPnt2d)
            tempMakeCirc = gce_MakeCirc(self.myFirstPoint.Pnt(), self.mySecondPoint.Pnt(), self.third_Pnt)
            if tempMakeCirc.Status() == gce_Done:
                self.tempGeom_Circle.SetCirc(tempMakeCirc.Value())
                self.myRubberCircle.SetCircle(self.tempGeom_Circle)
                self.myRubberCircle.SetFirstParam(
                    elclib.Parameter(self.tempGeom_Circle.Circ(), self.myFirstPoint.Pnt()))
                self.myRubberCircle.SetLastParam(elclib.Parameter(self.tempGeom_Circle.Circ(), self.third_Pnt))
                self.myContext.Redisplay(self.myRubberCircle, True)
        elif self.myArc3PAction == Arc3PAction.Input_PolylineArc:
            self.third_Pnt = elclib.To3d(self.curCoordinateSystem.Ax2(), self.curPnt2d)
            self.TempGeom2d_Point.SetPnt2d(self.curPnt2d)
            temp2d_QualifiedCurve = Geom2dGcc_QualifiedCurve(self.temp2dAdaptor_Curve, gccent_Unqualified)
            tempGcc_Circ2d3Tan = Geom2dGcc_Circ2d3Tan(temp2d_QualifiedCurve, self.FirstGeom2d_Point,
                                                      self.TempGeom2d_Point, 1.0e-6, 0)
            if (tempGcc_Circ2d3Tan.IsDone() and tempGcc_Circ2d3Tan.NbSolutions() > 0):
                self.temp2d_Circ = tempGcc_Circ2d3Tan.ThisSolution(1)
                self.u1 = elclib.Parameter(self.temp2d_Circ, self.myFirstgp_Pnt2d)
                self.u2 = elclib.Parameter(self.temp2d_Circ, self.mySecondgp_Pnt2d)

                self.temp_u1 = self.u1 + (self.u2 - self.u1) / 100
                self.temp_u2 = self.u1 - (self.u2 - self.u1) / 100

                self.tempu1_pnt2d = elclib.Value(self.temp_u1, self.temp2d_Circ)
                self.tempu2_pnt2d = elclib.Value(self.temp_u2, self.temp2d_Circ)

                self.dist1 = self.tempu1_pnt2d.Distance(self.midpoint2d)
                self.dist2 = self.tempu2_pnt2d.Distance(self.midpoint2d)

                if self.dist1 < self.dist2:
                    self.tempu1_pnt2d = self.tempu2_pnt2d
                tempMakeCirc = gce_MakeCirc(self.myFirstPoint.Pnt(),
                                            elclib.To3d(self.curCoordinateSystem.Ax2(), self.tempu1_pnt2d),
                                            self.third_Pnt)
                if tempMakeCirc.Status() == gce_Done:
                    self.tempGeom_Circle.SetCirc(tempMakeCirc.Value())
                    self.myRubberCircle.SetFirstParam(
                        elclib.Parameter(self.tempGeom_Circle.Circ(), self.myFirstPoint.Pnt()))
                    self.myRubberCircle.SetLastParam(elclib.Parameter(self.tempGeom_Circle.Circ(), self.third_Pnt))
                    self.myContext.Redisplay(self.myRubberCircle, True)

    def CancelEvent(self):
        if self.myArc3PAction == Arc3PAction.Nothing:
            pass
        elif self.myArc3PAction == Arc3PAction.Input_1ArcPoint:
            pass
        elif self.myArc3PAction == Arc3PAction.Input_2ArcPoint:
            self.myContext.Remove(self.myRubberLine, True)
        elif self.myArc3PAction == Arc3PAction.Input_3ArcPoint:
            self.myContext.Remove(self.myRubberCircle, True)
        elif self.myArc3PAction == Arc3PAction.Input_PolylineArc:
            self.myContext.Remove(self.myRubberCircle, True)
        self.myArc3PAction = Arc3PAction.Nothing

    def findlastSObject(self):
        self.midpoint2d = gp.Origin2d()
        if len(self.data) > 0:
            lastSObject: Sketch_Object = self.data[-1]
            if lastSObject.GetGeometryType() == Sketch_GeometryType.LineSketchObject:
                last2d_Edge: Geom2d_Edge = lastSObject.GetGeometry()
                if last2d_Edge.GetStart_Pnt().IsEqual(self.myFirstgp_Pnt2d, 1.0e-6) or last2d_Edge.GetEnd_Pnt().IsEqual(
                        self.myFirstgp_Pnt2d, 1.0e-6):
                    self.midpoint2d = last2d_Edge.MiddlePnt()
                    self.tempGeom2d_Line.SetLin2d(last2d_Edge.Lin2d())
                    self.temp2dAdaptor_Curve.Load(self.tempGeom2d_Line)
                else:
                    self.setTempLine()
            elif lastSObject.GetGeometryType() == Sketch_GeometryType.ArcSketchObject:
                last2d_Arc: Geom2d_Arc = lastSObject.GetGeometry()
                if last2d_Arc.FirstPnt().IsEqual(self.myFirstgp_Pnt2d, 1.0e-6) or last2d_Arc.LastPnt().IsEqual(
                        self.myFirstgp_Pnt2d, 1.0e-6):
                    self.midpoint2d = last2d_Arc.MiddlePnt()
                    self.tempGeom2d_Circle.SetCirc2d(last2d_Arc.Circ2d())
                    self.temp2dAdaptor_Curve.Load(self.tempGeom2d_Circle)
                else:
                    self.setTempLine()
            else:
                self.setTempLine()
        else:
            self.setTempLine()
        self.FirstGeom2d_Point.SetPnt2d(self.myFirstgp_Pnt2d)
        self.tempGeom_Circle.SetRadius(0.0)
        self.myRubberCircle.SetCircle(self.tempGeom_Circle)
        self.myArc3PAction = Arc3PAction.Input_PolylineArc

    def SetPolylineFirstPnt(self, p1):
        self.myFirstgp_Pnt2d = p1
        self.myFirstPoint.SetPnt(elclib.To3d(self.curCoordinateSystem.Ax2(), p1))
        self.findlastSObject()
        self.myContext.Display(self.myRubberCircle, True)

    def GetPolylineFirstPnt(self, p1):
        if self.myArc3PAction == Arc3PAction.Input_PolylineArc and self.myPolylineMode == True:
            p1 = self.myFirstgp_Pnt2d
            return True
        else:
            return False

    def SetPolylineMode(self, mode):
        self.myPolylineMode = mode
        if self.myArc3PAction == Arc3PAction.Nothing:
            pass
        elif self.myArc3PAction == Arc3PAction.Input_1ArcPoint:
            pass
        elif self.myArc3PAction == Arc3PAction.Input_2ArcPoint:
            self.findlastSObject()
            self.myContext.Remove(self.myRubberLine, True)
            self.myContext.Display(self.myRubberCircle, True)
        elif self.myArc3PAction == Arc3PAction.Input_3ArcPoint:
            self.findlastSObject()
            self.myContext.Redisplay(self.myRubberCircle, True)
        elif self.myArc3PAction == Arc3PAction.Input_PolylineArc:
            self.mySecondPoint.SetPnt(elclib.To3d(self.curCoordinateSystem.Ax2(), self.curPnt2d))
            self.myContext.Remove(self.myRubberCircle, True)
            self.myContext.Display(self.myRubberLine, True)
            self.myArc3PAction = Arc3PAction.Input_2ArcPoint

    def setTempLine(self):
        self.tempGeom2d_Line.SetLocation(self.myFirstgp_Pnt2d)
        self.tempGeom2d_Line.SetDirection(gp.DX2d())
        self.temp2dAdaptor_Curve.Load(self.tempGeom2d_Line)

    def GetTypeOfMethod(self):
        return Sketch_ObjectTypeOfMethod.Arc3P_Method
