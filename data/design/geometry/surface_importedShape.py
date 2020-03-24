from OCC.Core.Geom2d import *
from OCC.Core.AIS import *
from OCC.Core.Geom import *
from data.sketch.sketch_utils import *
from OCC.Core.gp import *
from OCC.Core.Aspect import *
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace
from OCC.Core.Prs3d import *
from data.sketch.sketch_object import *
from OCC.Core.GeomFill import *
from .surface_geometry import Surface_Geometry


class Surface_ImportedShape(Surface_Geometry):
    def __init__(self, theName, theContext):
        super(Surface_ImportedShape, self).__init__(theName, theContext)
        self.myGeometry = None
        self.myAIS_InteractiveObject = None

    def Compute(self):
        self.myAIS_InteractiveObject = AIS_Shape(self.myGeometry)
        self.myContext.Display(self.myAIS_InteractiveObject, True)
        self.SetCenter(self.myGeometry)
        self.InitClippingPlane()

    def SetGeometry(self, theGeometry):
        self.myGeometry = theGeometry
