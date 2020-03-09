from data.design.commands import *
from data.design.part_type import *
from data.design.part_object import Part_Object
from OCC.Core.GeomAPI import GeomAPI_IntCS
from OCC.Core.V3d import V3d_View
from OCC.Core.Prs3d import Prs3d_LineAspect
from OCC.Core.AIS import AIS_InteractiveContext
from OCC.Display.OCCViewer import Viewer3d
from data.node import *


class Part(object):
    def __init__(self, theDisplay: Viewer3d, statusBar, sg=None):
        self.myDisplay = theDisplay
        self.myContext: AIS_InteractiveContext = theDisplay.Context
        self.myView: V3d_View = theDisplay.View
        self.myStatusBar = statusBar
        self.myGUI = sg
        self.myGUI.SetContext(self.myContext)
        self.myCurrentMethod = Part_ObjectTypeOfMethod.Nothing_Method

        self.myIntCS = GeomAPI_IntCS()

        self.myNode: SketchNode = None
        self.myModel = None

        self.myData = []
        self.myCommands = []
        self.addCommand(Part_CommandBezierSurface(self.myGUI))
        self.addCommand(Part_CommandRevolvedSurface(self.myGUI))
        self.addCommand(Part_CommandExtrudedSurface(self.myGUI))
        self.addCommand(Part_CommandSweepSurface(self.myGUI))

    def SetContext(self, theContext: AIS_InteractiveContext):
        self.myContext = theContext
        self.myGUI.SetContext(theContext)
        for idx in range(len(self.myCommands)):
            self.CurCommand: Part_Command = self.myCommands[idx]
            self.CurCommand.SetContext(self.myContext)

    def SetDisplay(self, theDisplay: Viewer3d):
        self.myDisplay = theDisplay
        for idx in range(len(self.myCommands)):
            self.CurCommand: Part_Command = self.myCommands[idx]
            self.CurCommand.SetDisplay(self.myDisplay)

    def SetData(self, thedata: list):
        self.myData = thedata
        for idx in range(len(self.myCommands)):
            self.CurCommand: Part_Command = self.myCommands[idx]
            self.CurCommand.SetData(self.myData)

    def SetRootNode(self, theNode):
        self.myNode = theNode
        for idx in range(len(self.myCommands)):
            self.CurCommand: Part_Command = self.myCommands[idx]
            self.CurCommand.SetRootNode(self.myNode)

    def SetModel(self, theModel):
        self.myModel = theModel
        self.myGUI.SetModel(self.myModel)
        for idx in range(len(self.myCommands)):
            self.CurCommand: Part_Command = self.myCommands[idx]
            self.CurCommand.SetModel(self.myModel)

    def GetData(self):
        return self.myData

    def GetCoordinateSystem(self):
        return self.myCoordinateSystem

    def SetPrecise(self, aPrecise: float):
        if aPrecise > 0:
            self.myAnalyserSnap.SetMinDistance(aPrecise)

    def SetStyle(self, theLineStyle: Prs3d_LineAspect):
        for idx in range(len(self.myCommands)):
            self.CurCommand: Part_Command = self.myCommands[idx]
            self.CurCommand.SetStyle(theLineStyle)

    def ObjectAction(self, theMethod: Part_ObjectTypeOfMethod):
        self.myCurrentMethod = theMethod
        self.myGUI.SetGui(theMethod)
        self.SelectCurCommand()
        self.CurCommand.Action()

    def GetStatus(self):
        return self.myCurrentMethod

    def OnMouseInputEvent(self, *kargs):
        theX, theY, buttons, modifier = kargs
        aView: V3d_View = self.myView
        self.SelectCurCommand()
        if self.CurCommand.MouseInputEvent(theX, theY, buttons, modifier):
            self.SelectCurCommand()
            self.myCurrentMethod = Part_ObjectTypeOfMethod.Nothing_Method

    def OnMouseMoveEvent(self, *kargs):
        theX, theY, buttons, modifier = kargs
        aView: V3d_View = self.myView
        self.SelectCurCommand()
        self.CurCommand.MouseMoveEvent(theX, theY, buttons, modifier)

    def OnCancel(self):
        self.SelectCurCommand()
        self.myGUI.Hide()
        self.CurCommand.CancelEvent()
        self.myCurrentMethod = Part_ObjectTypeOfMethod.Nothing_Method

    def DeleteSelectedObject(self):
        for index in range(self.myNode.childCount()):
            child = self.myNode.child(index)
            if isinstance(child, SketchObjectNode):
                myObject = child.getSketchObject()
                if self.myContext.IsSelected(myObject.GetAIS_Object()):
                    myObject.RemoveDisplay()
                    self.myNode.removeChild(index)
                    break

    def ViewProperties(self):
        for idx in range(len(self.myData)):
            myCurObject: Part_Object = self.myData[idx]
            if self.myContext.IsSelected(myCurObject.GetAIS_Object()):
                self.myContext.ClearSelected()
                self.myGUI.SetSketcher_Object(myCurObject)
                break

    def RedrawAll(self):
        for idx in range(len(self.myData)):
            myCurObject: Part_Object = self.myData[idx]
            if self.myContext.IsSelected(myCurObject.GetAIS_Object()):
                self.myContext.Display(myCurObject.GetAIS_Object(), True)

    def addCommand(self, theCommand: Part_Command):
        theCommand.SetData(self.myData)
        theCommand.SetDisplay(self.myDisplay)
        theCommand.SetStatusBar(self.myStatusBar)
        self.myCommands.append(theCommand)

    def SelectCurCommand(self):
        for idx in range(len(self.myCommands)):
            self.CurCommand: Part_Command = self.myCommands[idx]
            if self.CurCommand.GetTypeOfMethod() == self.myCurrentMethod:
                break
