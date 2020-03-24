from data.design.commands.part_command import *
from data.design.gui import bezierSurfaceForm


class BsplineSurfaceAction(Enum):
    Nothing = 0
    Input_Curve1 = 1
    Input_Curve2 = 2
    Input_Curve3 = 3
    Input_Curve4 = 4

class Part_CommandBsplineSurface(Part_Command):
    def __init__(self,gui):
        super(Part_CommandBsplineSurface, self).__init__("BsplineSurface.")
        self.myCurves = []
        self.myGUI: part_qtgui.Part_QTGUI = gui
        self.myAxis = gp_Ax1()
        self.myGeomSurface = None
        self.myRubberSurface = None
        self.myBsplineSurfaceAction = BsplineSurfaceAction.Nothing

    def Action(self):
        self.myBsplineSurfaceAction = BsplineSurfaceAction.Input_Curve1

    def MouseInputEvent(self, xPix, yPix, buttons, modifier):
        myObjects = self.SelectObject(xPix, yPix)
        if myObjects is None:
            return False
        if myObjects.Type() == AIS_KOI_Shape:
            curve = self.FindGeometry(myObjects)

    def MouseMoveEvent(self, xPix, yPix, buttons, modifier):
        myObjects = self.DetectObject(xPix, yPix)
        if self.myBsplineSurfaceAction == BsplineSurfaceAction.Nothing:
            pass
        elif self.myBsplineSurfaceAction == BsplineSurfaceAction.Input_Curve1:
            self.myStatusBar.showMessage("select 1st bspline curve!", 1000)
        elif self.myBsplineSurfaceAction == BsplineSurfaceAction.Input_Curve2:
            self.myStatusBar.showMessage("select 2nd bspline curve!", 1000)
        elif self.myBsplineSurfaceAction == BsplineSurfaceAction.Input_Curve3:
            self.myStatusBar.showMessage("select 3rd bspline curve!", 1000)
        elif self.myBsplineSurfaceAction == BsplineSurfaceAction.Input_Curve4:
            self.myStatusBar.showMessage("select 4th bspline curve!", 1000)

    def CancelEvent(self):
        if self.myBsplineSurfaceAction == BsplineSurfaceAction.Nothing:
            pass
        elif self.myBsplineSurfaceAction == BsplineSurfaceAction.Input_Curve1:
            pass
        elif self.myBsplineSurfaceAction == BsplineSurfaceAction.Input_Curve2:
            pass
        elif self.myBsplineSurfaceAction == BsplineSurfaceAction.Input_Curve3:
            self.CloseSurface()
        elif self.myBsplineSurfaceAction == BsplineSurfaceAction.Input_Curve4:
            self.CloseSurface()
        self.myCurves.clear()
        self.myBsplineSurfaceAction = BsplineSurfaceAction.Nothing

    def CloseSurface(self):
        self.myContext.Remove(self.myRubberSurface, True)
        self.myGeomSurface = Surface_Bezier(self.myContext)
        self.myGeomSurface.SetCurves(self.myCurves)
        self.myGeomSurface.Compute()
        self.bezierSurfaceNode = BezierSurfaceNode(self.myGeomSurface.GetName(), self.myNode)
        self.bezierSurfaceNode.setSketchObject(self.myGeomSurface)
        self.myModel.layoutChanged.emit()

    def GetTypeOfMethod(self):
        return Part_ObjectTypeOfMethod.BSplineSurface_Method
