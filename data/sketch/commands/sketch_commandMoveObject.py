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
        self.currentSObject: Sketch_Point = None
        self.object = None

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
                            myCurObject: Sketch_Point = obj.getSketchObject()
                            if self.myContext.IsSelected(myCurObject.GetAIS_Object()):
                                self.currentSObject = myCurObject
                                self.myMoveAction = MoveAction.Input_SelectedObject
                                self.object = myCurObject
                                break
                        elif type(obj) == BezierNode or type(obj)==BsplineNode:
                            myCurObject: Sketch_BezierCurve = obj.getSketchObject()
                            for pole in myCurObject.GetPoles():
                                if self.myContext.IsSelected(pole.GetAIS_Object()):
                                    self.currentSObject = pole
                                    self.myMoveAction = MoveAction.Input_SelectedObject
                                    self.object = myCurObject
                                    break
            elif self.myMoveAction == MoveAction.Input_SelectedObject:
                if self.currentSObject:
                    self.currentSObject.DragTo(self.curPnt2d)
                if type(self.object) == Sketch_BezierCurve or type(self.object)==Sketch_Bspline:
                    self.object.Recompute()
                elif type(self.object) == Sketch_Line:
                    self.object.Recompute()

    def MouseReleaseEvent(self, buttons, modifiers):
        self.currentSObject = None
        self.object = None
        self.myMoveAction = MoveAction.Nothing

    def CancelEvent(self):
        self.myMoveAction = MoveAction.Nothing

    def GetTypeOfMethod(self) -> Sketch_ObjectTypeOfMethod:
        return Sketch_ObjectTypeOfMethod.Move_Method
