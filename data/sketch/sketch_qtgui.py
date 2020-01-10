from data.sketch.sketch_propertyPoint import Sketch_PropertyPoint
from data.sketch.sketch_propertyLine import Sketch_PropertyLine
from data.sketch.sketch_type import *


class Sketch_QTGUI(object):
    def __init__(self, parent=None):
        self.prop_point = Sketch_PropertyPoint(parent, "Point", True)
        self.prop_line=Sketch_PropertyLine(parent,"Line",True)
    def SetContext(self, theContext):
        self.prop_point.SetContext(theContext)
        self.prop_line.SetContext(theContext)

    def SetAx3(self, theAx3):
        self.prop_point.SetAx3(theAx3)
        self.prop_line.SetAx3(theAx3)

    def SetSketch_Object(self, CurObject):
        if not self.prop_point.isHidden():
            self.prop_point.close()
        if not self.prop_line.isHidden():
            self.prop_line.close()
        if CurObject.GetGeometryType() == Sketch_GeometryType.PointSketchObject:
            self.prop_point.SetObject(CurObject)
        elif CurObject.GetGeometryType() == Sketch_GeometryType.LineSketchObject:
            self.prop_line.SetObject(CurObject)