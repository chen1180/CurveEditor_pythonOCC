from data.design.commands.part_command import *


class RevolvedSurfaceAction(Enum):
    Nothing = 0
    Input_Curve = 1
    Input_Axis = 2


class Part_CommandRevolvedSurface(Part_Command):
    def __init__(self, gui):
        super(Part_CommandRevolvedSurface, self).__init__("RevolvedSurface.")
        self.myCurve = Geom_Line(gp.OX())
        self.myGUI: part_qtgui.Part_QTGUI = gui
        self.myRevolvedSurfaceAction = RevolvedSurfaceAction.Nothing

    def Action(self):
        self.myRevolvedSurfaceAction = RevolvedSurfaceAction.Input_Curve

    def MouseInputEvent(self, xPix, yPix, buttons, modifier):
        myObjects = self.SelectObject(xPix, yPix)
        if myObjects is None:
            return False
        if self.myGUI.form_createRevolSurface.selectProfile==True:
            self.myGUI.form_createRevolSurface.SetProfile()
            self.myGUI.form_createRevolSurface.selectProfile=False
        if self.myGUI.form_createRevolSurface.selectAxis==True:
            self.myGUI.form_createRevolSurface.SetAxis()
            self.myGUI.form_createRevolSurface.selectAxis=False
        # if self.myRevolvedSurfaceAction == RevolvedSurfaceAction.Nothing:
        #     pass
        # elif self.myRevolvedSurfaceAction == RevolvedSurfaceAction.Input_Curve:
        #     if myObjects.Type() == AIS_KOI_Shape:
        #         curve = self.FindGeometry(myObjects)
        # elif self.myRevolvedSurfaceAction == RevolvedSurfaceAction.Input_Axis:
        #     if myObjects.Type() == AIS_KOI_Datum:
        #         datum = self.FindDatum(myObjects)

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
