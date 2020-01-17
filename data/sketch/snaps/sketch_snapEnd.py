from data.sketch.snaps.sketch_snap import *
from data.sketch.geometry.geom2d_arc import Geom2d_Arc
from data.sketch.geometry.geom2d_edge import Geom2d_Edge


class Sketch_SnapEnd(Sketch_Snap):
    def __init__(self):
        super(Sketch_SnapEnd, self).__init__()

    def SelectEvent(self):
        self.findbestPnt2d = False
        self.minDistance = self.minimumSnapDistance
        for idx in range(len(self.data)):
            mySObject: Sketch_Object = self.data[idx]
            myGeometryType = mySObject.GetGeometryType()
            if myGeometryType == Sketch_GeometryType.PointSketchObject:
                self.curGeom2d_Point: Geom2d_CartesianPoint = mySObject.GetGeometry()
                self.objectPnt2d = self.curGeom2d_Point.Pnt2d()
                if self.count():
                    self.bestPnt2d = self.objectPnt2d
                    self.curHilightedObj = mySObject.GetAIS_Object()
            elif myGeometryType == Sketch_GeometryType.LineSketchObject:
                self.curGeom2d_Edge: Geom2d_Edge = mySObject.GetGeometry()
                self.objectPnt2d = self.curGeom2d_Edge.GetStart_Pnt()
                if self.count():
                    self.bestPnt2d = self.objectPnt2d
                    self.curHilightedObj = mySObject.GetAIS_Object()
                self.objectPnt2d = self.curGeom2d_Edge.GetEnd_Pnt()
                if self.count():
                    self.bestPnt2d = self.objectPnt2d
                    self.curHilightedObj = mySObject.GetAIS_Object()
            elif myGeometryType == Sketch_GeometryType.CurveSketchObject:
                self.curGeom2d_Curve: Geom2d_Curve = mySObject.GetGeometry()
                self.objectPnt2d = self.curGeom2d_Curve.Value(0.0)
                print(self.objectPnt2d)
                if self.count():
                    self.bestPnt2d = self.objectPnt2d
                    self.curHilightedObj = mySObject.GetAIS_Object()
                self.objectPnt2d = self.curGeom2d_Curve.Value(1.0)
                if self.count():
                    self.bestPnt2d = self.objectPnt2d
                    self.curHilightedObj = mySObject.GetAIS_Object()

            elif myGeometryType == Sketch_GeometryType.ArcSketchObject:
                self.curGeom2d_Arc: Geom2d_Arc = mySObject.GetGeometry()
                self.objectPnt2d = self.curGeom2d_Arc.FirstPnt()
                if self.count():
                    self.bestPnt2d = self.objectPnt2d
                    self.curHilightedObj = mySObject.GetAIS_Object()
                self.objectPnt2d = self.curGeom2d_Arc.LastPnt()
                if self.count():
                    self.bestPnt2d = self.objectPnt2d
                    self.curHilightedObj = mySObject.GetAIS_Object()
            elif myGeometryType == Sketch_GeometryType.CircleSketchObject:
                pass
        if self.minDistance == self.minimumSnapDistance:
            self.bestPnt2d = self.curPnt2d
        else:
            self.findbestPnt2d = True

    def GetSnapType(self) -> Sketcher_SnapType:
        return Sketcher_SnapType.SnapEnd
