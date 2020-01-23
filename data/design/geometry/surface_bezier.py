from OCC.Core.Geom2d import *
from OCC.Core.AIS import *
from OCC.Core.Geom import *
from data.sketch.sketch_utils import *
from OCC.Core.gp import *
from OCC.Core.Aspect import *
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from OCC.Core.Prs3d import *
from data.sketch.sketch_object import *
from .surface_geometry import Surface_Geometry

class Surface_Bezier(Surface_Geometry):
    def __init__(self, theContext, theAxis):
        super(Surface_Bezier, self).__init__("Bezier surface", theContext, theAxis)
        self.myGeometry = None
        self.myAIS_InteractiveObject = None
