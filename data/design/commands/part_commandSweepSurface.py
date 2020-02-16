from data.design.commands.part_command import *


class SweepSurfaceAction(Enum):
    Nothing = 0
    Input_Profile = 1
    Input_Path = 2


class Part_CommandSweepSurface(Part_Command):
    def __init__(self):
        super(Part_CommandSweepSurface, self).__init__("SweepSurface.")
        self.myCurve = Geom_Line(gp.OX())
        self.myPath = None
        self.myGeomSurface = GeomFill_Pipe()
        self.myRubberSurface = None
        self.mySweepSurfaceAction = SweepSurfaceAction.Nothing

    def Action(self):
        self.mySweepSurfaceAction = SweepSurfaceAction.Input_Profile

    def MouseInputEvent(self, xPix, yPix, buttons, modifier):
        myObjects = self.SelectObject(xPix, yPix)
        if myObjects is None:
            return False
        if self.mySweepSurfaceAction == SweepSurfaceAction.Nothing:
            pass
        elif self.mySweepSurfaceAction == SweepSurfaceAction.Input_Profile:
            if myObjects.Type() == AIS_KOI_Shape:
                curve = self.FindGeometry(myObjects)
                if curve:
                    self.myCurve = curve
                    self.mySweepSurfaceAction = SweepSurfaceAction.Input_Path
        elif self.mySweepSurfaceAction == SweepSurfaceAction.Input_Path:
            if myObjects.Type() == AIS_KOI_Shape:
                curve = self.FindGeometry(myObjects)
                if curve:
                    self.myPath = curve
                    self.CloseSurface()
                    self.mySweepSurfaceAction = SweepSurfaceAction.Nothing

    def MouseMoveEvent(self, xPix, yPix, buttons, modifier):
        myObjects = self.DetectObject(xPix, yPix)

        if self.mySweepSurfaceAction == SweepSurfaceAction.Nothing:
            pass
        elif self.mySweepSurfaceAction == SweepSurfaceAction.Input_Profile:
            pass
        elif self.mySweepSurfaceAction == SweepSurfaceAction.Input_Path:
            pass

    def CancelEvent(self):
        if self.mySweepSurfaceAction == SweepSurfaceAction.Nothing:
            pass
        elif self.mySweepSurfaceAction == SweepSurfaceAction.Input_Profile:
            pass
        elif self.mySweepSurfaceAction == SweepSurfaceAction.Input_Path:
            pass
        self.mySweepSurfaceAction = SweepSurfaceAction.Nothing

    def GetTypeOfMethod(self):
        return Part_ObjectTypeOfMethod.SweptSurface_Method

    def CloseSurface(self):
        self.mySurface = Surface_Sweep(self.myContext, self.curCoordinateSystem)
        self.mySurface.SetProfile(self.myCurve)
        self.mySurface.SetPath(self.myPath)
        self.mySurface.Compute()
        self.surfaceNode = SweepSurfaceNode(self.mySurface.GetName(), self.myNode)
        self.surfaceNode.setSketchObject(self.mySurface)
