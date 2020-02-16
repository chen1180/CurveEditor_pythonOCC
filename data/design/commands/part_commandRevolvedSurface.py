from data.design.commands.part_command import *


class RevolvedSurfaceAction(Enum):
    Nothing = 0
    Input_Curve = 1
    Input_Axis = 2


class Part_CommandRevolvedSurface(Part_Command):
    def __init__(self):
        super(Part_CommandRevolvedSurface, self).__init__("RevolvedSurface.")
        self.myCurve = Geom_Line(gp.OX())
        self.myAxis = gp_Ax1()
        self.myGeomSurface = Geom_SurfaceOfRevolution(self.myCurve, self.myAxis)
        self.myRubberSurface = None
        self.myRevolvedSurfaceAction = RevolvedSurfaceAction.Nothing

    def Action(self):
        self.myRevolvedSurfaceAction = RevolvedSurfaceAction.Input_Curve

    def MouseInputEvent(self, xPix, yPix, buttons, modifier):
        myObjects = self.SelectObject(xPix, yPix)
        if myObjects is None:
            return False
        if self.myRevolvedSurfaceAction == RevolvedSurfaceAction.Nothing:
            pass
        elif self.myRevolvedSurfaceAction == RevolvedSurfaceAction.Input_Curve:
            if myObjects.Type() == AIS_KOI_Shape:
                curve = self.FindGeometry(myObjects)
                if curve:
                    self.myCurve = curve
                    self.myGeomSurface.SetBasisCurve(self.myCurve)
                    self.myRevolvedSurfaceAction = RevolvedSurfaceAction.Input_Axis
        elif self.myRevolvedSurfaceAction == RevolvedSurfaceAction.Input_Axis:
            if myObjects.Type() == AIS_KOI_Datum:
                datum = self.FindDatum(myObjects)
                if datum:
                    if type(datum) == AIS_Line:
                        self.myContext.Remove(self.myRubberSurface, True)
                        self.myAxis = datum.Line().Position()
                        self.mySurface = Surface_Revolved(self.myContext, self.curCoordinateSystem)
                        self.mySurface.SetCurves(self.myCurve)
                        self.mySurface.SetRevolveAxis(self.myAxis)
                        self.mySurface.Compute()
                        self.surfaceNode = RevolvedSurfaceNode(self.mySurface.GetName(), self.myNode)
                        self.surfaceNode.setSketchObject(self.mySurface)
                        self.myRevolvedSurfaceAction = RevolvedSurfaceAction.Nothing

    def MouseMoveEvent(self, xPix, yPix, buttons, modifier):
        myObjects = self.DetectObject(xPix, yPix)
        if self.myRevolvedSurfaceAction == RevolvedSurfaceAction.Nothing:
            pass
        elif self.myRevolvedSurfaceAction == RevolvedSurfaceAction.Input_Curve:
            self.myStatusBar.showMessage("Select a shape for revolve operation! (Bezier curve or Bspline)", 1000)
        elif self.myRevolvedSurfaceAction == RevolvedSurfaceAction.Input_Axis:
            self.myStatusBar.showMessage("Select an axis!", 1000)

    def CancelEvent(self):
        if self.myRevolvedSurfaceAction == RevolvedSurfaceAction.Nothing:
            pass
        elif self.myRevolvedSurfaceAction == RevolvedSurfaceAction.Input_Curve:
            pass
        elif self.myRevolvedSurfaceAction == RevolvedSurfaceAction.Input_Axis:
            pass
        self.myRevolvedSurfaceAction = RevolvedSurfaceAction.Nothing

    def GetTypeOfMethod(self):
        return Part_ObjectTypeOfMethod.RevolvedSurface_Method
