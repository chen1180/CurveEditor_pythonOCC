from OCC.Core.Geom2d import *
from OCC.Core.AIS import *
from OCC.Core.Geom import *
from data.sketch.sketch_utils import *
from OCC.Core.gp import *
from OCC.Core.Aspect import *
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakeEdge
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakePrism
from OCC.Core.Prs3d import *
from data.sketch.sketch_object import *
from OCC.Core.Geom import Geom_SurfaceOfLinearExtrusion
from .surface_geometry import Surface_Geometry



class Surface_LinearExtrusion(Surface_Geometry):
    IndexCounter = 0

    def __init__(self, theContext):
        super(Surface_LinearExtrusion, self).__init__("Extruded Surface", theContext)
        Surface_LinearExtrusion.IndexCounter += 1
        self.myName = self.myName + str(self.IndexCounter)
        self.myCurve = None
        self.myVec = None
        self.myLength = 200
        self.myGeometry = None
        self.myAIS_InteractiveObject = None

    def Compute(self):
        # self.myGeometry = Geom_SurfaceOfLinearExtrusion(self.myCurve, self.myVec)
        # face = BRepBuilderAPI_MakeFace()
        # face.Init(self.myGeometry, True, 1.0e-6)
        # face.Build()
        profile = BRepBuilderAPI_MakeEdge(self.myCurve).Edge()
        prism = BRepPrimAPI_MakePrism(profile, self.myVec * self.myLength).Shape()

        self.myAIS_InteractiveObject = AIS_Shape(prism)
        self.myContext.Display(self.myAIS_InteractiveObject, True)
        self.SetCenter(prism)
        self.InitClippingPlane()
    def SetCurves(self, theCurves):
        self.myCurve = theCurves

    def SetDirection(self, theAxis):
        self.myVec = theAxis

    def SetLength(self, theLength):
        self.myLength = theLength


