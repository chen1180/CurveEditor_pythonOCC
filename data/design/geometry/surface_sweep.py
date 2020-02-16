from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace
from data.sketch.sketch_object import *
from .surface_geometry import Surface_Geometry
from OCC.Core.GeomFill import *


class Surface_Sweep(Surface_Geometry):
    IndexCounter = 0

    def __init__(self, theContext, theAxis):
        super(Surface_Sweep, self).__init__("Sweep Surface", theContext, theAxis)
        Surface_Sweep.IndexCounter += 1
        self.myName = self.myName + str(self.IndexCounter)
        self.myProfile = None
        self.myPath = None
        self.myGeometry = None
        self.myAIS_InteractiveObject = None

    def Compute(self):
        self.myGeometry = GeomFill_Pipe(self.myPath, self.myProfile, self.myProfile)
        self.myGeometry.Perform()
        face = BRepBuilderAPI_MakeFace()
        face.Init(self.myGeometry.Surface(), True, 1.0e-6)
        face.Build()
        self.myAIS_InteractiveObject = AIS_Shape(face.Shape())
        self.myContext.Display(self.myAIS_InteractiveObject, True)

    def SetProfile(self, theProfile):
        self.myProfile = theProfile

    def SetPath(self, thePath):
        self.myPath = thePath
