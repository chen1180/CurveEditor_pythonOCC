from data.design.commands.part_command import *


class SweepSurfaceAction(Enum):
    Nothing = 0
    Input_Profile = 1
    Input_Path = 2


class Part_CommandSweepSurface(Part_Command):
    def __init__(self, gui):
        super(Part_CommandSweepSurface, self).__init__("SweepSurface.")
        self.myGUI: part_qtgui.Part_QTGUI = gui
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
        if self.myGUI.form_createSweepSurface.selectPath == True:
            self.myGUI.form_createSweepSurface.SetPath()
            self.myGUI.form_createSweepSurface.selectPath = False
            self.mySweepSurfaceAction=SweepSurfaceAction.Input_Path
        if self.myGUI.form_createSweepSurface.selectConstantSection == True:
            self.myGUI.form_createSweepSurface.SetConstantSection()
            self.myGUI.form_createSweepSurface.selectConstantSection = False
            self.mySweepSurfaceAction = SweepSurfaceAction.Input_Profile
        if self.myGUI.form_createSweepSurface.selectFirstSection == True:
            self.myGUI.form_createSweepSurface.SetFirstSection()
            self.myGUI.form_createSweepSurface.selectFirstSection = False
            self.mySweepSurfaceAction = SweepSurfaceAction.Input_Profile
        if self.myGUI.form_createSweepSurface.selectLastSection == True:
            self.myGUI.form_createSweepSurface.SetLastSection()
            self.myGUI.form_createSweepSurface.selectLastSection = False
            self.mySweepSurfaceAction = SweepSurfaceAction.Input_Profile
        # elif self.mySweepSurfaceAction == SweepSurfaceAction.Input_Profile:
        #     if myObjects.Type() == AIS_KOI_Shape:
        #         curve = self.FindGeometry(myObjects)
        #         if curve:
        #             self.myCurve = curve
        #             self.mySweepSurfaceAction = SweepSurfaceAction.Input_Path
        # elif self.mySweepSurfaceAction == SweepSurfaceAction.Input_Path:
        #     if myObjects.Type() == AIS_KOI_Shape:
        #         curve = self.FindGeometry(myObjects)
        #         if curve:
        #             self.myPath = curve
        #             self.CloseSurface()
        #             self.mySweepSurfaceAction = SweepSurfaceAction.Nothing

    def MouseMoveEvent(self, xPix, yPix, buttons, modifier):
        myObjects = self.DetectObject(xPix, yPix)

        if self.mySweepSurfaceAction == SweepSurfaceAction.Nothing:
            pass
        elif self.mySweepSurfaceAction == SweepSurfaceAction.Input_Profile:
            if self.myGUI.form_createSweepSurface.selectConstantSection:
                self.myStatusBar.showMessage("Select a constant profile! Press Ecs to cancel!", 1000)
            if self.myGUI.form_createSweepSurface.selectFirstSection:
                self.myStatusBar.showMessage("Select the start profile! Press Ecs to cancel!", 1000)
            if self.myGUI.form_createSweepSurface.selectLastSection:
                self.myStatusBar.showMessage("Select the end profile! Press Ecs to cancel!", 1000)
        elif self.mySweepSurfaceAction == SweepSurfaceAction.Input_Path:
            self.myStatusBar.showMessage("Select a path to sweep! Press Ecs to cancel!", 1000)

    def CancelEvent(self):
        if self.mySweepSurfaceAction == SweepSurfaceAction.Nothing:
            pass
        elif self.mySweepSurfaceAction == SweepSurfaceAction.Input_Profile:
            self.myGUI.Show()
        elif self.mySweepSurfaceAction == SweepSurfaceAction.Input_Path:
            self.myGUI.Show()

    def GetTypeOfMethod(self):
        return Part_ObjectTypeOfMethod.SweptSurface_Method

