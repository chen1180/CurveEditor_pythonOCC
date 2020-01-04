from data.sketch.snaps.sketch_snap import *
from OCC.Core.Geom2d import Geom2d_Circle


class Sketch_SnapCenter(Sketch_Snap):
    def __init__(self):
        super(Sketch_SnapCenter, self).__init__()


    def SelectEvent(self):
        self.findbestPnt2d = False
        self.minDistance = self.minimumSnapDistance
        for idx in range(len(self.data)):
            mySObject: Sketch_Object = self.data[idx]
            myGeometryType = mySObject.GetGeometryType()
            if myGeometryType == Sketch_ObjectGeometryType.PointSketcherObject or \
                    myGeometryType == Sketch_ObjectGeometryType.LineSketcherObject:
                pass
            elif myGeometryType == Sketch_ObjectGeometryType.CircleSketcherObject or myGeometryType == Sketch_ObjectGeometryType.ArcSketcherObject:
                self.curGeom2d_Circle: Geom2d_Circle = mySObject.GetGeometry()
                self.ProjectOnCurve.Init(self.curPnt2d, self.curGeom2d_Circle)
                if self.countProject():
                    self.bestPnt2d = self.curGeom2d_Circle.Location()
                    self.curHilightedObj = mySObject.GetAIS_Object()
                objectPnt2d = self.curGeom2d_Circle.Location()
                if self.count():
                    self.bestPnt2d = objectPnt2d.Location()
                    self.curHilightedObj = mySObject.GetAIS_Object()
        if self.minDistance == self.minimumSnapDistance:
            self.bestPnt2d = self.curPnt2d
        else:
            self.findbestPnt2d = True

    def GetSnapType(self) -> Sketcher_SnapType:
        return Sketcher_SnapType.SnapCenter
