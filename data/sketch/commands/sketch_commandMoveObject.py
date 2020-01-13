from data.sketch.commands.sketch_command import *
from OCC.Core.ElCLib import elclib
from OCC.Core.AIS import AIS_Point
from OCC.Core.Geom2d import Geom2d_CartesianPoint
from enum import Enum


class MoveAction(Enum):
    Nothing = 0
    Input_SelectedObject = 1


class Sketch_CommandMoveObject(Sketch_Command):
    def __init__(self):
        super(Sketch_CommandMoveObject, self).__init__("Move Object")
        self.myMoveAction = MoveAction.Nothing
        self.currentSObject: Sketch_Object = None

    def Action(self):
        self.myMoveAction = MoveAction.Input_SelectedObject

    def MouseInputEvent(self, thePnt2d: gp_Pnt2d, buttons, modifier):
        self.curPnt2d = self.myAnalyserSnap.MouseInput(thePnt2d)
        return False

    def MouseMoveEvent(self, thePnt2d: gp_Pnt2d, buttons, modifiers):
        self.curPnt2d = self.myAnalyserSnap.MouseMove(thePnt2d)
        if buttons == Qt.LeftButton:
            if self.myMoveAction == MoveAction.Nothing:
                if self.rootNode:
                    for obj in self.rootNode.children():
                        if type(obj) == PointNode:
                            myCurObject: Sketch_Object = obj.getSketchObject()
                            if self.myContext.IsSelected(myCurObject.GetAIS_Object()):
                                self.currentSObject = myCurObject
                                self.myMoveAction = MoveAction.Input_SelectedObject
                                break
                        elif type(obj) == BezierNode:
                            for subNodes in obj.children():
                                myCurObject: Sketch_Object = subNodes.getSketchObject()
                                if self.myContext.IsSelected(myCurObject.GetAIS_Object()):
                                    self.currentSObject = myCurObject
                                    self.myMoveAction = MoveAction.Input_SelectedObject
                                    break

            elif self.myMoveAction == MoveAction.Input_SelectedObject:
                self.UpdatePoint()

    def MouseReleaseEvent(self, buttons, modifiers):
        self.currentSObject = None
        self.myContext.ClearSelected(True)
        self.myMoveAction = MoveAction.Nothing

    def CancelEvent(self):
        self.myMoveAction = MoveAction.Nothing

    def GetTypeOfMethod(self) -> Sketch_ObjectTypeOfMethod:
        return Sketch_ObjectTypeOfMethod.Nothing_Method

    def UpdatePoint(self):
        if self.currentSObject:
            geometry: Geom2d_CartesianPoint = self.currentSObject.GetGeometry()
            geometry.SetPnt2d(self.curPnt2d)
            # print(geometry.X(), geometry.Y())
            curPoint = elclib.To3d(self.curCoordinateSystem.Ax2(), self.curPnt2d)
            curGeom_Point = Geom_CartesianPoint(curPoint)
            ais_point = self.currentSObject.GetAIS_Object()
            ais_point.SetComponent(curGeom_Point)
            ais_point.Redisplay(True)
