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


class Surface_Bezier(Surface_Geometry):
    def __init__(self, theContext, theAxis):
        super(Surface_Bezier, self).__init__("Bezier surface", theContext, theAxis)
        self.myCurves = []
        self.myGeometry = None
        self.myAIS_InteractiveObject = None

    def Compute(self):
        if len(self.myCurves) == 2:
            self.myGeometry = GeomFill_BezierCurves(self.myCurves[0], self.myCurves[1], GeomFill_CurvedStyle)
        elif len(self.myCurves) == 3:
            self.myGeometry = GeomFill_BezierCurves(self.myCurves[0], self.myCurves[1], self.myCurves[2],
                                                    GeomFill_CurvedStyle)
        elif len(self.myCurves) == 4:
            self.myGeometry = GeomFill_BezierCurves(self.myCurves[0], self.myCurves[1], self.myCurves[2],
                                                    self.myCurves[3], GeomFill_CurvedStyle)
        face = BRepBuilderAPI_MakeFace()
        face.Init(self.myGeometry.Surface(), True, 1.0e-6)
        face.Build()
        self.myAIS_InteractiveObject = AIS_Shape(face.Shape())
        self.myContext.Display(self.myAIS_InteractiveObject, True)

    def SetCurves(self, theCurves):
        self.myCurves = theCurves
