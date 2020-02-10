from data.sketch.commands import *
from data.sketch.gui.sketch_qtgui import Sketch_QTGUI
from data.sketch.snaps.sketch_analyserSnap import *
from OCC.Core.GeomAPI import GeomAPI_IntCS
from OCC.Core.V3d import V3d_View
from OCC.Core.Geom import Geom_Line
from OCC.Core.Prs3d import Prs3d_LineAspect
from data.node import *


class Sketch(object):
    def __init__(self, theDisplay, sg: Sketch_QTGUI = None):
        self.myCoordinateSystem = gp_Ax3(gp.XOY())
        self.myContext: AIS_InteractiveContext = theDisplay.Context
        self.myView: V3d_View = theDisplay.View
        self.myGUI = sg
        self.myGUI.SetAx3(self.myCoordinateSystem)
        self.myGUI.SetContext(self.myContext)

        self.myCurrentMethod = Sketch_ObjectTypeOfMethod.Nothing_Method

        self.myCurrentDir: gp_Dir = gp.DZ()
        self.myTempPnt: gp_Pnt = gp.Origin()
        self.myCurrentPnt2d: gp_Pnt2d = gp.Origin2d()
        self.myCurrentPlane = Geom_Plane(self.myCoordinateSystem)
        self.myCurrentLine = Geom_Line(self.myTempPnt, self.myCurrentDir)

        self.myIntCS = GeomAPI_IntCS()

        self.PolylineFirstPoint = gp.Origin2d()
        self.PolylineFirstPointExist = False

        self.myData = []
        self.myNode: SketchObjectNode = None
        self.myCommands = []

        self.myAnalyserSnap = Sketch_AnalyserSnap(self.myContext, self.myData, self.myCoordinateSystem)

        self.addCommand(Sketch_CommandPoint())
        self.addCommand(Sketch_CommandLine2P())
        self.addCommand(Sketch_CommandBezierCurve())
        self.addCommand(Sketch_CommandArc3P())
        self.addCommand(Sketch_CommandCircleCenterRadius())
        self.addCommand(Sketch_CommandBSpline())
        self.addCommand(Sketch_CommandPointToBSpline())
        self.addCommand(Sketch_CommandMoveObject())
        self.addCommand(Sketch_CommandNurbCircle())

    def SetContext(self, theContext: AIS_InteractiveContext):
        self.myContext = theContext
        self.myAnalyserSnap.SetContext(self.myContext)
        self.myGUI.SetContext(theContext)
        for idx in range(len(self.myCommands)):
            self.CurCommand: Sketch_Command = self.myCommands[idx]
            self.CurCommand.SetContext(self.myContext)

    def SetData(self, thedata: list):
        self.myData = thedata
        for idx in range(len(self.myCommands)):
            self.CurCommand: Sketch_Command = self.myCommands[idx]
            self.CurCommand.SetData(self.myData)

    def SetRootNode(self, theNode):
        self.myNode = theNode
        for idx in range(len(self.myCommands)):
            self.CurCommand: Sketch_Command = self.myCommands[idx]
            self.CurCommand.SetRootNode(self.myNode)

    def GetData(self):
        return self.myData

    def SetCoordinateSystem(self, theCS: gp_Ax3):
        self.myCoordinateSystem = theCS
        self.myCurrentPlane.SetPosition(self.myCoordinateSystem)
        self.myAnalyserSnap.SetAx3(self.myCoordinateSystem)
        self.myGUI.SetAx3(self.myCoordinateSystem)
        for idx in range(len(self.myCommands)):
            self.CurCommand: Sketch_Command = self.myCommands[idx]
            self.CurCommand.SetAx3(self.myCoordinateSystem)

    def GetCoordinateSystem(self):
        return self.myCoordinateSystem

    def SetPrecise(self, aPrecise: float):
        if aPrecise > 0:
            self.myAnalyserSnap.SetMinDistance(aPrecise)

    def SetColor(self, theColor: Quantity_Color):
        for idx in range(len(self.myCommands)):
            self.CurCommand: Sketch_Command = self.myCommands[idx]
            self.CurCommand.SetColor(theColor)

    def SetType(self, theType: Sketch_ObjectType):
        for idx in range(len(self.myCommands)):
            self.CurCommand: Sketch_Command = self.myCommands[idx]
            self.CurCommand.SetType(theType)

    def SetStyle(self, theLineStyle: Prs3d_LineAspect):
        for idx in range(len(self.myCommands)):
            self.CurCommand: Sketch_Command = self.myCommands[idx]
            self.CurCommand.SetStyle(theLineStyle)

    def ObjectAction(self, theMethod: Sketch_ObjectTypeOfMethod):
        self.myCurrentMethod = theMethod
        self.SelectCurCommand()
        self.CurCommand.Action()
        if (
                self.myCurrentMethod == Sketch_ObjectTypeOfMethod.Line2P_Method or self.myCurrentMethod == Sketch_ObjectTypeOfMethod.Arc3P_Method) and self.PolylineFirstPointExist:
            self.CurCommand.SetPolylineFirstPnt(self.PolylineFirstPoint)
        else:
            self.PolylineFirstPointExist = False

    def GetStatus(self):
        return self.myCurrentMethod

    def ProjectPointOnPlane(self, v3dX, v3dY, v3dZ, projVx, projVy, projVz):
        self.myTempPnt.SetCoord(v3dX, v3dY, v3dZ)
        self.myCurrentDir.SetCoord(projVx, projVy, projVz)

        self.myCurrentLine.SetDirection(self.myCurrentDir)
        self.myCurrentLine.SetLocation(self.myTempPnt)

        self.myIntCS.Perform(self.myCurrentLine, self.myCurrentPlane)  # perfrom intersection calculation
        if self.myIntCS.NbPoints() >= 1:
            self.myTempPnt = self.myIntCS.Point(1)
            self.myCurrentPnt2d.SetX((
                                             self.myTempPnt.X() - self.myCoordinateSystem.Location().X()) * self.myCoordinateSystem.XDirection().X() + (
                                             self.myTempPnt.Y() - self.myCoordinateSystem.Location().Y()) * self.myCoordinateSystem.XDirection().Y() + (
                                             self.myTempPnt.Z() - self.myCoordinateSystem.Location().Z()) * self.myCoordinateSystem.XDirection().Z())
            self.myCurrentPnt2d.SetY(
                (
                        self.myTempPnt.X() - self.myCoordinateSystem.Location().X()) * self.myCoordinateSystem.YDirection().X() + (
                        self.myTempPnt.Y() - self.myCoordinateSystem.Location().Y()) * self.myCoordinateSystem.YDirection().Y() + (
                        self.myTempPnt.Z() - self.myCoordinateSystem.Location().Z()) * self.myCoordinateSystem.YDirection().Z())
            return True
        else:
            return False

    def OnMouseInputEvent(self, *kargs):
        theX, theY, buttons, modifier = kargs
        aView: V3d_View = self.myView
        v3dX, v3dY, v3dZ, projVx, projVy, projVz = aView.ConvertWithProj(theX, theY)
        if self.ProjectPointOnPlane(v3dX, v3dY, v3dZ, projVx, projVy, projVz):
            self.SelectCurCommand()
            if self.CurCommand.MouseInputEvent(self.myCurrentPnt2d, buttons, modifier):
                self.myCurrentMethod = Sketch_ObjectTypeOfMethod.Nothing_Method

    def OnMouseMoveEvent(self, *kargs):
        theX, theY, buttons, modifier = kargs
        aView: V3d_View = self.myView
        v3dX, v3dY, v3dZ, projVx, projVy, projVz = aView.ConvertWithProj(theX, theY)
        if self.ProjectPointOnPlane(v3dX, v3dY, v3dZ, projVx, projVy, projVz):
            self.SelectCurCommand()
            self.CurCommand.MouseMoveEvent(self.myCurrentPnt2d, buttons, modifier)

    def OnMouseReleaseEvent(self, *kargs):
        buttons, modifier = kargs
        self.SelectCurCommand()
        self.CurCommand.MouseReleaseEvent(buttons, modifier)

    def GetCurPoint2D(self):
        return self.myCurrentPnt2d

    def GetCurPoint3D(self):
        return elclib.To3d(self.myCoordinateSystem.Ax2(), self.myCurrentPnt2d)

    def OnCancel(self):
        self.SelectCurCommand()
        self.myAnalyserSnap.Cancel()
        if (
                self.myCurrentMethod == Sketch_ObjectTypeOfMethod.Line2P_Method and self.myCurrentMethod == Sketch_ObjectTypeOfMethod.Arc3P_Method):
            self.PolylineFirstPointExist = self.CurCommand.GetPolylineFirstPnt(self.PolylineFirstPoint)
        self.CurCommand.CancelEvent()
        self.myCurrentMethod = Sketch_ObjectTypeOfMethod.Nothing_Method
        # for all the sketch object selectable
        self.myContext.Deactivate()
        self.myContext.Activate(0)

    def DeleteSelectedObject(self):
        index = 0
        while index < self.myNode.childCount():
            child = self.myNode.child(index)
            assert isinstance(child, SketchObjectNode)
            myCurObject: Sketch_Geometry = child.getSketchObject()
            if self.myContext.IsSelected(myCurObject.GetAIS_Object()):
                myCurObject.RemoveDisplay()
                self.myNode.removeChild(index)
            else:
                index += 1

    def ViewProperties(self):
        # for idx in range(len(self.myData)):
        #     myCurObject: Sketch_Object = self.myData[idx]
        #     if self.myContext.IsSelected(myCurObject.GetAIS_Object()):
        #         self.myContext.ClearSelected(True)
        #         self.myGUI.SetSketch_Object(myCurObject)
        #         break
        for child in self.myNode.children():
            assert isinstance(child, SketchObjectNode)
            myCurObject: Sketch_Geometry = child.getSketchObject()
            if self.myContext.IsSelected(myCurObject.GetAIS_Object()):
                self.myContext.ClearSelected(True)
                self.myGUI.SetSketch_Object(myCurObject)
                break

    def RedrawAll(self):
        for idx in range(len(self.myData)):
            myCurObject: Sketch_Object = self.myData[idx]
            if self.myContext.IsSelected(myCurObject.GetAIS_Object()):
                self.myContext.Display(myCurObject.GetAIS_Object(), True)

    def SetPolylineMode(self, amode):
        for idx in range(len(self.myCommands)):
            self.CurCommand = self.myCommands[idx]
            self.CurCommand.SetPolylineMode(amode)

    def SetSnap(self, theSnap):
        self.myAnalyserSnap.SetSnapType(theSnap)

    def GetSnap(self):
        return self.myAnalyserSnap.GetSnapType()

    def addCommand(self, theCommand: Sketch_Command):
        theCommand.SetData(self.myData)
        theCommand.SetContext(self.myContext)
        theCommand.SetRootNode(self.myNode)
        theCommand.SetAnalyserSnap(self.myAnalyserSnap)

        theCommand.SetAx3(self.myCoordinateSystem)
        self.myCommands.append(theCommand)

    def SelectCurCommand(self):
        for idx in range(len(self.myCommands)):
            self.CurCommand: Sketch_Command = self.myCommands[idx]
            if self.CurCommand.GetTypeOfMethod() == self.myCurrentMethod:
                break
