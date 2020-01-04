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
from data.sketch.sketch_analyserSnap import *


class Sketch_Command(Standard_Transient):
    def __init__(self, name):
        super(Sketch_Command, self).__init__()
        self.myContext = AIS_InteractiveContext()
        self.data=TColStd_HSequenceOfTransient()

        self.objectName = name
        self.curCoordinateSystem = gp_Ax3(gp.XOY())
        self.objectCounter = 0
        self.objectType = Sketcher_ObjectType.MainSketcherType

        self.myAnalyserSnap=Sketcher_AnalyserSnap()

        self.myColor = Quantity_NOC_YELLOW
        self.myStyle = Aspect_TOL_SOLID
        self.myWidth = 1.0
        self.myPrs3dAspect = Prs3d_LineAspect(self.myColor, self.myStyle, self.myWidth)

        self.myPolylineMode = False
        self.curPnt2d = gp_Origin2d()
        self.myFirstgp_Pnt2d = gp_Origin2d()

        self.myFirstPoint = Geom_CartesianPoint(gp_Origin())
        self.mySecondPoint = Geom_CartesianPoint(gp_Origin())
        self.myRubberLine = AIS_Line(self.myFirstPoint, self.mySecondPoint)
        self.myRubberLine.SetColor(Quantity_NOC_LIGHTPINK1)

    def SetContext(self, theContext: AIS_InteractiveContext):
        self.myContext = theContext

    def SetData(self, theData: TColStd_HSequenceOfTransient):
        self.data = theData

    def SetAx3(self, theAx3: gp_Ax3):
        self.curCoordinateSystem = theAx3

    def SetAnalyserSnap(self, theAnalyserSnap):
        self.myAnalyserSnap = theAnalyserSnap

    def SetColor(self, theColor):
        self.myColor = theColor

    def SetType(self, theType):
        self.objectType = theType

    def SetWidth(self, theWidth):
        self.myWidth = theWidth

    def AddObject(self, theGeom2d_Geometry: Geom2d_Geometry, theAIS_InteractiveObject: AIS_InteractiveObject,
                  theGeometryType: Sketcher_ObjectGeometryType):
        self.objectCounter += 1
        numString = TCollection_ExtendedString(self.objectCounter)
        currentName = TCollection_ExtendedString(self.objectName)
        currentName += numString
        if self.GetTypeOfMethod() == Sketcher_ObjectTypeOfMethod.Point_Method:
            theAIS_InteractiveObject.SetColor(self.myColor)
        else:
            self.myPrs3dAspect.SetColor(self.myColor)
            self.myPrs3dAspect.SetTypeOfLine(self.myStyle)
            self.myPrs3dAspect.SetWidth(self.myWidth)
        so = Sketch_Object(theGeom2d_Geometry, theAIS_InteractiveObject, currentName, theGeometryType,
                           self.GetTypeOfMethod())
        so.SetColor(self.myColor)
        so.SetType(self.myType)
        so.SetStyle(self.myStyle)
        so.SetWidth(self.myWidth)
        self.data.Append(so)

    def GetTypeOfMethod(self) -> Sketcher_ObjectTypeOfMethod:
        return 0

    def Action(self):
        raise NotImplementedError()

    def MouseInputEvent(self, thePnt2d: gp_Pnt2d):
        raise NotImplementedError()

    def MouseMoveEvent(self, thePnt2d: gp_Pnt2d):
        raise NotImplementedError()

    def CancelEvent(self):
        raise NotImplementedError()

    def SetPolylineFirstPnt(self, p1):
        raise NotImplementedError()

    def GetPolylineFirstPnt(self, p1):
        return False

    def SetPolylineMode(self, mode):
        raise NotImplementedError()
