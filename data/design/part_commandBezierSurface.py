from data.design.part_command import *
from enum import Enum
from OCC.Core.BRepBuilderAPI import *
from OCC.Core.Geom import Geom_Line
from OCC.Core.GeomFill import *


class BezierSurfaceAction(Enum):
    Nothing = 0
    Input_Curve1 = 1
    Input_Curve2 = 2
    Input_Curve3 = 3
    Input_Curve4 = 4


class Part_CommandBezierSurface(Part_Command):
    def __init__(self):
        super(Part_CommandBezierSurface, self).__init__("BezierSurface.")
        self.myCurves = []
        self.myAxis = gp_Ax1()
        self.myGeomSurface = []
        self.myRubberSurface = None
        self.myBezierSurfaceAction = BezierSurfaceAction.Nothing

    def Action(self):
        self.myBezierSurfaceAction = BezierSurfaceAction.Input_Curve1

    def MouseInputEvent(self, xPix, yPix):
        myObjects = self.SelectObject(xPix, yPix)
        if myObjects is None:
            return False
        if self.myBezierSurfaceAction == BezierSurfaceAction.Nothing:
            pass
        elif self.myBezierSurfaceAction == BezierSurfaceAction.Input_Curve1:
            if myObjects.Type() == AIS_KOI_Shape:
                curve = self.FindGeometry(myObjects)
                if curve:
                    self.myCurves.append(curve)
                    self.myBezierSurfaceAction = BezierSurfaceAction.Input_Curve2
        elif self.myBezierSurfaceAction == BezierSurfaceAction.Input_Curve2:
            if myObjects.Type() == AIS_KOI_Shape:
                curve = self.FindGeometry(myObjects)
                if curve:
                    self.myCurves.append(curve)
                    surface1 = GeomFill_BezierCurves(self.myCurves[0], curve, GeomFill_CurvedStyle)
                    face = BRepBuilderAPI_MakeFace()
                    face.Init(surface1.Surface(), True, 1.0e-6)
                    face.Build()
                    shape=AIS_Shape(face.Shape())
                    self.myContext.Display(shape,True)
                    self.myBezierSurfaceAction = BezierSurfaceAction.Input_Curve3

    def MouseMoveEvent(self, xPix, yPix):
        myObjects = self.DetectObject(xPix, yPix)
        if self.myBezierSurfaceAction == BezierSurfaceAction.Nothing:
            pass

    def CancelEvent(self):
        if self.myBezierSurfaceAction == BezierSurfaceAction.Nothing:
            pass
        elif self.myBezierSurfaceAction == BezierSurfaceAction.Input_Curve1:
            pass
        elif self.myBezierSurfaceAction == BezierSurfaceAction.Input_Curve2:
            pass
        self.myBezierSurfaceAction = BezierSurfaceAction.Nothing

    def GetTypeOfMethod(self):
        return Part_ObjectTypeOfMethod.BezierSurface_Method
