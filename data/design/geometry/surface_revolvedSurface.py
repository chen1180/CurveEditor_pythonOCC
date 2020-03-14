from OCC.Core.Geom2d import *
from OCC.Core.AIS import *
from OCC.Core.Geom import *
from data.sketch.sketch_utils import *
from OCC.Core.gp import *
from OCC.Core.Aspect import *
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakeEdge
from OCC.Core.Prs3d import *
from data.sketch.sketch_object import *
from OCC.Core.BRepPrimAPI import *
from OCC.Core.Geom import Geom_SurfaceOfRevolution
from .surface_geometry import Surface_Geometry
import math


class Surface_Revolved(Surface_Geometry):
    IndexCounter = 0

    def __init__(self, theContext):
        super(Surface_Revolved, self).__init__("Revolved Surface", theContext)
        Surface_Revolved.IndexCounter += 1
        self.myName = self.myName + str(self.IndexCounter)
        self.myCurve = None
        self.myRevolveAxis = None
        self.myGeometry = None
        self.myAngle = 360
        self.myAIS_InteractiveObject = None

    def Compute(self):
        # self.myGeometry = Geom_SurfaceOfRevolution(self.myCurve, self.myRevolveAxis)
        # face = BRepBuilderAPI_MakeFace()
        # face.Init(self.myGeometry, True, 1.0e-6)
        # face.Build()
        profile = self.myCurve.GetGeometry()
        axis = self.myRevolveAxis.GetGeometry().Position()
        edge = BRepBuilderAPI_MakeEdge(profile)
        shape = BRepPrimAPI_MakeRevol(edge.Edge(), axis, math.radians(self.myAngle)).Shape()

        self.myAIS_InteractiveObject = AIS_Shape(shape)
        self.myContext.Display(self.myAIS_InteractiveObject, True)
        self.SetCenter(shape)
        self.InitClippingPlane()
    def SetCurves(self, theCurves):
        self.myCurve = theCurves

    def SetRevolveAxis(self, theRevolveAxis):
        self.myRevolveAxis = theRevolveAxis

    def SetAngle(self, theDegree):
        self.myAngle = theDegree
