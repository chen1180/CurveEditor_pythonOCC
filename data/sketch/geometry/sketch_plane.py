from OCC.Core.Geom import *
from OCC.Core.AIS import AIS_Plane
from OCC.Core.gp import *
from OCC.Core.Aspect import *
from OCC.Core.Graphic3d import *


class Sketch_PlaneType:
    XY = 0
    YZ = 1
    XZ = 2


class Sketch_Plane(object):

    def __init__(self, theDisplay, theCoordinate):
        self.myContext = theDisplay.Context
        self.myDisplay = theDisplay
        self.myCoordinate = theCoordinate
        self.myGeometry: Geom_Plane = None
        self.myAIS_InteractiveObject: AIS_Plane = None

    def Compute(self):
        self.myGeometry = Geom_Plane(self.myCoordinate)
        self.myAIS_InteractiveObject = AIS_Plane(self.myGeometry, True)
        self.myDisplay.Viewer.SetPrivilegedPlane(self.myCoordinate)
        self.myContext.Display(self.myAIS_InteractiveObject, True)

    def RemoveDisplay(self):
        self.myContext.Remove(self.myAIS_InteractiveObject, False)
        self.myDisplay.Viewer.DeactivateGrid()

    def GetCoordinate(self):
        return self.myCoordinate

    def CreateDynamicGrid(self, offset):
        # camera attribute
        self.view = self.myDisplay.View
        # scale factor by mosue scroller
        self.camera: Graphic3d_Camera = self.view.Camera()
        canvas_size = max(self.view.Size())
        grid_interval = self.camera.Distance() // self.view.Scale() / 5
        self.myDisplay.Viewer.SetRectangularGridGraphicValues(canvas_size, canvas_size, offset)
        self.myDisplay.Viewer.SetRectangularGridValues(0.0, 0.0, grid_interval, grid_interval, 0.0)

    def DisplayGrid(self):
        self.myDisplay.View.SetFront()
        self.myDisplay.Viewer.ActivateGrid(Aspect_GT_Rectangular, Aspect_GDM_Lines)

    def GetAIS_Object(self):
        return self.myAIS_InteractiveObject
