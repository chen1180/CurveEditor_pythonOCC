from data.sketch.commands.sketch_command import *
from OCC.Core.ElCLib import elclib
from OCC.Core.Geom2d import Geom2d_Circle
from enum import Enum
from OCC.Core.Geom import Geom_Circle


class CircleCenterRadiusAction(Enum):
    Nothing = 0
    Input_CenterPoint = 1
    Input_RadiusPoint = 2


class Sketch_CommandNurbCircleTriangle(Sketch_Command):
    def __init__(self):
        super(Sketch_CommandNurbCircleTriangle, self).__init__("NURBS Circle.")
        self.myCircleCenterRadiusAction = CircleCenterRadiusAction.Nothing
        self.radius = 0.0
        self.tempGeom_Circle = Geom_Circle(self.curCoordinateSystem.Ax2(), SKETCH_RADIUS)
        self.myRubberCircle = AIS_Circle(self.tempGeom_Circle)
        self.myRubberCircle.SetColor(Quantity_Color(Quantity_NOC_BLUE1))
        self.myCircleAx2d = gp_Ax2d()

    def Action(self):
        self.myCircleCenterRadiusAction = CircleCenterRadiusAction.Input_CenterPoint
        self.tempGeom_Circle.SetAxis(self.curCoordinateSystem.Axis())
        # if self.curCoordinateSystem.XDirection():
        #     self.myCircleAx2d.SetDirection(gp_Dir2d(self.curCoordinateSystem.XDirection().X(), self.curCoordinateSystem.XDirection().Y()))

    def MouseInputEvent(self, thePnt2d: gp_Pnt2d, buttons, modifier):
        if self.myCircleCenterRadiusAction == CircleCenterRadiusAction.Nothing:
            pass
        elif self.myCircleCenterRadiusAction == CircleCenterRadiusAction.Input_CenterPoint:
            self.curPnt2d = self.myAnalyserSnap.MouseInput(thePnt2d)
            self.myFirstgp_Pnt2d = gp_Pnt2d(self.curPnt2d.X(), self.curPnt2d.Y())
            self.myFirstPoint.SetPnt(elclib.To3d(self.curCoordinateSystem.Ax2(), self.curPnt2d))

            self.myCircleAx2d.SetLocation(self.myFirstgp_Pnt2d)
            self.tempGeom_Circle.SetLocation(self.myFirstPoint.Pnt())
            self.tempGeom_Circle.SetRadius(SKETCH_RADIUS)
            self.myRubberCircle.SetCircle(self.tempGeom_Circle)
            self.myContext.Display(self.myRubberCircle, True)

            # self.myRubberLine.SetPoints(self.myFirstPoint, self.myFirstPoint)
            # self.myContext.Display(self.myRubberLine, True)

            self.myCircleCenterRadiusAction = CircleCenterRadiusAction.Input_RadiusPoint
        elif self.myCircleCenterRadiusAction == CircleCenterRadiusAction.Input_RadiusPoint:
            self.curPnt2d = self.myAnalyserSnap.MouseInputException(self.myFirstgp_Pnt2d, thePnt2d,
                                                                    TangentType.Circle_CenterPnt, True)
            self.radius = self.myFirstgp_Pnt2d.Distance(self.curPnt2d)
            self.myContext.Remove(self.myRubberCircle, True)

            nurbs = self.ToNurbs_Triangle()
            nurbs.Compute()
            self.bspline_node = BsplineNode(nurbs.GetName(), self.rootNode)
            self.bspline_node.setSketchObject(nurbs)
            self.AddObject(nurbs.GetGeometry2d(), nurbs.GetAIS_Object(), Sketch_GeometryType.CurveSketchObject)
            self.myCircleCenterRadiusAction = CircleCenterRadiusAction.Nothing

        return False

    def MouseMoveEvent(self, thePnt2d: gp_Pnt2d, buttons, modifiers):
        if self.myCircleCenterRadiusAction == CircleCenterRadiusAction.Nothing:
            pass
        elif self.myCircleCenterRadiusAction == CircleCenterRadiusAction.Input_CenterPoint:
            self.curPnt2d = self.myAnalyserSnap.MouseMove(thePnt2d)
        elif self.myCircleCenterRadiusAction == CircleCenterRadiusAction.Input_RadiusPoint:
            self.curPnt2d = self.myAnalyserSnap.MouseMoveException(self.myFirstgp_Pnt2d, thePnt2d,
                                                                   TangentType.Circle_CenterPnt, True)
            self.radius = self.myFirstgp_Pnt2d.Distance(self.curPnt2d)
            if self.radius == 0.0:
                self.radius = 1.0
            self.tempGeom_Circle.SetRadius(self.radius)
            self.myContext.Redisplay(self.myRubberCircle, True)
            self.mySecondPoint.SetPnt(elclib.To3d(self.curCoordinateSystem.Ax2(), self.curPnt2d))
            # self.myRubberLine.SetPoints(self.myFirstPoint, self.mySecondPoint)
            # self.myContext.Redisplay(self.myRubberLine, True)

    def CancelEvent(self):
        if self.myCircleCenterRadiusAction == CircleCenterRadiusAction.Nothing:
            pass
        elif self.myCircleCenterRadiusAction == CircleCenterRadiusAction.Input_CenterPoint:
            pass
        elif self.myCircleCenterRadiusAction == CircleCenterRadiusAction.Input_RadiusPoint:
            self.myContext.Remove(self.myRubberCircle, True)
        self.myCircleCenterRadiusAction = CircleCenterRadiusAction.Nothing

    def GetTypeOfMethod(self):
        return Sketch_ObjectTypeOfMethod.NurbsCircleTriangle_Method

    def ToNurbs_Triangle(self):
        nurbsCircle = Sketch_Bspline(self.myContext, self.curCoordinateSystem)
        convert: Geom_BSplineCurve = geomconvert_CurveToBSplineCurve(self.tempGeom_Circle)
        poles = TColgp_Array1OfPnt2d_to_point_list(convert.Poles())
        weights = convert.Weights()
        knots = convert.Knots()
        multiplicity = convert.Multiplicities()

        for pole in poles:
            x, y = pole.X(), pole.Y()
            nurbsCircle.AddPoles(gp_Pnt2d(x, y))
        nurbsCircle.AddPoles(gp_Pnt2d(poles[0].X(), poles[0].Y()))

        nurbsCircle.SetWeights([1.0, 0.5000000000000001, 1.0, 0.5000000000000001, 1.0, 0.5000000000000001, 1.0])
        nurbsCircle.SetKnots(TColStd_Array1OfNumber_to_list(knots))
        nurbsCircle.SetMultiplicities([3, 2, 2, 3])
        nurbsCircle.SetDegree(convert.Degree())

        nurbsCircle.Compute()
        return nurbsCircle
