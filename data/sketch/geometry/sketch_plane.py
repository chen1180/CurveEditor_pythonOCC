from OCC.Core.Geom import *
from OCC.Core.AIS import AIS_Plane
from OCC.Core.gp import *
from OCC.Core.Aspect import *
from OCC.Core.Graphic3d import *
from OCC.Core.Quantity import *
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace


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
        self.myShape = None
        self.myAIS_InteractiveObject: AIS_Plane = None
        self.myColor = Quantity_Color(Quantity_NOC_ALICEBLUE)

    def Compute(self):
        self.myGeometry = Geom_Plane(self.myCoordinate)
        self.myAIS_InteractiveObject = AIS_Plane(self.myGeometry, True)
        self.myAIS_InteractiveObject.SetColor(self.myColor)
        self.myShape = BRepBuilderAPI_MakeFace(self.myGeometry.Pln()).Shape()
        # self.myContext.Display(self.myAIS_InteractiveObject, True)

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
        canvas_size = 1000
        grid_interval = 100
        self.myDisplay.Viewer.SetRectangularGridGraphicValues(canvas_size, canvas_size, offset)
        self.myAIS_InteractiveObject.SetSize(canvas_size * 2)
        self.myDisplay.Viewer.SetRectangularGridValues(0.0, 0.0, grid_interval, grid_interval, 0.0)
    def DisplayGrid(self):
        self.myDisplay.Viewer.SetPrivilegedPlane(self.myCoordinate)
        self.myDisplay.Viewer.ActivateGrid(Aspect_GT_Rectangular, Aspect_GDM_Lines)
        self.myDisplay.View.SetFront()

    def GetAIS_Object(self):
        return self.myAIS_InteractiveObject

    def GetGeometry(self):
        return self.myGeometry

    def GetShape(self):
        return self.myShape
