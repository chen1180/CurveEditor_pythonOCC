from data.sketch.snaps.sketch_analyserSnap import Sketch_AnalyserSnap
from data.sketch.sketch_type import *
from data.sketch.sketch_object import Sketch_Object
from OCC.Core.Geom import Geom_CartesianPoint
from OCC.Core.gp import gp_Origin2d, gp_Ax3, gp_Pnt2d, gp, gp_Pnt, gp_Circ, gp_Circ2d, gp_Lin2d, gp_Ax2d, gp_Dir2d, \
    gp_Dir, gp_Vec
from OCC.Core.AIS import AIS_InteractiveContext, AIS_Line, AIS_InteractiveObject, AIS_Shape, AIS_Circle
from OCC.Core.Aspect import Aspect_TOL_SOLID
from OCC.Core.Prs3d import Prs3d_LineAspect
from OCC.Core.Quantity import Quantity_NOC_YELLOW, Quantity_NOC_LIGHTPINK1, Quantity_Color
from OCC.Core.Geom2d import Geom2d_Geometry
from OCC.Core.TCollection import TCollection_ExtendedString
from data.node import *
from data.sketch.sketch_utils import *

SKETCH_RADIUS = 10.0


class Sketch_Command(object):
    def __init__(self, name):
        self.data = []
        self.rootNode: Node = None
        self.objectName = name
        self.curCoordinateSystem = gp_Ax3(gp.XOY())
        self.objectCounter = 0

        self.myType = Sketch_ObjectType.MainSketchType
        self.myColor = Quantity_Color(Quantity_NOC_YELLOW)
        self.myStyle = Aspect_TOL_SOLID
        self.myWidth = 1.0
        self.myPrs3dAspect = Prs3d_LineAspect(self.myColor, self.myStyle, self.myWidth)

        self.myPolylineMode = False
        self.curPnt2d = gp.Origin2d()
        self.myFirstgp_Pnt2d = gp.Origin2d()
        self.mySecondgp_Pn2d = gp.Origin2d()

        self.myFirstPoint: Geom_CartesianPoint = Geom_CartesianPoint(gp.Origin())
        self.mySecondPoint: Geom_CartesianPoint = Geom_CartesianPoint(gp.Origin())
        self.myRubberLine = AIS_Line(self.myFirstPoint, self.mySecondPoint)
        self.myRubberLine.SetColor(Quantity_Color(Quantity_NOC_LIGHTPINK1))

    def SetContext(self, theContext: AIS_InteractiveContext):
        self.myContext = theContext

    def SetData(self, theData: list):
        self.data = theData

    def SetRootNode(self, theNode: Node):
        self.rootNode: Node = theNode

    def insertNode(self, node):
        '''

        Args:
            item: Mesh node (usually represent shape node)

        Returns:

        '''
        self.rootNode.insertNode(node, 0, 1)

    def SetAx3(self, theAx3: gp_Ax3):
        self.curCoordinateSystem = theAx3

    def SetAnalyserSnap(self, theAnalyserSnap):
        self.myAnalyserSnap: Sketch_AnalyserSnap = theAnalyserSnap

    def SetColor(self, theColor):
        self.myColor = theColor

    def SetType(self, theType):
        self.objectType = theType

    def SetWidth(self, theWidth):
        self.myWidth = theWidth

    def SetStyle(self, theLineStyle):
        self.myStyle = theLineStyle

    def AddObject(self, theGeom2d_Geometry: Geom2d_Geometry, theAIS_InteractiveObject: AIS_InteractiveObject,
                  theGeometryType: Sketch_GeometryType):
        self.objectCounter += 1
        numString = str(self.objectCounter)
        currentName = self.objectName
        currentName += numString
        if self.GetTypeOfMethod() == Sketch_ObjectTypeOfMethod.Point_Method:
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
        self.data.append(so)

    def AddNode(self, node: SketchObjectNode, theGeometry, theAIS_Object):
        node.setGeometry(theGeometry)
        node.setAisGeometry(theAIS_Object)
        node.setAxis(self.curCoordinateSystem)
    def GetTypeOfMethod(self):
        raise NotImplementedError()

    def Action(self):
        raise NotImplementedError()

    def MouseInputEvent(self, thePnt2d: gp_Pnt2d):
        raise NotImplementedError()

    def MouseMoveEvent(self, thePnt2d: gp_Pnt2d):
        raise NotImplementedError()

    def CancelEvent(self):
        raise NotImplementedError()

    def SetPolylineFirstPnt(self, p1):
        pass

    def GetPolylineFirstPnt(self, p1):
        pass

    def SetPolylineMode(self, mode):
        pass
