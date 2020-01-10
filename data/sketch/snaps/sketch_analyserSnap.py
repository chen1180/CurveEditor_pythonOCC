from data.sketch.snaps.sketch_snap import *
from OCC.Core.gp import *
from OCC.Core.AIS import *
from OCC.Core.TColStd import *
from data.sketch.sketch_type import *
from data.sketch.snaps.sketch_snapCenter import Sketch_SnapCenter
from data.sketch.snaps.sketch_snapEnd import Sketch_SnapEnd
from data.sketch.snaps.sketch_snapNearest import Sketch_SnapNearest
from OCC.Core.TColgp import *


class Sketch_AnalyserSnap(object):
    def __init__(self, theContext: AIS_InteractiveContext,
                 thedata: list,
                 theAx3: gp_Ax3):
        self.curCoordinateSystem = gp_Ax3(gp.XOY())
        self.myContext = theContext
        self.data = thedata
        self.curCoordinateSystem = theAx3

        self.myCurrentSnap = Sketcher_SnapType.SnapNothing
        self.mySnapAnType = Sketcher_SnapType.SnapNothing
        self.myPnt2d = gp.Origin2d()

        self.minimumSnapDistance = MINIMUMSNAP
        self.bestDist = 0
        self.curDist = 0

        self.storedPnt2d = gp.Origin2d()
        self.storedTangentType = TangentType.NothingTangent
        self.isTangent = False
        self.isLine = False

        self.mySnaps = []

        self.curSnapAnType = Sketcher_SnapType.SnapNothing

        self.mySeqOfPnt2d = TColgp_SequenceOfPnt2d()
        self.mySeqOfDistance = TColStd_SequenceOfReal()
        self.mySeqOfFactor = TColStd_SequenceOfReal()
        self.mySnapType = TColStd_SequenceOfInteger()

        self.addSnap(Sketch_SnapCenter())
        self.addSnap(Sketch_SnapEnd())
        self.addSnap(Sketch_SnapNearest())
    def SetContext(self, theContext):
        self.myContext = theContext
        for idx in range(len(self.mySnaps)):
            self.CurSnap = self.mySnaps[idx]
            self.CurSnap.SetContext(self.myContext)

    def SetData(self, thedata):
        self.data = thedata
        for idx in range(len(self.mySnaps)):
            self.CurSnap = self.mySnaps[idx]
            self.CurSnap.SetData(self.data)

    def SetAx3(self, theAx3: gp_Ax3):
        self.curCoordinateSystem = theAx3
        for idx in range(len(self.mySnaps)):
            self.CurSnap = self.mySnaps[idx]
            self.CurSnap.SetAx3(self.curCoordinateSystem)

    def SetMinDistance(self, aPrecise):
        self.minimumSnapDistance = aPrecise
        for idx in range(len(self.mySnaps)):
            self.CurSnap = self.mySnaps[idx]
            self.CurSnap.SetMinDistance(self.minimumSnapDistance)

    def SetSnapType(self, theSnap: Sketcher_SnapType):
        self.Cancel()
        self.myCurrentSnap = theSnap

    def GetSnapType(self):
        return self.myCurrentSnap

    def MouseInput(self, thePnt2d: gp_Pnt2d):
        self.myPnt2d = thePnt2d
        if (self.myCurrentSnap == Sketcher_SnapType.SnapEnd) or \
                (self.myCurrentSnap == Sketcher_SnapType.SnapMiddle) or \
                (self.myCurrentSnap == Sketcher_SnapType.SnapCenter) or \
                (self.myCurrentSnap == Sketcher_SnapType.SnapIntersection) or \
                (self.myCurrentSnap == Sketcher_SnapType.SnapNearest):
            self.SelectCurSnap()
            self.myPnt2d = self.CurSnap.MouseInputEvent(thePnt2d)
        elif self.myCurrentSnap == Sketcher_SnapType.SnapTangent:
            if self.isTangent:
                self.SelectCurSnap()
                self.CurSnap.setFirstPnt(self.storedPnt2d, self.storedTangentType)
                self.myPnt2d = self.CurSnap.MouseInputEvent(gp_Pnt2d)
        elif self.myCurrentSnap == Sketcher_SnapType.SnapParallel or self.myCurrentSnap == Sketcher_SnapType.SnapPerpendicular:
            if self.isLine:
                self.SelectCurSnap()
                self.CurSnap.setFirstPnt(self.storedPnt2d)
                self.myPnt2d = self.CurSnap.MouseInputEvent(gp_Pnt2d)
        elif self.myCurrentSnap == Sketcher_SnapType.SnapAnalyse:
            self.SnapAnalyserEvent()
            self.CurSnap.EraseSnap()
            self.mySnapAnType = Sketcher_SnapType.SnapNothing
        return self.myPnt2d

    def MouseMove(self, thePnt2d: gp_Pnt2d):
        self.myPnt2d = thePnt2d
        if (self.myCurrentSnap == Sketcher_SnapType.SnapEnd) or \
                (self.myCurrentSnap == Sketcher_SnapType.SnapMiddle) or \
                (self.myCurrentSnap == Sketcher_SnapType.SnapCenter) or \
                (self.myCurrentSnap == Sketcher_SnapType.SnapIntersection) or \
                (self.myCurrentSnap == Sketcher_SnapType.SnapNearest):
            self.SelectCurSnap()
            self.myPnt2d = self.CurSnap.MouseMoveEvent(thePnt2d)
        elif self.myCurrentSnap == Sketcher_SnapType.SnapTangent:
            if self.isTangent:
                self.SelectCurSnap()
                self.CurSnap.setFirstPnt(self.storedPnt2d, self.storedTangentType)
                self.myPnt2d = self.CurSnap.MouseMoveEvent(gp_Pnt2d)
        elif self.myCurrentSnap == Sketcher_SnapType.SnapParallel or self.myCurrentSnap == Sketcher_SnapType.SnapPerpendicular:
            if self.isLine:
                self.SelectCurSnap()
                self.CurSnap.setFirstPnt(self.storedPnt2d)
                self.myPnt2d = self.CurSnap.MouseMoveEvent(gp_Pnt2d)
        elif self.myCurrentSnap == Sketcher_SnapType.SnapAnalyse:
            self.SnapAnalyserEvent()
            if self.mySnapAnType != self.curSnapAnType:
                self.mySnapAnType = self.curSnapAnType
                self.CurSnap.EraseSnap()
            for idx in range(1, self.mySnaps.Length() + 1):
                self.CurSnap: Sketch_Snap = Sketch_Snap.DownCast(self.mySnaps.Value(idx))
                if self.CurSnap.GetSnapType() == self.mySnapAnType:
                    self.myPnt2d = self.CurSnap.MouseMoveEvent(thePnt2d)
        return self.myPnt2d

    def Cancel(self):
        self.SelectCurSnap()
        self.CurSnap.EraseSnap()
        self.mySnapAnType = Sketcher_SnapType.SnapNothing
        self.storedTangentType = TangentType.NothingTangent
        self.isTangent = False
        self.isLine = False

    def MouseInputException(self, p1: gp_Pnt2d, thePnt2d: gp_Pnt2d, CType: TangentType, TangentOnly: bool):
        if (self.myCurrentSnap == Sketcher_SnapType.SnapAnalyse) or \
                (self.myCurrentSnap == Sketcher_SnapType.SnapParallel) or \
                (self.myCurrentSnap == Sketcher_SnapType.SnapPerpendicular) or \
                (self.myCurrentSnap == Sketcher_SnapType.SnapTangent):
            self.storedPnt2d = p1
            self.storedTangentType = CType
            if TangentOnly == False:
                self.isLine = True
            self.MouseInput(thePnt2d)
            self.isTangent = False
            self.isLine = False
            return self.myPnt2d
        else:
            return self.MouseInput(thePnt2d)

    def MouseMoveException(self, p1: gp_Pnt2d, thePnt2d: gp_Pnt2d, CType: TangentType, TangentOnly: bool):
        if (self.myCurrentSnap == Sketcher_SnapType.SnapAnalyse) or \
                (self.myCurrentSnap == Sketcher_SnapType.SnapParallel) or \
                (self.myCurrentSnap == Sketcher_SnapType.SnapPerpendicular) or \
                (self.myCurrentSnap == Sketcher_SnapType.SnapTangent):
            self.storedPnt2d = p1
            self.storedTangentType = CType
            if TangentOnly == False:
                self.isLine = True
            self.MouseMove(thePnt2d)
            self.isTangent = False
            self.isLine = False
            return self.myPnt2d
        else:
            return self.MouseMove(thePnt2d)

    def SnapAnalyserEvent(self):
        self.bestDist = self.minimumSnapDistance * 10
        self.curDist = 0

        self.mySeqOfPnt2d.Clear()
        self.mySeqOfDistance.Clear()
        self.mySeqOfFactor.Clear()
        self.mySnapType.Clear()

        for idx in range(1, self.mySnaps.Length() + 1):
            self.CurSnap: Sketch_Snap = Sketch_Snap.DownCast(self.mySnaps.Value(idx))
            type = self.CurSnap.GetSnapType()
            if type == Sketcher_SnapType.SnapEnd:
                self.AddPoints(1)
            elif type == Sketcher_SnapType.SnapMiddle:
                self.AddPoints(3.5)
            elif type == Sketcher_SnapType.SnapCenter:
                self.AddPoints(4)
            elif type == Sketcher_SnapType.SnapIntersection:
                self.AddPoints(1)
            elif type == Sketcher_SnapType.SnapNearest:
                self.AddPoints(8)
            elif type == Sketcher_SnapType.SnapTangent:
                if self.isTangent:
                    self.CurSnap.setFirstPnt(self.storedPnt2d, self.storedTangentType)
                    self.AddPoints(1)
            elif type == Sketcher_SnapType.SnapParallel or type == Sketcher_SnapType.SnapPerpendicular:
                if self.isLine:
                    self.CurSnap.setFirstPnt(self.storedPnt2d)
                    self.AddPoints(8)
        self.curSnapAnType = Sketcher_SnapType.SnapNothing
        for idx in range(1, self.mySeqOfPnt2d.Length() + 1):
            self.curDist = self.mySeqOfPnt2d(idx) * self.mySeqOfFactor(idx)
            if self.bestDist > self.curDist:
                self.bestDist = self.curDist
                self.myPnt2d = self.mySeqOfPnt2d(idx)
                self.curSnapAnType = self.mySnapType(idx)
        for idx in range(1, self.mySnaps.Length() + 1):
            self.CurSnap: Sketch_Snap = Sketch_Snap.DownCast(self.mySnaps.Value(idx))
            if self.CurSnap.GetSnapType() == self.mySnapAnType:
                break

    def AddPoints(self, factor):
        findbestPnt2d, pt, distance, snaptype = self.CurSnap.AnalyserEvent(self.myPnt2d)
        if findbestPnt2d:
            self.mySeqOfPnt2d.Append(pt)
            self.mySeqOfDistance.Append(distance)
            self.mySeqOfFactor.Append(factor)
            self.mySnaps.Append(snaptype)

    def addSnap(self, theSnap: Sketch_Snap):
        theSnap.SetData(self.data)
        theSnap.SetContext(self.myContext)
        theSnap.SetAx3(self.curCoordinateSystem)
        self.mySnaps.append(theSnap)

    def SelectCurSnap(self):
        for idx in range(len(self.mySnaps)):
            self.CurSnap: Sketch_Snap = self.mySnaps[idx]
            if self.CurSnap.GetSnapType() == self.myCurrentSnap:
                break
