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
from OCC.Core.GeomAbs import *
from OCC.Core.GeomFill import *


class InteractiveEditor(object):
    Filter_Edge = StdSelect_ShapeTypeFilter(TopAbs_EDGE)
    Filter_Vertex = StdSelect_ShapeTypeFilter(TopAbs_VERTEX)
    Filter_Face = StdSelect_ShapeTypeFilter(TopAbs_FACE)
    Filter_Datum_Line=AIS_SignatureFilter(AIS_KOI_Datum,AIS_SD_Line)
    Filter_Datum_Point = AIS_SignatureFilter(AIS_KOI_Datum, AIS_SD_Point)
    def __init__(self, display):
        self._display = display
        self._context: AIS_InteractiveContext = display.Context

        self.First_Point = True
        self.points = []
        self.curves = []

    def prepareContext_find_edge(self):
        self._context.Deactivate()
        self.selectALLShapes()
        self._context.AddFilter(self.Filter_Edge)
        # Allows you to add the filter aFilter to Neutral Point or to a local context if one or more selection modes have been activated.
        # Only type filters may be active in Neutral Point.
        # at  this point, you can call the selection/detection function

    def interaction_revolvedSurface(self, xPix, yPix):
        detect = self._display.MoveTo(xPix, yPix)
        self._context.Select(True)
        self._context.InitSelected()
        if self._context.MoreSelected():
            if self._context.HasSelectedShape():
                shape: TopoDS_Shape = self._context.SelectedShape()
                print("First select", shape)
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
                if shape.ShapeType() == TopAbs_VERTEX:
                    if self.First_Point == True:
                        self.points.append(shape)
                        self.First_Point = False
                        return True
                    else:
                        self.points.append(shape)
                        self.First_Point = True
                        axis = self.axis_FromTwoPoints()
                        self.makeSurfaceOfRevolution(self._selectedEdge, axis)
                        self.points.clear()
                        self._context.RemoveFilters()
                        self.terminateContext()
                        return False
                elif shape.ShapeType() == TopAbs_EDGE:
                    self._selectedEdge = self.convertEdge(shape)
                    self._context.RemoveFilters()
                    self._context.AddFilter(self.Filter_Vertex)
                    # self._context.AddFilter(self.Filter_Vertex)
                elif shape.ShapeType() == TopAbs_FACE:
                    surface: Geom_Surface = BRep_Tool.Surface(shape)
                    if type == Geom_Plane.get_type_descriptor():
                        plane: Geom_Plane = Geom_Plane.DownCast(surface)
                        # plane.SetLocation(gp_Pnt(0,100,10))
                        ais_surface = AIS_PlaneTrihedron(plane)
                        ais_surface.SetLength(100)
                        self._context.Display(ais_surface, True)
                    elif type == Geom_CylindricalSurface.get_type_descriptor():
                        print("cylindrical surface detected")
            else:
                SelObj = self._display.Context.SelectedInteractive()
                print(SelObj)
                '''
                signature 0 - Shape
                signature 1 - Point
                signature 2 - Axis
                signature 3 - Trihedron
                signature 4 - PlaneTrihedron
                signature 5 - Line
                signature 6 - Circle
                signature 7 - Plane
                '''
                if SelObj.Type() == AIS_KOI_Datum:
                    print(SelObj.Type(), SelObj.Signature())
                    # object=AIS_Trihedron.DownCast(SelObj)
                    # dir=object.Component().Ax2().Direction()
                    # print(dir.X(),dir.Y(),dir.Z())

    def interaction_bezierSurface(self, xPix, yPix):
        detect = self._display.MoveTo(xPix, yPix)
        self._context.Select(True)
        self._context.InitSelected()
        if self._context.MoreSelected():
            if self._context.HasSelectedShape():
                shape: TopoDS_Shape = self._context.SelectedShape()
                if shape.ShapeType() == TopAbs_EDGE:
                    self.curves.append(self.convertEdge(shape))
                    if len(self.curves) >= 2 and len(self.curves) <= 4:
                        self.makeSurfaceBezier(self.curves)
                        self.terminateContext()

    def makeSurfaceOfRevolution(self, curve, axis):
        if axis:
            surface = Geom_SurfaceOfRevolution(curve, axis)
            self._display.DisplayShape(surface)

    def makeSurfaceBezier(self, curves):
        if curves:
            if len(curves) == 2:
                surface = GeomFill_BezierCurves(curves[0], curves[1], GeomFill_CurvedStyle)
            elif len(curves) == 3:
                surface = GeomFill_BezierCurves(curves[0], curves[1], curves[2], GeomFill_CurvedStyle)
            elif len(curves) == 4:
                surface = GeomFill_BezierCurves(curves[0], curves[1], curves[2], curves[3], GeomFill_CurvedStyle)
            self._display.DisplayShape(surface.Surface())

    def convertEdge(self, edge):
        curve = BRepAdaptor_Curve(edge)
        curve_type = curve.GetType()
        if curve_type == GeomAbs_BezierCurve:
            return curve.Bezier()
        elif curve_type == GeomAbs_BSplineCurve:
            return curve.BSpline()
        elif curve_type == GeomAbs_Circle:
            return Geom_Circle(curve.Circle())

    def terminateContext(self):
        # deactivate Local Selection
        self.clearAllContents()
        self._context.RemoveFilters()
        self._context.Deactivate()
        self._context.Activate(0)

    def clearAllContents(self):
        self.curves.clear()
        self.points.clear()
    def selectALLShapes(self):
        self._context.Activate(AIS_Shape.SelectionMode(TopAbs_EDGE))
        self._context.Activate(AIS_Shape.SelectionMode(TopAbs_FACE))
        self._context.Activate(AIS_Shape.SelectionMode(TopAbs_VERTEX))
    def axis_FromTwoPoints(self):
        p1 = BRep_Tool.Pnt(self.points[0])
        p2 = BRep_Tool.Pnt(self.points[1])
        vec = gp_Vec(p1, p2)
        dir = gp_Dir(vec)
        axis = gp_Ax1(p1, dir)
        return axis
