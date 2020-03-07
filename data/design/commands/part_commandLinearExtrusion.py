from data.design.commands.part_command import *


class ExtrudedSurfaceAction(Enum):
    Nothing = 0
    Input_Curve = 1


class Part_CommandExtrudedSurface(Part_Command):
    def __init__(self):
        super(Part_CommandExtrudedSurface, self).__init__("ExtrudedSurface.")
        self.myCurve = Geom_Line(gp.OX())
        self.myDir = gp_Dir()
        self.myGeomSurface = Geom_SurfaceOfLinearExtrusion(self.myCurve, self.myDir)
        self.myRubberSurface = None
        self.myRevolvedSurfaceAction = ExtrudedSurfaceAction.Nothing

    def Action(self):
        self.myRevolvedSurfaceAction = ExtrudedSurfaceAction.Input_Curve

    def MouseInputEvent(self, xPix, yPix, buttons, modifier):
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
                    self.CloseSurface()
            elif myObjects.Type() == AIS_KOI_Datum:
                datum = self.FindDatum(myObjects)
                if type(datum) == AIS_Circle:
                    self.myCurve = datum.Circle()
                    self.myGeomSurface.SetBasisCurve(self.myCurve)
                    self.CloseSurface()
                # elif type(datum) == AIS_Line:
                #     self.myCurve = datum.Line()
                #     self.myGeomSurface.SetBasisCurve(self.myCurve)
                #     self.CloseSurface()
    def MouseMoveEvent(self, xPix, yPix, buttons, modifier):
        myObjects = self.DetectObject(xPix, yPix)
        if self.myRevolvedSurfaceAction == ExtrudedSurfaceAction.Nothing:
            pass
        elif self.myRevolvedSurfaceAction == ExtrudedSurfaceAction.Input_Curve:
            pass

    def CancelEvent(self):
        if self.myRevolvedSurfaceAction == ExtrudedSurfaceAction.Nothing:
            pass
        elif self.myRevolvedSurfaceAction == ExtrudedSurfaceAction.Input_Curve:
            pass
        self.myRevolvedSurfaceAction = ExtrudedSurfaceAction.Nothing

    def GetTypeOfMethod(self):
        return Part_ObjectTypeOfMethod.ExtrudedSurface_Method

    def CloseSurface(self):
        self.mySurface = Surface_LinearExtrusion(self.myContext, self.curCoordinateSystem)
        normal_axis = self.curCoordinateSystem.Axis()
        self.myDir = normal_axis.Direction()

        self.mySurface.SetCurves(self.myCurve)
        self.mySurface.SetDirection(self.myDir)
        self.mySurface.Compute()
        self.surfaceNode = ExtrudedSurfaceNode(self.mySurface.GetName(), self.myNode)
        self.surfaceNode.setSketchObject(self.mySurface)
        self.myModel.layoutChanged.emit()
