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


class Surface_Bspline(Surface_Geometry):
    IndexCounter = 0

    def __init__(self, theContext):
        super(Surface_Bspline, self).__init__("Bspline surface", theContext)
        Surface_Bspline.IndexCounter += 1
        self.myName = self.myName + str(self.IndexCounter)
        self.myCurves = []
        self.myGeometry = None
        self.myAIS_InteractiveObject = None
        self.myStyle = GeomFill_StretchStyle

    def Compute(self):
        if len(self.myCurves) == 2:
            self.myGeometry = GeomFill_BSplineCurves(self.myCurves[0], self.myCurves[1], self.myStyle)
        elif len(self.myCurves) == 3:
            self.myGeometry = GeomFill_BSplineCurves(self.myCurves[0], self.myCurves[1], self.myCurves[2],
                                                    self.myStyle)
        elif len(self.myCurves) == 4:
            self.myGeometry = GeomFill_BSplineCurves(self.myCurves[0], self.myCurves[1], self.myCurves[2],
                                                    self.myCurves[3], self.myStyle)
        self.myGeometry = self.myGeometry.Surface()
        face = BRepBuilderAPI_MakeFace()
        face.Init(self.myGeometry, True, 1.0e-6)
        face.Build()
        face=face.Shape()
        self.myAIS_InteractiveObject = AIS_Shape(face)
        self.myContext.Display(self.myAIS_InteractiveObject, True)
        self.SetCenter(face)
        self.InitClippingPlane()

    def SetCurves(self, theCurves):
        self.myCurves = theCurves

    def SetStyle(self, theStyle):
        self.myStyle = theStyle
