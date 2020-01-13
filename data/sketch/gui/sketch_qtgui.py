from data.sketch.gui.sketch_propertyPoint import Sketch_PropertyPoint
from data.sketch.gui.sketch_propertyLine import Sketch_PropertyLine
from data.sketch.gui.sketch_propertyBezierCurve import Sketch_PropertyBezierCurve
from data.sketch.sketch_type import *


class Sketch_QTGUI(object):
    def __init__(self, parent=None):
        self.prop_point = Sketch_PropertyPoint(parent, "Point", True)
        self.prop_line = Sketch_PropertyLine(parent, "Line", True)
        self.prop_bezierCurve = Sketch_PropertyBezierCurve(parent, "Bezier curve", True)

    def SetContext(self, theContext):
        self.prop_point.SetContext(theContext)
        self.prop_line.SetContext(theContext)
        self.prop_bezierCurve.SetContext(theContext)

    def SetAx3(self, theAx3):
        self.prop_point.SetAx3(theAx3)
        self.prop_line.SetAx3(theAx3)
        self.prop_bezierCurve.SetAx3(theAx3)

    def SetSketch_Object(self, CurObject):
        if not self.prop_point.isHidden():
            self.prop_point.close()
        if not self.prop_line.isHidden():
            self.prop_line.close()
        if not self.prop_bezierCurve.isHidden():
            self.prop_bezierCurve.close()
        if CurObject.GetGeometryType() == Sketch_GeometryType.PointSketchObject:
            self.prop_point.SetObject(CurObject)
        elif CurObject.GetGeometryType() == Sketch_GeometryType.LineSketchObject:
            self.prop_line.SetObject(CurObject)
        elif CurObject.GetGeometryType() == Sketch_GeometryType.CurveSketchObject:
            if CurObject.GetTypeOfMethod()==Sketch_ObjectTypeOfMethod.BezierCurve_Method:
                self.prop_bezierCurve.SetObject(CurObject)
