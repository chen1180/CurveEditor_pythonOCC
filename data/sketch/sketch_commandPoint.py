from OCC.Core.Geom import *
from OCC.Core.gp import *
from OCC.Core.V3d import *
from OCC.Core.AIS import *
from OCC.Core.BRepPrimAPI import *
from OCC.Display.OCCViewer import Viewer3d
from OCC.Core.TopAbs import *
from OCC.Core.TopoDS import *
from OCC.Core.StdSelect import *
from OCC.Core.BRepAdaptor import *
from OCC.Core.BRep import *
from OCC.Core.GeomAbs import *
from OCC.Core.GeomFill import *
from OCC.Core.Aspect import *
from OCC.Core.Prs3d import *
from OCC.Core.Quantity import *
from OCC.Core.TColStd import *
from OCC.Core.Geom2d import *
from OCC.Core.TCollection import *
from OCC.Core.Standard import Standard_Transient
from data.sketch.sketch_type import *
from OCC.Core.ElCLib import *
from data.sketch.sketch_command import *
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
        curPnt2d = self.myAnalyserSnap.MouseInput(thePnt2d)
        if self.myPointAction == PointAction.Nothing:
            pass
        elif self.myPointAction == PointAction.Input_Point:
            myGeom2d_Point = Geom2d_CartesianPoint(curPnt2d)
            myGeom_Point = Geom_CartesianPoint(elclib.To3d(self.curCoordinateSystem.Ax2()))
            myAIS_Point = AIS_Point(myGeom_Point)
            self.myContext.Display(myAIS_Point)
            self.AddObject(myGeom2d_Point, myAIS_Point, Sketcher_ObjectGeometryType.PointSketcherObject)
        return False

    def MouseMoveEvent(self, thePnt2d: gp_Pnt2d):
        curPnt2d = self.myAnalyserSnap.MouseMove(thePnt2d)

    def CancelEvent(self):
        self.myPointAction = PointAction.Nothing

    def GetTypeOfMethod(self) -> Sketcher_ObjectTypeOfMethod:
        return Sketcher_ObjectTypeOfMethod.Point_Method
