from data.sketch.commands.sketch_command import *
from OCC.Core.ElCLib import elclib
from OCC.Core.AIS import AIS_Point
from OCC.Core.Geom2d import Geom2d_CartesianPoint
from enum import Enum


class PointAction(Enum):
    Nothing = 0
    Input_Point = 1


class Sketch_CommandPoint(Sketch_Command):
    def __init__(self):
        super(Sketch_CommandPoint, self).__init__("Point.")
        self.myPointAction = PointAction.Nothing

    def Action(self):
        self.myPointAction = PointAction.Input_Point

    def MouseInputEvent(self, thePnt2d: gp_Pnt2d):
        self.curPnt2d = self.myAnalyserSnap.MouseInput(thePnt2d)
        if self.myPointAction == PointAction.Nothing:
            pass
        elif self.myPointAction == PointAction.Input_Point:
            myGeom2d_Point = Geom2d_CartesianPoint(self.curPnt2d)
            myGeom_Point = Geom_CartesianPoint(elclib.To3d(self.curCoordinateSystem.Ax2(), self.curPnt2d))
            myAIS_Point = AIS_Point(myGeom_Point)
            self.myContext.Display(myAIS_Point, True)
            self.AddObject(myGeom2d_Point, myAIS_Point, Sketch_GeometryType.PointSketchObject)
            node = PointNode(self.objectName + str(self.objectCounter), self.rootNode)
            self.AddNode(node, myGeom2d_Point, myAIS_Point)
        return False

    def MouseMoveEvent(self, thePnt2d: gp_Pnt2d):
        self.curPnt2d = self.myAnalyserSnap.MouseMove(thePnt2d)

    def CancelEvent(self):
        # self.rootNode.removeChild(self.rootNode.childCount() - 1)
        self.myPointAction = PointAction.Nothing

    def GetTypeOfMethod(self) -> Sketch_ObjectTypeOfMethod:
        return Sketch_ObjectTypeOfMethod.Point_Method
