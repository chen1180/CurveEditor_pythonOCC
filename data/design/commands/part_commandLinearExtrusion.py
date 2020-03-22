from data.design.commands.part_command import *


class ExtrudedSurfaceAction(Enum):
    Nothing = 0
    Input_Curve = 1
    Input_Axis = 2


class Part_CommandExtrudedSurface(Part_Command):
    def __init__(self, gui):
        super(Part_CommandExtrudedSurface, self).__init__("ExtrudedSurface.")
        self.myGUI: part_qtgui.Part_QTGUI = gui
        self.myExtrudedSurfaceAction = ExtrudedSurfaceAction.Nothing

    def Action(self):
        self.myExtrudedSurfaceAction = ExtrudedSurfaceAction.Input_Curve

    def MouseInputEvent(self, xPix, yPix, buttons, modifier):
        myObjects = self.SelectObject(xPix, yPix)
        if myObjects is None:
            return False
        if self.myExtrudedSurfaceAction == ExtrudedSurfaceAction.Nothing:
            pass
        if self.myGUI.form_createExtrudedSurface.selectProfile == True:
            self.myGUI.form_createExtrudedSurface.SetProfile()
            self.myGUI.form_createExtrudedSurface.selectProfile = False
            self.myExtrudedSurfaceAction = ExtrudedSurfaceAction.Input_Axis
        if self.myGUI.form_createExtrudedSurface.selectDirection == True:
            self.myGUI.form_createExtrudedSurface.SetDirections()
            self.myGUI.form_createExtrudedSurface.selectDirection = False
            self.myExtrudedSurfaceAction = ExtrudedSurfaceAction.Input_Curve

    def MouseMoveEvent(self, xPix, yPix, buttons, modifier):
        myObjects = self.DetectObject(xPix, yPix)
        if self.myExtrudedSurfaceAction == ExtrudedSurfaceAction.Nothing:
            pass
        elif self.myExtrudedSurfaceAction == ExtrudedSurfaceAction.Input_Curve:
            if self.myGUI.form_createExtrudedSurface.selectProfile == True:
                self.myStatusBar.showMessage("Select a profile! Press Esc to cancel!", 1000)
            else:
                self.myStatusBar.showMessage("Construct extruded surface!", 1000)
        elif self.myExtrudedSurfaceAction == ExtrudedSurfaceAction.Input_Axis:
            if self.myGUI.form_createExtrudedSurface.selectDirection == True:
                self.myStatusBar.showMessage("Select a axis!", 1000)
            else:
                pass

    def CancelEvent(self):
        if self.myExtrudedSurfaceAction == ExtrudedSurfaceAction.Nothing:
            pass
        elif self.myExtrudedSurfaceAction == ExtrudedSurfaceAction.Input_Curve:
            self.myGUI.Show()
        elif self.myExtrudedSurfaceAction == ExtrudedSurfaceAction.Input_Axis:
            self.myGUI.Show()

    def GetTypeOfMethod(self):
        return Part_ObjectTypeOfMethod.ExtrudedSurface_Method
