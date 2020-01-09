from OCC.Core.BRepAdaptor import BRepAdaptor_Curve
from OCC.Core.GeomAbs import *
def recognize_edge(self, a_edge):
    """ Takes a TopoDS shape and tries to identify its nature
    whether it is a plane a cylinder a torus etc.
    if a plane, returns the normal
    if a cylinder, returns the radius
    """
    curve = BRepAdaptor_Curve(a_edge)
    curve_type = curve.GetType()
    if curve_type == GeomAbs_BezierCurve:
        print("--> Bezier")
        self._selectedShape = curve.Bezier()
    elif curve_type == GeomAbs_BSplineCurve:
        print("--> BSpline")
        self._selectedShape = curve.BSpline()
    elif curve_type == GeomAbs_Circle:
        print("--> Circle")
        self._selectedShape = Geom_Circle(curve.Circle())
    else:
        # TODO there are plenty other type that can be checked
        # see documentation for the BRepAdaptor class
        # https://www.opencascade.com/doc/occt-6.9.1/refman/html/class_b_rep_adaptor___surface.html
        print("not implemented")