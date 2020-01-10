from data.sketch.snaps.sketch_snap import *
from data.sketch.geometry.geom2d_arc import Geom2d_Arc
from data.sketch.geometry.geom2d_edge import Geom2d_Edge


class Sketch_SnapNearest(Sketch_Snap):
    def __init__(self):
        super(Sketch_SnapNearest, self).__init__()

    def SelectEvent(self):
        self.findbestPnt2d = False
        self.minDistance = self.minimumSnapDistance
        for idx in range(len(self.data)):
            mySObject: Sketch_Object = self.data[idx]
            myGeometryType = mySObject.GetGeometryType()
            if myGeometryType == Sketch_GeometryType.PointSketchObject:
                pass
            elif myGeometryType == Sketch_GeometryType.LineSketchObject \
                    or myGeometryType == Sketch_GeometryType.CircleSketchObject \
                    or myGeometryType == Sketch_GeometryType.ArcSketchObject\
                    or myGeometryType==Sketch_GeometryType.CurveSketchObject:
                self.curGeom2d_Curve: Geom2d_Curve = mySObject.GetGeometry()
                self.ProjectOnCurve.Init(self.curPnt2d, self.curGeom2d_Curve)
                if self.countProject():
                    self.bestPnt2d = self.objectPnt2d
                    self.curHilightedObj = mySObject.GetAIS_Object()

        if self.minDistance == self.minimumSnapDistance:
            self.bestPnt2d = self.curPnt2d
        else:
            self.findbestPnt2d = True

    def GetSnapType(self) -> Sketcher_SnapType:
        return Sketcher_SnapType.SnapNearest
