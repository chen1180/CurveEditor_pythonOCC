from OCC.Core.Geom2d import *
from OCC.Core.AIS import *
from OCC.Core.Geom import *
from data.sketch.sketch_utils import *
from OCC.Core.gp import *
from OCC.Core.Aspect import *
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge,BRepBuilderAPI_MakeVertex
from OCC.Core.Prs3d import *
from data.sketch.sketch_object import *


class Sketch_Geometry:

    def __init__(self, name, theContext, theAxis):
        self.myGeometry = None
        self.myGeometry2d = None
        self.myAIS_InteractiveObject :AIS_InteractiveObject= None
        self.curCoordinateSystem: gp_Ax3 = theAxis
        self.myContext:AIS_InteractiveContext = theContext

        self.myName = name
        self.myGeometryType = None
        self.myTypeOfMethod = None


        self.myNameOfColor = Quantity_NOC_GREEN
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
        self.myPointWidth=5.0
        self.myPointAspect = Prs3d_PointAspect(self.myPointStyle, Quantity_Color(Quantity_NOC_BLUE1), self.myPointWidth)

        self.myLineStyle = Aspect_TOL_DOT
        self.myLineWidth = 1.0
        self.myLineAspect = Prs3d_LineAspect(Quantity_Color(Quantity_NOC_WHITE), self.myLineStyle, self.myLineWidth)

        self.myWireStyle = Aspect_TOL_SOLID
        self.myWireWidth = 2
        self.myWireAspect = Prs3d_LineAspect(Quantity_Color(self.myNameOfColor), self.myWireStyle, self.myWireWidth)

        self.myDrawer = Prs3d_Drawer()
        #for stright line
        self.myDrawer.SetLineAspect(self.myLineAspect)
        #for point
        self.myDrawer.SetPointAspect(self.myPointAspect)
        #for bezier curve or bspline
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

    def Display(self, theContext: AIS_InteractiveContext):
        pass

    def Redisplay(self, theContext: AIS_InteractiveContext):
        pass

    def RemoveDisplay(self):
        self.myContext.Remove(self.myAIS_InteractiveObject,True)