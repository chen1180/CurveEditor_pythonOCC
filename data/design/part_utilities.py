from OCC.Core.BRepAdaptor import *
from OCC.Core.GeomAbs import *
from OCC.Core.TopoDS import *
from OCC.Core.TopAbs import *
from OCC.Core.BRep import *
from OCC.Core.Geom import *
from OCC.Core.GeomAPI import *
from OCC.Core.gp import *
from data.sketch.geometry import *


def shape_to_geometry(shape):
    """
    COMPOUND: A group of any of the shapes below.
    COMPSOLID: A set of solids connected by their faces. This expands the notions of WIRE and SHELL to solids.
    SOLID: A part of 3D space bounded by shells.
    SHELL: A set of faces connected by some of the edges of their wire boundaries. A shell can be open or closed.
    FACE: Part of a plane (in 2D geometry) or a surface (in 3D geometry) bounded by a closed wire. Its geometry is constrained (trimmed) by contours.
    WIRE: A sequence of edges connected by their vertices. It can be open or closed depending on whether the edges are linked or not.
    EDGE: A single dimensional shape corresponding to a curve, and bound by a vertex at each extremity.
    VERTEX: A zero-dimensional shape corresponding to a point in geometry.
    @param shape:
    @return:
    """
    if shape.ShapeType() == TopAbs_EDGE:
        edge = topods_Edge(shape)
        return recognize_edge(edge)
    elif shape.ShapeType() == TopAbs_FACE:
        surface = topods_Face(shape)
        return recognize_face(surface)
    elif shape.ShapeType() == TopAbs_VERTEX:
        return recognize_vertices(shape)
    else:
        return shape


def recognize_edge(a_edge):
    """ Takes a TopoDS shape and tries to identify its nature
    whether it is a plane a cylinder a torus etc.
    if a plane, returns the normal
    if a cylinder, returns the radius
    curve type:
        0:GeomAbs_Line
        1:GeomAbs_Circle
        2:GeomAbs_Ellipse
        3:GeomAbs_Hyperbola
        4:GeomAbs_Parabola
        5:GeomAbs_BezierCurve
        6:GeomAbs_BSplineCurve
        7:GeomAbs_OtherCurve
    """
    curve = BRepAdaptor_Curve(a_edge)
    curve_type = curve.GetType()
    if curve_type == GeomAbs_Line:
        print("--> Line", curve.Line())
        return curve.Value(curve.FirstParameter()), curve.Value(curve.LastParameter())
    elif curve_type == GeomAbs_BezierCurve:
        print("--> Bezier", curve.Bezier())
        return curve.Bezier()
    elif curve_type == GeomAbs_BSplineCurve:
        print("--> BSpline", curve.BSpline())
        return curve.BSpline()
    else:
        # see documentation for the BRepAdaptor class
        # https://www.opencascade.com/doc/occt-6.9.1/refman/html/class_b_rep_adaptor___surface.html
        print("not implemented")


def recognize_vertices(a_vertex):
    point = BRep_Tool.Pnt(a_vertex)
    print("--> Point", point)
    return Geom_CartesianPoint(point)


def recognize_face(a_surface):
    """ Takes a TopoDS shape and tries to identify its surface nature
    surface type:
        GeomAbs_Plane
        GeomAbs_Cylinder
        GeomAbs_Cone
        GeomAbs_Sphere
        GeomAbs_Torus
        GeomAbs_BezierSurface
        GeomAbs_BSplineSurface
        GeomAbs_SurfaceOfRevolution
        GeomAbs_SurfaceOfExtrusion
        GeomAbs_OffsetSurface
        GeomAbs_OtherSurface
    """
    surface = BRepAdaptor_Surface(a_surface)
    surface_type = surface.GetType()
    if surface_type == GeomAbs_Plane:
        print("--> Plane", surface.Plane())
        return surface.Plane()
    elif surface_type == GeomAbs_BezierSurface:
        print("--> Bezier surface", surface.Bezier())
        return  surface.Bezier()
    elif surface_type == GeomAbs_BSplineSurface:
        print("--> Bspline surface", surface.BSpline())
        return surface.BSpline()
    elif surface_type == GeomAbs_SurfaceOfRevolution:
        print("--> Revoluted surface")
        return surface
    elif surface_type == GeomAbs_SurfaceOfExtrusion:
        print("--> Extruded surface", surface.ChangeSurface())
        return surface
    else:
        # see documentation for the BRepAdaptor class
        # https://www.opencascade.com/doc/occt-6.9.1/refman/html/class_b_rep_adaptor___surface.html
        print("not implemented")
