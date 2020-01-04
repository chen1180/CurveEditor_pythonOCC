from data.sketch.sketch_gui import *
from data.sketch.commands.sketch_commandPoint import *
from data.sketch.sketch_analyserSnap import *
from OCC.Core.GeomAPI import GeomAPI_IntCS
from OCC.Core.V3d import V3d_View


class Sketch(object):
    def __init__(self, theDisplay, sg: Sketch_GUI = None):
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
        self.myCommands = []

        self.myAnalyserSnap = Sketch_AnalyserSnap(self.myContext, self.myData, self.myCoordinateSystem)

        self.addCommand(Sketch_CommandPoint())

    def SetContext(self, theContext):
        self.myContext = theContext
        self.myAnalyserSnap.SetContext(self.myContext)
        self.myGUI.SetContext(theContext)
        for idx in range(1, self.myCommands.Length() + 1):
            self.CurCommand: Sketch_Command = Sketch_Command.DownCast(self.myCommands.Value(idx))
            self.CurCommand.SetContext(self.myContext)

    def SetData(self, thedata):
        self.myData = thedata
        for idx in range(1, self.myCommands.Length() + 1):
            self.CurCommand: Sketch_Command = Sketch_Command.DownCast(self.myCommands.Value(idx))
            self.CurCommand.SetData(self.myData)

    def GetData(self):
        return self.myData

    def SetCoordinateSystem(self, theCS):
        self.myCoordinateSystem = theCS
        self.myCurrentPlane.SetPosition(self.myCoordinateSystem)
        self.myAnalyserSnap.SetAx3(self.myCoordinateSystem)
        self.myGUI.SetAx3(self.myCoordinateSystem)
        for idx in range(len(self.myCommands)):
            self.CurCommand: Sketch_Command = self.myCommands[idx]
            self.CurCommand.SetAx3(self.myCoordinateSystem)

    def GetCoordinateSystem(self):
        return self.myCoordinateSystem

    def SetPrecise(self, aPrecise):
        if aPrecise > 0:
            self.myAnalyserSnap.SetMinDistance(aPrecise)

    def SetColor(self, theColor):
        for idx in range(len(self.myCommands)):
            self.CurCommand: Sketch_Command = self.myCommands[idx]
            self.CurCommand.SetColor(theColor)

    def SetType(self, theType):
        for idx in range(len(self.myCommands)):
            self.CurCommand: Sketch_Command = self.myCommands[idx]
            self.CurCommand.SetType(theType)

    def SetStyle(self, theLineStyle):
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
            print("current xy",self.myCurrentPnt2d.X(),self.myCurrentPnt2d.Y())
            return True
        else:
            return False

    def OnMouseInputEvent(self, *kargs):
        theX, theY = kargs
        aView: V3d_View = self.myView
        v3dX, v3dY, v3dZ, projVx, projVy, projVz = aView.ConvertWithProj(theX, theY)
        if self.ProjectPointOnPlane(v3dX, v3dY, v3dZ, projVx, projVy, projVz):
            self.SelectCurCommand()
            self.CurCommand.MouseInputEvent(self.myCurrentPnt2d)
            self.myCurrentMethod = Sketch_ObjectTypeOfMethod.Nothing_Method

    def OnMouseMoveEvent(self, *kargs):
        theX, theY = kargs
        aView: V3d_View = self.myView
        v3dX, v3dY, v3dZ, projVx, projVy, projVz = aView.ConvertWithProj(theX, theY)
        if self.ProjectPointOnPlane(v3dX, v3dY, v3dZ, projVx, projVy, projVz):
            self.SelectCurCommand()
            self.CurCommand.MouseMoveEvent(self.myCurrentPnt2d)
            self.myCurrentMethod = Sketch_ObjectTypeOfMethod.Nothing_Method

    def OnCancel(self):
        self.SelectCurCommand()
        self.myAnalyserSnap.Cancel()
        if (
                self.myCurrentMethod == Sketch_ObjectTypeOfMethod.Line2P_Method and self.myCurrentMethod == Sketch_ObjectTypeOfMethod.Arc3P_Method):
            self.PolylineFirstPointExist = self.CurCommand.GetPolylineFirstPnt(self.PolylineFirstPoint)
        self.CurCommand.CancelEvent()
        self.myCurrentMethod = Sketch_ObjectTypeOfMethod.Nothing_Method

    def DeleteSelectedObject(self):
        for idx in range(len(self.myData)):
            myCurObject: Sketch_Object = self.myData[idx]
            if self.myContext.IsSelected(myCurObject.GetAIS_Object()):
                self.myContext.Erase(myCurObject.GetAIS_Object(), True)
                self.myData.remove(idx)

    def ViewProperties(self):
        for idx in range(len(self.myData)):
            myCurObject: Sketch_Object = self.myData[idx]
            if self.myContext.IsSelected(myCurObject.GetAIS_Object()):
                self.myContext.ClearSelected()
                self.myGUI.SetSketcher_Object(myCurObject)
                break

    def RedrawAll(self):
        for idx in range(len(self.myData)):
            myCurObject: Sketch_Object = self.myData[idx]
            if self.myContext.IsSelected(myCurObject.GetAIS_Object()):
                self.myContext.Display(myCurObject.GetAIS_Object())

    def SetPolylineMode(self, amode):
        for idx in range(len(self.myCommands)):
            self.CurCommand: Sketch_Command = self.myCommands[idx]
            self.CurCommand.SetPolylineMode(amode)

    def SetSnap(self, theSnap):
        self.myAnalyserSnap.SetSnapType(theSnap)

    def GetSnap(self):
        return self.myAnalyserSnap.GetSnapType()

    def addCommand(self, theCommand: Sketch_Command):
        theCommand.SetData(self.myData)
        theCommand.SetContext(self.myContext)
        theCommand.SetAnalyserSnap(self.myAnalyserSnap)

        theCommand.SetAx3(self.myCoordinateSystem)
        self.myCommands.append(theCommand)

    def SelectCurCommand(self):
        for idx in range(len(self.myCommands)):
            self.CurCommand: Sketch_Command = self.myCommands[idx]
            if self.CurCommand.GetTypeOfMethod() == self.myCurrentMethod:
                break
