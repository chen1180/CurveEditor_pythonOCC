from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace
from data.sketch.sketch_object import *
from .surface_geometry import Surface_Geometry
from OCC.Core.GeomFill import *


class SweepConstructionMethod:
    Radius = 0
    ConstantSection = 1
    EvolvingSection = 2


class Surface_Sweep(Surface_Geometry):
    IndexCounter = 0

    def __init__(self, theContext):
        super(Surface_Sweep, self).__init__("Sweep Surface", theContext)
        Surface_Sweep.IndexCounter += 1
        self.myName = self.myName + str(self.IndexCounter)
        self.myGeometry = None
        self.myPath = None
        self.mySections = []
        self.myRadius = 50
        self.myConstructionMethod = SweepConstructionMethod.Radius
        self.myAIS_InteractiveObject = None

    def Compute(self):
        if self.myConstructionMethod == SweepConstructionMethod.Radius:
            myGeometry = GeomFill_Pipe(self.myPath, self.myRadius)
        elif self.myConstructionMethod == SweepConstructionMethod.ConstantSection:
            myGeometry = GeomFill_Pipe(self.myPath, self.mySections[0])
        elif self.myConstructionMethod == SweepConstructionMethod.EvolvingSection:
            myGeometry = GeomFill_Pipe(self.myPath, self.mySections[0], self.mySections[1])
        myGeometry.Perform()
        self.myGeometry = myGeometry.Surface()
        face = BRepBuilderAPI_MakeFace()
        face.Init(self.myGeometry, True, 1.0e-6)
        face.Build()
        face=face.Shape()
        self.myAIS_InteractiveObject = AIS_Shape(face)
        self.myContext.Display(self.myAIS_InteractiveObject, True)

        self.SetCenter(face)
        self.InitClippingPlane()


    def SetSections(self, theSection):
        self.mySections = theSection

    def SetPath(self, thePath):
        self.myPath = thePath

    def SetConstructionMethod(self, theMethod):
        self.myConstructionMethod = theMethod

    def SetRadius(self, theRadius):
        self.myRadius = theRadius
