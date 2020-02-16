from OCC.Core.Geom2d import *
from OCC.Core.AIS import *
from OCC.Core.Geom import *
from data.sketch.sketch_utils import *
from OCC.Core.gp import *
from OCC.Core.Aspect import *
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace
from OCC.Core.Prs3d import *
from data.sketch.sketch_object import *
from OCC.Core.Geom import Geom_SurfaceOfLinearExtrusion
from .surface_geometry import Surface_Geometry


class Surface_LinearExtrusion(Surface_Geometry):
    IndexCounter = 0

    def __init__(self, theContext, theAxis):
        super(Surface_LinearExtrusion, self).__init__("Extruded Surface", theContext, theAxis)
        Surface_LinearExtrusion.IndexCounter += 1
        self.myName = self.myName + str(self.IndexCounter)
        self.myCurve = None
        self.myAxis = None
        self.myGeometry = None
        self.myAIS_InteractiveObject = None

    def Compute(self):
        self.myGeometry = Geom_SurfaceOfLinearExtrusion(self.myCurve, self.myAxis)
        face = BRepBuilderAPI_MakeFace()
        face.Init(self.myGeometry, True, 1.0e-6)
        face.Build()
        self.myAIS_InteractiveObject = AIS_Shape(face.Shape())
        self.myContext.Display(self.myAIS_InteractiveObject, True)

    def SetCurves(self, theCurves):
        self.myCurve = theCurves

    def SetDirection(self, theAxis):
        self.myAxis = theAxis
