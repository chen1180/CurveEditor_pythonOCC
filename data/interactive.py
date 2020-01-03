from OCC.Core.Geom import *
from OCC.Core.gp import *
from OCC.Core.V3d import *
from OCC.Core.AIS import *
from OCC.Core.BRepPrimAPI import *
from OCC.Display.OCCViewer import Viewer3d
from OCC.Core.TopAbs import *
from OCC.Core.TopoDS import *
from OCC.Core.StdSelect import *
from OCC.Core.BRepAdaptor import *
from OCC.Core.BRep import *

class InteractiveEditor(object):
    def __init__(self,display):
        self._display=display
        self._context:AIS_InteractiveContext=display.Context
        self.points=[]
        self.First_Point=True
    def prepareContext(self):
        self._context.Deactivate()
        self.f1=AIS_SignatureFilter(AIS_KOI_Datum,AIS_SD_Line)
        self.f2=StdSelect_ShapeTypeFilter(TopAbs_VERTEX)
        self.f3 = StdSelect_ShapeTypeFilter(TopAbs_EDGE)
        self.f4 = StdSelect_ShapeTypeFilter(TopAbs_FACE)
        self.selectALLShapes()
        #Allows you to add the filter aFilter to Neutral Point or to a local context if one or more selection modes have been activated.
        #Only type filters may be active in Neutral Point.
        #at  this point, you can call the selection/detection function
    # def selection(self,xPix,yPix):
    #     try:
    #         if self._display.Context.HasDetected():
    #             self._display.Context.InitDetected()
    #             while (self._display.Context.MoreDetected()):
    #                 detected_object = self._display.Context.DetectedInteractive()
    #                 assert isinstance(detected_object, AIS_InteractiveObject)
    #                 self.setObject(detected_object)
    #                 self._display.Context.NextDetected()
    #     except Exception as e:
    #         print(e)
    def selectALLShapes(self):
        self._context.Activate(AIS_Shape.SelectionMode(TopAbs_EDGE))
        self._context.Activate(AIS_Shape.SelectionMode(TopAbs_FACE))
        self._context.Activate(AIS_Shape.SelectionMode(TopAbs_VERTEX))

    def moveTo(self,xPix,yPix):
        detect=self._display.MoveTo(xPix,yPix)
        self._context.Select(True)
        self._context.InitSelected()
        if self._context.MoreSelected():
            if self._context.HasSelectedShape():
                shape:TopoDS_Shape=self._context.SelectedShape()
                print("Interactive editor",shape)
                '''
                TopAbs_COMPOUND 	
                TopAbs_COMPSOLID 	
                TopAbs_SOLID 	
                TopAbs_SHELL 	
                TopAbs_FACE 	
                TopAbs_WIRE 	
                TopAbs_EDGE 	
                TopAbs_VERTEX 	
                TopAbs_SHAPE 
                '''
                # if shape.ShapeType() == TopAbs_VERTEX:
                #     if self.First_Point==True:
                #         self.points.append(shape)
                #         self._context.RemoveFilters()
                #         self._context.AddFilter(self.f2)
                #         self.First_Point=False
                #         return True
                #     else:
                #         self.points.append(shape)
                #         self.First_Point=True
                #         p1=BRep_Tool.Pnt(self.points[0])
                #         p1=Geom_CartesianPoint(p1)
                #         p2=BRep_Tool.Pnt(self.points[1])
                #         p2=Geom_CartesianPoint(p2)
                #         ais_line=AIS_Line(p1,p2)
                #         self._context.Display(ais_line,True)
                #         self.points.clear()
                #         self._context.RemoveFilters()
                #         # self._context.AddFilter(self.f1)
                #         return False
                # elif shape.ShapeType() == TopAbs_EDGE:
                #     if self.First_Point==True:
                #         self.points.append(shape)
                #         self._context.RemoveFilters()
                #         self._context.AddFilter(self.f3)
                #         self.First_Point=False
                #         return True
                #     else:
                #         self.First_Point = True
                #         self._context.RemoveFilters()
                #         return False
                # elif shape.ShapeType() == TopAbs_FACE:
                #     surface:Geom_Surface=BRep_Tool.Surface(shape)
                #     if type==Geom_Plane.get_type_descriptor():
                #         plane:Geom_Plane=Geom_Plane.DownCast(surface)
                #         # plane.SetLocation(gp_Pnt(0,100,10))
                #         ais_surface=AIS_PlaneTrihedron(plane)
                #         ais_surface.SetLength(100)
                #         self._context.Display(ais_surface,True)
                #     elif type==Geom_CylindricalSurface.get_type_descriptor():
                #         print("cylindrical surface detected")
    def terminate(self):
        # deactivate Local Selection
        self._context.Deactivate()
        self._context.Activate(0)