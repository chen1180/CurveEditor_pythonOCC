from data.design.part_command import *
from enum import Enum

from OCC.Core.Geom import  Geom_SurfaceOfRevolution, Geom_Line


class BezierSurfaceAction(Enum):
    Nothing = 0
    Input_Curve1 = 1
    Input_Curve2 = 2
    Input_Curve3 = 3

class Part_CommandRevolvedSurface(Part_Command):
    def __init__(self):
        super(Part_CommandRevolvedSurface, self).__init__("RevolvedSurface.")
        # self.myRubberAxis = AIS_Line()
        # self.myRubberAxis.SetColor(Quantity_Color(Quantity_NOC_LIGHTPINK1))
        self.myCurve = Geom_Line(gp.OX())
        self.myAxis = gp_Ax1()
        self.myGeomSurface = Geom_SurfaceOfRevolution(self.myCurve, self.myAxis)
        self.myRubberSurface = None
        self.myRevolvedSurfaceAction = BezierSurfaceAction.Nothing

    def Action(self):
        self.myRevolvedSurfaceAction = BezierSurfaceAction.Input_Curve

    def MouseInputEvent(self, xPix, yPix):
        myObjects = self.SelectObject(xPix, yPix)
        if myObjects is None:
            return False
        if self.myRevolvedSurfaceAction == BezierSurfaceAction.Nothing:
            pass
        elif self.myRevolvedSurfaceAction == BezierSurfaceAction.Input_Curve:
            if myObjects.Type() == AIS_KOI_Shape:
                curve = self.FindGeometry(myObjects)
                if curve:
                    self.myCurve = curve
                    self.myGeomSurface.SetBasisCurve(self.myCurve)
                    self.myRevolvedSurfaceAction = BezierSurfaceAction.Input_Axis
            elif myObjects.Type() == AIS_KOI_Datum:
                datum = self.FindDatum(myObjects)
                if type(datum) == AIS_Circle:
                    self.myCurve = datum.Circle()
                    self.myGeomSurface.SetBasisCurve(self.myCurve)
                    self.myRevolvedSurfaceAction = BezierSurfaceAction.Input_Axis
                elif type(datum) == AIS_Line:
                    self.myCurve = datum.Line()
                    self.myGeomSurface.SetBasisCurve(self.myCurve)
                    self.myRevolvedSurfaceAction = BezierSurfaceAction.Input_Axis
        elif self.myRevolvedSurfaceAction == BezierSurfaceAction.Input_Axis:
            if myObjects.Type() == AIS_KOI_Datum:
                datum = self.FindDatum(myObjects)
                if datum:
                    if type(datum) == AIS_Line:
                        self.myContext.Remove(self.myRubberSurface, True)
                        self.myAxis = datum.Line().Position()
                        surface = Geom_SurfaceOfRevolution(self.myCurve, self.myAxis)
                        self.myDisplay.DisplayShape(surface)
                        self.myRevolvedSurfaceAction = BezierSurfaceAction.Input_Curve

    def MouseMoveEvent(self, xPix, yPix):
        myObjects = self.DetectObject(xPix, yPix)

        if self.myRevolvedSurfaceAction == BezierSurfaceAction.Nothing:
            pass
        elif self.myRevolvedSurfaceAction == BezierSurfaceAction.Input_Curve:
            pass
        elif self.myRevolvedSurfaceAction == BezierSurfaceAction.Input_Axis:
            if myObjects is None:
                self.myContext.Remove(self.myRubberSurface, True)
            else:
                if myObjects.Type() == AIS_KOI_Datum:
                    datum = self.FindDatum(myObjects)
                    if datum:
                        if type(datum) == AIS_Line:
                            myAxis = datum.Line().Position()
                            surface = Geom_SurfaceOfRevolution(self.myCurve, myAxis)
                            self.myRubberSurface = self.myDisplay.DisplayShape(surface)
                else:
                    self.myContext.Remove(self.myRubberSurface, True)

    def CancelEvent(self):
        if self.myRevolvedSurfaceAction == BezierSurfaceAction.Nothing:
            pass
        elif self.myRevolvedSurfaceAction == BezierSurfaceAction.Input_Curve:
            pass
        elif self.myRevolvedSurfaceAction == BezierSurfaceAction.Input_Axis:
            geomSurface = Geom_SurfaceOfRevolution(self.myCurve, self.myAxis)
            self.myContext.Remove(self.myRubberSurface, True)
            # self.AddObject() not impletemented yet
            self.myContext.Display(geomSurface, True)
        self.myRevolvedSurfaceAction = BezierSurfaceAction.Nothing

    def GetTypeOfMethod(self):
        return Part_ObjectTypeOfMethod.RevolvedSurface_Method


