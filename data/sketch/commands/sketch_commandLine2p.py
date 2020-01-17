from data.sketch.commands.sketch_command import *
from data.sketch.geometry.geom2d_edge import *
from OCC.Core.ElCLib import elclib
from OCC.Core.AIS import AIS_Point
from OCC.Core.Geom2d import Geom2d_CartesianPoint
from OCC.Core.Geom import Geom_CartesianPoint, Geom_Line
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from enum import Enum


class Line2PAction(Enum):
    Nothing = 0
    Input_FirstPointLine = 1
    Input_SecondPointLine = 2


class Sketch_CommandLine2P(Sketch_Command):
    def __init__(self):
        super(Sketch_CommandLine2P, self).__init__("Line2p.")
        self.myLine2PAction = Line2PAction.Nothing

    def Action(self):
        self.myLine2PAction = Line2PAction.Input_FirstPointLine

    def MouseInputEvent(self, thePnt2d: gp_Pnt2d, buttons, modifier):

        if self.myLine2PAction == Line2PAction.Nothing:
            pass
        elif self.myLine2PAction == Line2PAction.Input_FirstPointLine:
            self.curPnt2d = self.myAnalyserSnap.MouseInputException(thePnt2d, thePnt2d, TangentType.Line_FirstPnt, True)
            self.myFirstgp_Pnt2d = gp_Pnt2d(self.curPnt2d.X(),
                                            self.curPnt2d.Y())  # important to create new instance otherwise, this varible will be the copy of self.curPnt2d
            self.myFirstPoint.SetPnt(elclib.To3d(self.curCoordinateSystem.Ax2(), self.curPnt2d))
            self.myRubberLine.SetPoints(self.myFirstPoint, self.myFirstPoint)
            self.myContext.Display(self.myRubberLine, True)

            self.line = Sketch_Line(self.myContext,self.curCoordinateSystem)
            self.line.AddPoints(self.curPnt2d)

            self.myLine2PAction = Line2PAction.Input_SecondPointLine
        elif self.myLine2PAction == Line2PAction.Input_SecondPointLine:

            self.curPnt2d = self.myAnalyserSnap.MouseInputException(self.myFirstgp_Pnt2d, thePnt2d,
                                                                    TangentType.Line_SecondPnt, False)
            self.mySecondgp_Pn2d = gp_Pnt2d(self.curPnt2d.X(), self.curPnt2d.Y())
            self.line.AddPoints(self.curPnt2d)
            self.line.Compute()
            node = LineNode(self.objectName + str(self.objectCounter), self.rootNode)
            node.setSketchObject(self.line)
            self.AddObject(self.line.GetGeometry2d(),self.line.GetAIS_Object(), Sketch_GeometryType.LineSketchObject)
            if self.myPolylineMode:
                self.myFirstgp_Pnt2d = self.curPnt2d
                self.myFirstPoint.SetPnt(self.mySecondPoint.Pnt())
                self.myRubberLine.SetPoints(self.myFirstPoint, self.myFirstPoint)
                self.myContext.Redisplay(self.myRubberLine, True)
            else:
                self.myContext.Remove(self.myRubberLine, True)
                self.myLine2PAction = Line2PAction.Input_FirstPointLine
        return False

    def MouseMoveEvent(self, thePnt2d: gp_Pnt2d, buttons, modifiers):
        if self.myLine2PAction == Line2PAction.Nothing:
            pass
        elif self.myLine2PAction == Line2PAction.Input_FirstPointLine:
            self.curPnt2d = self.myAnalyserSnap.MouseMoveException(thePnt2d, thePnt2d, TangentType.Line_FirstPnt, True)

        elif self.myLine2PAction == Line2PAction.Input_SecondPointLine:
            self.curPnt2d = self.myAnalyserSnap.MouseMoveException(self.myFirstgp_Pnt2d, thePnt2d,
                                                                   TangentType.Line_SecondPnt, False)
            self.mySecondPoint.SetPnt(elclib.To3d(self.curCoordinateSystem.Ax2(), self.curPnt2d))

            self.myRubberLine.SetPoints(self.myFirstPoint, self.mySecondPoint)

            self.myContext.Redisplay(self.myRubberLine, True)

    def CancelEvent(self):
        if self.myLine2PAction == Line2PAction.Nothing:
            pass
        elif self.myLine2PAction == Line2PAction.Input_FirstPointLine:
            pass
        elif self.myLine2PAction == Line2PAction.Input_SecondPointLine:
            self.myContext.Remove(self.myRubberLine, True)
        self.myLine2PAction = Line2PAction.Nothing

    def GetTypeOfMethod(self) -> Sketch_ObjectTypeOfMethod:
        return Sketch_ObjectTypeOfMethod.Line2P_Method

    def SetPolylineFirstPnt(self, p1: gp_Pnt2d):
        self.myFirstgp_Pnt2d = p1
        self.myFirstPoint.SetPnt(elclib.To3d(self.curCoordinateSystem.Ax2(), p1))
        self.myRubberLine.SetPoints(self.myFirstPoint, self.myFirstPoint)
        self.myContext.Display(self.myRubberLine, 0, -1)
        self.myLine2PAction = Line2PAction.Input_SecondPointLine

    def GetPolylineFirstPnt(self, p1: gp_Pnt2d):
        if self.myLine2PAction == Line2PAction.Input_SecondPointLine and self.myPolylineMode == True:
            p1 = self.myFirstgp_Pnt2d
            return True
        else:
            return False

    def SetPolylineMode(self, mode):
        self.myPolylineMode = mode
