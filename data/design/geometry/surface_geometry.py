from OCC.Core.Geom2d import *
from OCC.Core.AIS import *
from OCC.Core.Geom import *
from data.sketch.sketch_utils import *
from OCC.Core.gp import *
from OCC.Core.Aspect import *
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from OCC.Core.Prs3d import *
from data.sketch.sketch_object import *


class Surface_Geometry:

    def __init__(self, name, theContext, theAxis):
        self.myGeometry = None
        self.myAIS_InteractiveObject = None
        self.curCoordinateSystem: gp_Ax3 = theAxis
        self.myContext = theContext

        self.myName = name
        self.myGeometryType = None
        self.myTypeOfMethod = None

    def SetAxis(self, theAxis):
        self.curCoordinateSystem = theAxis

    def SetContext(self, theContext):
        self.myContext: AIS_InteractiveContext = theContext

    def SetAIS_Object(self, theAIS_InteractiveObject):
        self.myAIS_InteractiveObject = theAIS_InteractiveObject

    def GetAIS_Object(self):
        return self.myAIS_InteractiveObject

    def GetGeometry(self):
        return self.myGeometry

    def GetName(self):
        return self.myName

    def GetGeometryType(self):
        pass

    def GetTypeOfMethod(self):
        pass

    def Display(self, theContext: AIS_InteractiveContext):
        pass

    def Redisplay(self, theContext: AIS_InteractiveContext):
        pass

    def RemoveDisplay(self, theContext: AIS_InteractiveContext):
        pass
