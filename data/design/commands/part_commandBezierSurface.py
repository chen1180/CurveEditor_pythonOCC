from data.design.commands.part_command import *
from data.design.gui import bezierSurfaceForm


class BezierSurfaceAction(Enum):
    Nothing = 0
    Input_Curve1 = 1
    Input_Curve2 = 2
    Input_Curve3 = 3
    Input_Curve4 = 4

class Part_CommandBezierSurface(Part_Command):
    def __init__(self,gui):
        super(Part_CommandBezierSurface, self).__init__("BezierSurface.")
        self.myCurves = []
        self.myGUI: part_qtgui.Part_QTGUI = gui
        self.myAxis = gp_Ax1()
        self.myGeomSurface = None
        self.myRubberSurface = None
        self.myBezierSurfaceAction = BezierSurfaceAction.Nothing

    def Action(self):
        self.myBezierSurfaceAction = BezierSurfaceAction.Input_Curve1

    def MouseInputEvent(self, xPix, yPix, buttons, modifier):
        myObjects = self.SelectObject(xPix, yPix)
        if myObjects is None:
            return False
        if myObjects.Type() == AIS_KOI_Shape:
            curve = self.FindGeometry(myObjects)
            # if curve:
            #     if type(curve) == Geom_BSplineCurve:
            #         raise Exception("Curve must be bezier type")
            #     if self.myBezierSurfaceAction == BezierSurfaceAction.Nothing:
            #         pass
            #     elif self.myBezierSurfaceAction == BezierSurfaceAction.Input_Curve1:
            #         self.myCurves.append(curve)
            #         self.myBezierSurfaceAction = BezierSurfaceAction.Input_Curve2
            #     elif self.myBezierSurfaceAction == BezierSurfaceAction.Input_Curve2:
            #         self.myCurves.append(curve)
            #         surface1 = GeomFill_BezierCurves(self.myCurves[0], curve, GeomFill_CurvedStyle)
            #         face = BRepBuilderAPI_MakeFace()
            #         face.Init(surface1.Surface(), True, 1.0e-6)
            #         face.Build()
            #
            #         self.myRubberSurface = AIS_Shape(face.Shape())
            #         self.myContext.Display(self.myRubberSurface, True)
            #         self.myBezierSurfaceAction = BezierSurfaceAction.Input_Curve3
            #     elif self.myBezierSurfaceAction == BezierSurfaceAction.Input_Curve3:
            #         self.myCurves.append(curve)
            #         surface1 = GeomFill_BezierCurves(self.myCurves[0], self.myCurves[1], curve, GeomFill_CurvedStyle)
            #         face = BRepBuilderAPI_MakeFace()
            #         face.Init(surface1.Surface(), True, 1.0e-6)
            #         face.Build()
            #         self.myRubberSurface.SetShape(face.Shape())
            #         self.myContext.Redisplay(self.myRubberSurface, True)
            #         self.myBezierSurfaceAction = BezierSurfaceAction.Input_Curve4
            #     elif self.myBezierSurfaceAction == BezierSurfaceAction.Input_Curve4:
            #         self.myCurves.append(curve)
            #         surface1 = GeomFill_BezierCurves(self.myCurves[0], self.myCurves[1], self.myCurves[2], curve,
            #                                          GeomFill_CurvedStyle)
            #         face = BRepBuilderAPI_MakeFace()
            #         face.Init(surface1.Surface(), True, 1.0e-6)
            #         face.Build()
            #         self.myRubberSurface.SetShape(face.Shape())
            #         self.myContext.Redisplay(self.myRubberSurface, True)
            #         self.CloseSurface()
            #         self.myBezierSurfaceAction = BezierSurfaceAction.Nothing

    def MouseMoveEvent(self, xPix, yPix, buttons, modifier):
        myObjects = self.DetectObject(xPix, yPix)
        if self.myBezierSurfaceAction == BezierSurfaceAction.Nothing:
            pass
        elif self.myBezierSurfaceAction == BezierSurfaceAction.Input_Curve1:
            self.myStatusBar.showMessage("select 1st bezier curve!", 1000)
        elif self.myBezierSurfaceAction == BezierSurfaceAction.Input_Curve2:
            self.myStatusBar.showMessage("select 2nd bezier curve!", 1000)
        elif self.myBezierSurfaceAction == BezierSurfaceAction.Input_Curve3:
            self.myStatusBar.showMessage("select 3rd bezier curve!", 1000)
        elif self.myBezierSurfaceAction == BezierSurfaceAction.Input_Curve4:
            self.myStatusBar.showMessage("select 4th bezier curve!", 1000)

    def CancelEvent(self):
        if self.myBezierSurfaceAction == BezierSurfaceAction.Nothing:
            pass
        elif self.myBezierSurfaceAction == BezierSurfaceAction.Input_Curve1:
            pass
        elif self.myBezierSurfaceAction == BezierSurfaceAction.Input_Curve2:
            pass
        elif self.myBezierSurfaceAction == BezierSurfaceAction.Input_Curve3:
            self.CloseSurface()
        elif self.myBezierSurfaceAction == BezierSurfaceAction.Input_Curve4:
            self.CloseSurface()
        self.myCurves.clear()
        self.myBezierSurfaceAction = BezierSurfaceAction.Nothing

    def CloseSurface(self):
        self.myContext.Remove(self.myRubberSurface, True)
        self.myGeomSurface = Surface_Bezier(self.myContext)
        self.myGeomSurface.SetCurves(self.myCurves)
        self.myGeomSurface.Compute()
        self.bezierSurfaceNode = BezierSurfaceNode(self.myGeomSurface.GetName(), self.myNode)
        self.bezierSurfaceNode.setSketchObject(self.myGeomSurface)
        self.myModel.layoutChanged.emit()

    def GetTypeOfMethod(self):
        return Part_ObjectTypeOfMethod.BezierSurface_Method
