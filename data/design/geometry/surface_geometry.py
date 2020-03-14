from OCC.Core.Geom2d import *
from OCC.Core.AIS import *
from OCC.Core.Geom import *
from data.sketch.sketch_utils import *
from OCC.Core.gp import *
from OCC.Core.Aspect import *
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from OCC.Core.Prs3d import *
from OCC.Core.GProp import GProp_GProps
from OCC.Core.BRepGProp import brepgprop_VolumeProperties, brepgprop_SurfaceProperties
from OCC.Core.Graphic3d import Graphic3d_ClipPlane, Graphic3d_Vec4d
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB


class Surface_Geometry:

    def __init__(self, name, theContext):
        self.myGeometry = None
        self.myAIS_InteractiveObject = None
        self.myContext = theContext
        self.myCenter = None

        self.myName = name
        self.myGeometryType = None
        self.myTypeOfMethod = None

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

    def RemoveDisplay(self):
        self.myContext.Remove(self.myAIS_InteractiveObject, True)
        if self.myAIS_ClippingPlane:
            self.myContext.Remove(self.myAIS_ClippingPlane, True)

    def Compute(self):
        pass

    def GetCenter(self):
        return self.myCenter

    def SetCenter(self, theShape):
        props = GProp_GProps()
        brepgprop_SurfaceProperties(theShape, props)
        cog = props.CentreOfMass()
        cog_x, cog_y, cog_z = cog.Coord()
        self.myCenter = gp_Pnt(cog_x, cog_y, cog_z)
        print("Center of mass: x = %f;y = %f;z = %f;" % (cog_x, cog_y, cog_z))

    def InitClippingPlane(self):
        # clip plane number one, by default xOy
        clip_plane = Graphic3d_ClipPlane(gp_Pln(self.myCenter, gp_Dir(1., 0., 0.)))
        # set hatch on
        clip_plane.SetCapping(True)
        clip_plane.SetCappingHatch(True)
        # off by default, user will have to enable it
        clip_plane.SetOn(True)
        # set clip plane color
        aMat = clip_plane.CappingMaterial()
        aColor = Quantity_Color(0.5, 0.6, 0.7, Quantity_TOC_RGB)
        aMat.SetAmbientColor(aColor)
        aMat.SetDiffuseColor(aColor)
        clip_plane.SetCappingMaterial(aMat)
        self.myClippingPlane = clip_plane
        self.myGeomClippingPlane = Geom_Plane(self.myClippingPlane.ToPlane())
        self.myAIS_ClippingPlane = AIS_Plane(self.myGeomClippingPlane)

    def OnClippingPlane(self, state):
        if state:
            self.myClippingPlane.SetOn(True)
            self.myAIS_InteractiveObject.AddClipPlane(self.myClippingPlane)
            self.myContext.Display(self.myAIS_ClippingPlane, True)
        else:
            self.myClippingPlane.SetOn(False)
            self.myAIS_InteractiveObject.RemoveClipPlane(self.myClippingPlane)
            self.myContext.Remove(self.myAIS_ClippingPlane, True)
        self.myContext.UpdateCurrentViewer()

    def UpdateClippingPlane(self, direction):
        tmp_plane = gp_Pln(self.myCenter, direction)
        equation = Graphic3d_ClipPlane(tmp_plane).GetEquation()
        self.myClippingPlane.SetEquation(equation)
        self.myGeomClippingPlane.SetPln(self.myClippingPlane.ToPlane())
        self.myAIS_ClippingPlane.SetComponent(self.myGeomClippingPlane)
        self.myContext.Redisplay(self.myAIS_ClippingPlane, True)
        self.myContext.UpdateCurrentViewer()

    def TranslateClippingPlane(self, direction):
        self.myGeomClippingPlane.Translate(direction)
        self.myClippingPlane.SetEquation(self.myGeomClippingPlane.Pln())
        self.myAIS_ClippingPlane.SetComponent(self.myGeomClippingPlane)
        self.myContext.Redisplay(self.myAIS_ClippingPlane, True)
        self.myContext.UpdateCurrentViewer()
