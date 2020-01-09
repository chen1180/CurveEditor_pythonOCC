from data.design.part_command import *
from enum import Enum

from OCC.Core.Geom import  Geom_SurfaceOfLinearExtrusion, Geom_Line


class ExtrudedSurfaceAction(Enum):
    Nothing = 0
    Input_Curve = 1
    Input_Axis = 2


class Part_CommandExtrudedSurface(Part_Command):
    def __init__(self):
        super(Part_CommandExtrudedSurface, self).__init__("ExtrudedSurface.")
        # self.myRubberAxis = AIS_Line()
        # self.myRubberAxis.SetColor(Quantity_Color(Quantity_NOC_LIGHTPINK1))
        self.myCurve = Geom_Line(gp.OX())
        self.myDir = gp_Dir()
        self.myGeomSurface = Geom_SurfaceOfLinearExtrusion(self.myCurve, self.myDir)
        self.myRubberSurface = None
        self.myRevolvedSurfaceAction = ExtrudedSurfaceAction.Nothing

    def Action(self):
        self.myRevolvedSurfaceAction = ExtrudedSurfaceAction.Input_Curve

    def MouseInputEvent(self, xPix, yPix):
        myObjects = self.SelectObject(xPix, yPix)
        if myObjects is None:
            return False
        if self.myRevolvedSurfaceAction == ExtrudedSurfaceAction.Nothing:
            pass
        elif self.myRevolvedSurfaceAction == ExtrudedSurfaceAction.Input_Curve:
            if myObjects.Type() == AIS_KOI_Shape:
                curve = self.FindGeometry(myObjects)
                if curve:
                    self.myCurve = curve
                    self.myGeomSurface.SetBasisCurve(self.myCurve)
                    self.myRevolvedSurfaceAction = ExtrudedSurfaceAction.Input_Axis
            elif myObjects.Type() == AIS_KOI_Datum:
                datum = self.FindDatum(myObjects)
                if type(datum) == AIS_Circle:
                    self.myCurve = datum.Circle()
                    self.myGeomSurface.SetBasisCurve(self.myCurve)
                    self.myRevolvedSurfaceAction = ExtrudedSurfaceAction.Input_Axis
                elif type(datum) == AIS_Line:
                    self.myCurve = datum.Line()
                    self.myGeomSurface.SetBasisCurve(self.myCurve)
                    self.myRevolvedSurfaceAction = ExtrudedSurfaceAction.Input_Axis
        elif self.myRevolvedSurfaceAction == ExtrudedSurfaceAction.Input_Axis:
            if myObjects.Type() == AIS_KOI_Datum:
                datum = self.FindDatum(myObjects)
                if datum:
                    if type(datum) == AIS_Line:
                        self.myContext.Remove(self.myRubberSurface, True)
                        axis=datum.Line().Position()
                        self.myDir = axis.Direction()
                        surface = Geom_SurfaceOfLinearExtrusion(self.myCurve, self.myDir)
                        self.myDisplay.DisplayShape(surface)
                        self.myRevolvedSurfaceAction = ExtrudedSurfaceAction.Input_Curve

    def MouseMoveEvent(self, xPix, yPix):
        myObjects = self.DetectObject(xPix, yPix)

        if self.myRevolvedSurfaceAction == ExtrudedSurfaceAction.Nothing:
            pass
        elif self.myRevolvedSurfaceAction == ExtrudedSurfaceAction.Input_Curve:
            pass
        elif self.myRevolvedSurfaceAction == ExtrudedSurfaceAction.Input_Axis:
            if myObjects is None:
                self.myContext.Remove(self.myRubberSurface, True)
            else:
                if myObjects.Type() == AIS_KOI_Datum:
                    datum = self.FindDatum(myObjects)
                    if datum:
                        if type(datum) == AIS_Line:
                            myAxis = datum.Line().Position()
                            surface = Geom_SurfaceOfLinearExtrusion(self.myCurve, myAxis.Direction())
                            self.myRubberSurface = self.myDisplay.DisplayShape(surface)
                else:
                    self.myContext.Remove(self.myRubberSurface, True)

    def CancelEvent(self):
        if self.myRevolvedSurfaceAction == ExtrudedSurfaceAction.Nothing:
            pass
        elif self.myRevolvedSurfaceAction == ExtrudedSurfaceAction.Input_Curve:
            pass
        elif self.myRevolvedSurfaceAction == ExtrudedSurfaceAction.Input_Axis:
            geomSurface = Geom_SurfaceOfLinearExtrusion(self.myCurve, self.myDir)
            self.myContext.Remove(self.myRubberSurface, True)
            # self.AddObject() not impletemented yet
            self.myContext.Display(geomSurface, True)
        self.myRevolvedSurfaceAction = ExtrudedSurfaceAction.Nothing

    def GetTypeOfMethod(self):
        return Part_ObjectTypeOfMethod.ExtrudedSurface_Method


