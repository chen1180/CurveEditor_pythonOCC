from data.sketch.commands.sketch_commandBSpline import *
from OCC.Core.Geom2dAPI import Geom2dAPI_PointsToBSpline
from OCC.Core.GeomAPI import GeomAPI_PointsToBSpline


class Sketch_CommandPointToBSpline(Sketch_Command):
    def __init__(self):
        super(Sketch_CommandPointToBSpline, self).__init__("PointsToBSpline")
        self.IndexCounter = 1
        self.tempPnt2d = gp.Origin2d()
        self.myFirstgp_Pnt = gp.Origin()
        self.tempPnt = gp.Origin()
        self.curEdge = TopoDS_Edge()

        self.myBSplineCurveAction = BSplineCurveAction.Nothing
        self.Poles2d = [gp.Origin2d()] * 2
        self.Poles = [gp.Origin()] * 2

        curgp_Array1CurvePoles2d = point_list_to_TColgp_Array1OfPnt2d(self.Poles2d)
        curgp_Array1CurvePoles = point_list_to_TColgp_Array1OfPnt(self.Poles)

        self.myGeom2d_BSplineCurve = Geom2dAPI_PointsToBSpline(curgp_Array1CurvePoles2d).Curve()
        self.myGeom_BSplineCurve = GeomAPI_PointsToBSpline(curgp_Array1CurvePoles).Curve()

        self.myRubberAIS_Shape = AIS_Shape(self.curEdge)

    def Action(self):
        self.myBSplineCurveAction = BSplineCurveAction.Input_1Point

    def InterpolatePoints(self):
        curgp_Array1CurvePoles2d = point_list_to_TColgp_Array1OfPnt2d(self.Poles2d)
        curgp_Array1CurvePoles = point_list_to_TColgp_Array1OfPnt(self.Poles)
        try:
            myGeom2d_BSplineCurve = Geom2dAPI_PointsToBSpline(curgp_Array1CurvePoles2d)
            if myGeom2d_BSplineCurve.IsDone():
                self.myGeom2d_BSplineCurve = myGeom2d_BSplineCurve.Curve()
        except Exception as e:
            print(e)
        try:
            myGeom_BSplineCurve = GeomAPI_PointsToBSpline(curgp_Array1CurvePoles)
            if myGeom_BSplineCurve.IsDone():
                self.myGeom_BSplineCurve = myGeom_BSplineCurve.Curve()
        except Exception as e:
            print(e)

    def FindPoints(self, li):
        for i in li:
            if type(i) == gp_Pnt:
                print("3d", i.X(), i.Y(), i.Z())
            elif type(i) == gp_Pnt2d:
                print("2d", i.X(), i.Y())

    def MouseInputEvent(self, thePnt2d: gp_Pnt2d, buttons, modifier):
        self.curPnt2d = self.myAnalyserSnap.MouseInput(thePnt2d)

        if self.myBSplineCurveAction == BSplineCurveAction.Nothing:
            pass
        elif self.myBSplineCurveAction == BSplineCurveAction.Input_1Point:
            self.myFirstgp_Pnt2d = gp_Pnt2d(self.curPnt2d.X(), self.curPnt2d.Y())
            self.myFirstgp_Pnt = elclib.To3d(self.curCoordinateSystem.Ax2(), self.curPnt2d)
            self.myFirstPoint.SetPnt(self.myFirstgp_Pnt)
            self.myRubberLine.SetPoints(self.myFirstPoint, self.myFirstPoint)

            self.Poles2d[0] = gp_Pnt2d(self.curPnt2d.X(), self.curPnt2d.Y())
            self.Poles[0] = gp_Pnt(self.myFirstgp_Pnt.X(), self.myFirstgp_Pnt.Y(), self.myFirstgp_Pnt.Z())
            self.InterpolatePoints()
            self.interpolateBspline = Sketch_Bspline(self.myContext, self.curCoordinateSystem)
            self.interpolateBspline.AddPoles(self.curPnt2d)

            # myGeom2d_Point = Geom2d_CartesianPoint(self.curPnt2d)
            # myAIS_Point = AIS_Point(self.myFirstPoint)
            #
            # self.myContext.Display(myAIS_Point, True)
            # self.AddObject(myGeom2d_Point, myAIS_Point, Sketch_GeometryType.PointSketchObject)
            #
            self.myContext.Display(self.myRubberLine, True)
            self.myBSplineCurveAction = BSplineCurveAction.Input_2Point
            self.IndexCounter = 2

        elif self.myBSplineCurveAction == BSplineCurveAction.Input_2Point:
            self.Poles2d[1] = gp_Pnt2d(self.curPnt2d.X(), self.curPnt2d.Y())
            self.tempPnt = elclib.To3d(self.curCoordinateSystem.Ax2(), self.curPnt2d)
            self.Poles[1] = gp_Pnt(self.tempPnt.X(), self.tempPnt.Y(), self.tempPnt.Z())
            # self.myGeom_BSplineCurve.SetPole(self.IndexCounter,gp_Pnt(self.tempPnt.X(), self.tempPnt.Y(), self.tempPnt.Z()))
            self.InterpolatePoints()
            self.mySecondPoint.SetPnt(self.tempPnt)

            ME = BRepBuilderAPI_MakeEdge(self.myGeom_BSplineCurve)
            if ME.IsDone():
                self.interpolateBspline.AddPoles(self.curPnt2d)
                self.curEdge = ME.Edge()
                self.myRubberAIS_Shape.Set(self.curEdge)
                self.myContext.Remove(self.myRubberLine, True)
                self.myContext.Display(self.myRubberAIS_Shape, True)

                self.Poles2d.append(self.curPnt2d)
                self.Poles.append(self.tempPnt)
                self.InterpolatePoints()
                self.IndexCounter += 1
                self.myBSplineCurveAction = BSplineCurveAction.Input_OtherPoints

        elif self.myBSplineCurveAction == BSplineCurveAction.Input_OtherPoints:
            # self.myGeom2d_BSplineCurve.SetPole(self.IndexCounter, gp_Pnt2d(self.curPnt2d.X(), self.curPnt2d.Y()))
            self.Poles2d[self.IndexCounter - 1] = gp_Pnt2d(self.curPnt2d.X(), self.curPnt2d.Y())
            self.tempPnt = elclib.To3d(self.curCoordinateSystem.Ax2(), self.curPnt2d)
            self.Poles[self.IndexCounter - 1] = gp_Pnt(self.tempPnt.X(), self.tempPnt.Y(), self.tempPnt.Z())
            # self.myGeom_BSplineCurve.SetPole(self.IndexCounter,gp_Pnt(self.tempPnt.X(), self.tempPnt.Y(), self.tempPnt.Z()))
            self.InterpolatePoints()
            self.mySecondPoint.SetPnt(self.tempPnt)
            ME = BRepBuilderAPI_MakeEdge(self.myGeom_BSplineCurve)
            if ME.IsDone():
                self.interpolateBspline.AddPoles(self.curPnt2d)
                self.curEdge = ME.Edge()
                if self.IndexCounter > MAXIMUMPOLES:
                    self.closeBSpline()
                else:
                    self.myRubberAIS_Shape.Set(self.curEdge)
                    self.myContext.Redisplay(self.myRubberAIS_Shape, True)

                    self.Poles2d.append(self.curPnt2d)
                    self.Poles.append(self.tempPnt)
                    self.InterpolatePoints()
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
            self.mySecondPoint.SetPnt(elclib.To3d(self.curCoordinateSystem.Ax2(), self.curPnt2d))
            self.myRubberLine.SetPoints(self.myFirstPoint, self.mySecondPoint)
            self.myContext.Redisplay(self.myRubberLine, True)
        elif self.myBSplineCurveAction == BSplineCurveAction.Input_OtherPoints:
            self.myGeom2d_BSplineCurve.SetPole(self.IndexCounter - 1, self.curPnt2d)
            self.mySecondPoint.SetPnt(elclib.To3d(self.curCoordinateSystem.Ax2(), self.curPnt2d))
            self.myGeom_BSplineCurve.SetPole(self.IndexCounter - 1, self.mySecondPoint.Pnt())
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
            self.myContext.Remove(self.myRubberLine, True)
        elif self.myBSplineCurveAction == BSplineCurveAction.Input_OtherPoints:
            ME = BRepBuilderAPI_MakeEdge(self.myGeom_BSplineCurve)
            if ME.IsDone():
                self.curEdge = ME.Edge()
                self.IndexCounter -= 1
                self.closeBSpline()
        self.myBSplineCurveAction = BSplineCurveAction.Nothing

    def GetTypeOfMethod(self):
        return Sketch_ObjectTypeOfMethod.PointsToBSpline_Method

    def closeBSpline(self):
        self.myContext.Remove(self.myRubberAIS_Shape, True)
        self.interpolateBspline.AddPoles(self.curPnt2d)
        self.interpolateBspline_node = BsplineNode(self.interpolateBspline.GetName(), self.rootNode)
        self.interpolateBspline.ComputeInterpolation()
        self.interpolateBspline_node.setSketchObject(self.interpolateBspline)
        self.AddObject(self.interpolateBspline.GetGeometry2d(), self.interpolateBspline.GetAIS_Object(),
                       Sketch_GeometryType.CurveSketchObject)

        self.Poles2d = [gp.Origin2d()] * 2
        self.Poles = [gp.Origin()] * 2
        self.InterpolatePoints()
        self.myBSplineCurveAction = BSplineCurveAction.Input_1Point
