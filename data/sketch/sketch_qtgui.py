from data.sketch.sketch_propertyPoint import Sketch_PropertyPoint
from data.sketch.sketch_type import *


class Sketch_QTGUI(object):
    def __init__(self, parent=None):
        self.prop_point = Sketch_PropertyPoint(parent, "Point", True)
    def SetContext(self, theContext):
        self.prop_point.SetContext(theContext)

    def SetAx3(self, theAx3):
        self.prop_point.SetAx3(theAx3)

    def SetSketch_Object(self, CurObject):
        if not self.prop_point.isHidden():
            self.prop_point.close()
        if CurObject.GetGeometryType() == Sketch_GeometryType.PointSketcherObject:
            self.prop_point.SetObject(CurObject)
