from OCC.Core.Geom2d import *
from OCC.Core.AIS import *
from OCC.Core.Geom import *
from data.sketch.sketch_utils import *
from OCC.Core.gp import *
from OCC.Core.Aspect import *
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeVertex
from OCC.Core.Prs3d import *
from data.sketch.sketch_object import *


class Sketch_Geometry:

    def __init__(self, name, theContext, theAxis):
        self.myGeometry = None
        self.myGeometry2d = None
        self.myAIS_InteractiveObject: AIS_InteractiveObject = None
        self.myAIS_Name: AIS_TextLabel = None
        self.myAIS_Coordinate: AIS_TextLabel = None
        self.curCoordinateSystem: gp_Ax3 = theAxis
        self.myContext: AIS_InteractiveContext = theContext

        self.myName = name
        self.myGeometryType = None
        self.myTypeOfMethod = None

        # flags for showing object name and coordinate on screen
        self.showViewportName = False
        self.showViewportCoordinate = False
        self.showViewportObject = True
        self.showVieportAuxilirayLine = True

        self.myObjectType = AIS_SD_None
        '''
        Line style:
                    Aspect_TOL_SOLID 	
                    Aspect_TOL_DASH 	
                    Aspect_TOL_DOT 	
                    Aspect_TOL_DOTDASH 	
                    Aspect_TOL_USERDEFINED 
        '''
        self.myPointStyle = Aspect_TOM_O_POINT
        self.myPointWidth = 5.0
        self.myPointColor = Quantity_NOC_BLUE1
        self.myPointAspect = Prs3d_PointAspect(self.myPointStyle, Quantity_Color(self.myPointColor), self.myPointWidth)

        self.myLineStyle = Aspect_TOL_SOLID
        self.myLineWidth = 2.0
        self.myLineColor = Quantity_NOC_WHITE
        self.myLineAspect = Prs3d_LineAspect(Quantity_Color(self.myLineColor), self.myLineStyle, self.myLineWidth)

        self.myWireStyle = Aspect_TOL_SOLID
        self.myWireWidth = 3.0
        self.myWireColor = Quantity_NOC_GREEN
        self.myWireAspect = Prs3d_LineAspect(Quantity_Color(self.myWireColor), self.myWireStyle, self.myWireWidth)

        self.myDrawer = Prs3d_Drawer()
        # for stright line
        self.myDrawer.SetLineAspect(self.myLineAspect)
        # for point
        self.myDrawer.SetPointAspect(self.myPointAspect)
        # for bezier curve or bspline
        self.myDrawer.SetWireAspect(self.myWireAspect)

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

    def GetType(self):
        return self.myObjectType

    def GetColor(self):
        pass

    def SetColor(self, theColor):
        pass

    def GetWidth(self):
        pass

    def SetWidth(self, theWidth):
        pass

    def GetStyle(self):
        pass

    def SetStyle(self, theStyle):
        pass

    def Display(self, theContext: AIS_InteractiveContext):
        pass

    def Redisplay(self, theContext: AIS_InteractiveContext):
        pass

    def RemoveLabel(self):
        pass

    def RemoveDisplay(self):
        self.myContext.Remove(self.myAIS_InteractiveObject, True)

    def DisplayName(self):
        pass

    def DisplayCoordinate(self):
        pass

    def DisplayObject(self):
        if self.showViewportObject == True:
            self.myContext.Display(self.GetAIS_Object(), True)
        else:
            self.myContext.Erase(self.GetAIS_Object(), True)

    def DisplayAuxiliryLine(self):
        pass
