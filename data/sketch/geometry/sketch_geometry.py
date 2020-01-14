from OCC.Core.Geom2d import *
from OCC.Core.AIS import *
from OCC.Core.Geom import *
from data.sketch.sketch_utils import *
from OCC.Core.gp import *
from OCC.Core.Aspect import *
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from data.sketch.sketch_object import *


class Sketch_Geometry:

    def __init__(self, name):
        self.myGeometry = None
        self.myGeometry2d = None
        self.myAIS_InteractiveObject = None
        self.curCoordinateSystem: gp_Ax3 = None

        self.myName = name
        self.myGeometryType = None
        self.myTypeOfMethod = None

        self.myNameOfColor = None
        self.myObjectType = AIS_SD_None
        self.myLineStyle = Aspect_TOL_SOLID
        self.myWidth = 1.0

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

    def GetGeometry2d(self):
        return self.myGeometry2d

    def GetName(self):
        return self.myName

    def GetGeometryType(self):
        pass

    def GetTypeOfMethod(self):
        pass

    def SetColor(self, theColor):
        self.myNameOfColor = theColor

    def GetColor(self):
        return self.myNameOfColor

    def SetType(self, theType):
        self.myObjectType = theType

    def GetType(self):
        return self.myObjectType

    def SetStyle(self, theLineStyle):
        self.myLineStyle = theLineStyle

    def GetStyle(self):
        return self.myLineStyle

    def SetWidth(self, theWidth):
        self.myWidth = theWidth

    def GetWidth(self):
        return self.myWidth

    def Display(self, theContext: AIS_InteractiveContext):
        pass

    def Redisplay(self, theContext: AIS_InteractiveContext):
        pass

    def RemoveDisplay(self, theContext: AIS_InteractiveContext):
        pass
