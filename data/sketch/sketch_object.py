from OCC.Core.AIS import *
from OCC.Core.Aspect import *

from OCC.Core.Quantity import *

from OCC.Core.Geom2d import *
from OCC.Core.TCollection import *
from OCC.Core.Standard import Standard_Transient
from data.sketch.sketch_type import *


class Sketch_Object(object):
    def __init__(self, theGeom2d_Geometry: Geom2d_Geometry, theAIS_InteractiveObject: AIS_InteractiveObject,
                 theName: str, theGeometryType: Sketch_GeometryType,
                 theTypeOfMethod: Sketch_ObjectTypeOfMethod):
        self.myGeometry = theGeom2d_Geometry
        self.myAIS_InteractiveObject = theAIS_InteractiveObject
        self.myName = theName
        self.myGeometryType = theGeometryType
        self.myTypeOfMethod = theTypeOfMethod

        self.myNameOfColor = Quantity_NOC_YELLOW
        self.myObjectType = Sketch_ObjectType.MainSketchType
        self.myLineStyle = Aspect_TOL_SOLID
        self.myWidth = 1.0
        # store temperary information about sketch object such as the poles of bezier curve or bspline
        self.myChildren = []

    def SetGeometry(self, theGeom2d_Geometry):
        self.myGeometry = theGeom2d_Geometry

    def GetGeometry(self):
        return self.myGeometry

    def SetAIS_Object(self, theAIS_InteractiveObject):
        self.myAIS_InteractiveObject = theAIS_InteractiveObject

    def GetAIS_Object(self):
        return self.myAIS_InteractiveObject

    def GetObjectName(self):
        return self.myName

    def SetGeometryType(self, theGeometryType):
        self.myGeometryType = theGeometryType

    def GetGeometryType(self):
        return self.myGeometryType

    def SetTypeOfMethod(self, theTypeOfMethod):
        self.myTypeOfMethod = theTypeOfMethod

    def GetTypeOfMethod(self):
        return self.myTypeOfMethod

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

    def SetObjectName(self, theName):
        self.myNameOfColor = theName

    def GetObjectName(self):
        return self.myName

    def AddChild(self, theObject):
        self.myChildren.append(theObject)

    def DeleteChild(self, theObject):
        self.myChildren.remove(theObject)

    def SetChildren(self, theChildren):
        self.myChildren = list(theChildren)

    def GetChildren(self) -> list:
        return self.myChildren

    def GetChild(self, index: int):
        return self.myChildren[index]
