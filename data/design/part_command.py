from OCC.Core.Geom import Geom_CartesianPoint
from OCC.Core.gp import gp_Origin2d, gp_Ax3, gp_Pnt2d, gp, gp_Pnt, gp_Circ, gp_Circ2d, gp_Lin2d, gp_Ax2d, gp_Dir2d, \
    gp_Dir, gp_Ax1
from OCC.Core.AIS import *
from OCC.Core.Aspect import Aspect_TOL_SOLID
from OCC.Core.Prs3d import Prs3d_LineAspect
from OCC.Core.Quantity import Quantity_NOC_YELLOW, Quantity_NOC_LIGHTPINK1, Quantity_Color, Quantity_NOC_SKYBLUE
from OCC.Core.Geom2d import Geom2d_Geometry
from OCC.Core.TCollection import TCollection_ExtendedString
from OCC.Display.OCCViewer import Viewer3d
from data.design.part_type import *
from OCC.Core.BRepAdaptor import BRepAdaptor_Curve
from OCC.Core.GeomAbs import *
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.TopAbs import *
from OCC.Core.Geom import Geom_Circle,Geom_Line


class Part_Command(object):
    def __init__(self, name):
        self.data = []

        self.objectName = name
        self.curCoordinateSystem = gp_Ax3(gp.XOY())
        self.objectCounter = 0

        self.myColor = Quantity_Color(Quantity_NOC_SKYBLUE)
        self.myStyle = Aspect_TOL_SOLID
        self.myWidth = 1.0
        self.myPrs3dAspect = Prs3d_LineAspect(self.myColor, self.myStyle, self.myWidth)

        self.myPolylineMode = False
        self.curPnt2d = gp.Origin2d()
        self.myFirstgp_Pnt2d = gp.Origin2d()

        self.myFirstPoint: Geom_CartesianPoint = Geom_CartesianPoint(gp.Origin())
        self.mySecondPoint: Geom_CartesianPoint = Geom_CartesianPoint(gp.Origin())
        self.myRubberLine = AIS_Line(self.myFirstPoint, self.mySecondPoint)
        self.myRubberLine.SetColor(Quantity_Color(Quantity_NOC_LIGHTPINK1))

    def SetContext(self, theContext: AIS_InteractiveContext):
        self.myContext = theContext

    def SetDisplay(self, theDisplay: Viewer3d):
        self.myDisplay: Viewer3d = theDisplay
        self.SetContext(self.myDisplay.Context)

    def SetData(self, theData: list):
        self.data = theData

    def SetAx3(self, theAx3: gp_Ax3):
        dir = theAx3.Direction()
        location = theAx3.Location()
        self.curCoordinateSystem.SetDirection(dir)
        self.curCoordinateSystem.SetLocation(location)

    def SetColor(self, theColor):
        self.myColor = theColor

    def SetType(self, theType):
        self.objectType = theType

    def SetWidth(self, theWidth):
        self.myWidth = theWidth

    def SetStyle(self, theLineStyle):
        self.myStyle = theLineStyle

    # def AddObject(self, theGeom2d_Geometry: Geom2d_Geometry, theAIS_InteractiveObject: AIS_InteractiveObject,
    #               theGeometryType: Sketch_GeometryType):
    #     self.objectCounter += 1
    #     numString = TCollection_ExtendedString(self.objectCounter)
    #     currentName = TCollection_ExtendedString(self.objectName)
    #     currentName += numString
    #     if self.GetTypeOfMethod() == Sketch_ObjectTypeOfMethod.Point_Method:
    #         theAIS_InteractiveObject.SetColor(self.myColor)
    #     else:
    #         self.myPrs3dAspect.SetColor(self.myColor)
    #         self.myPrs3dAspect.SetTypeOfLine(self.myStyle)
    #         self.myPrs3dAspect.SetWidth(self.myWidth)
    #     so = Sketch_Object(theGeom2d_Geometry, theAIS_InteractiveObject, currentName, theGeometryType,
    #                        self.GetTypeOfMethod())
    #     so.SetColor(self.myColor)
    #     so.SetType(self.myType)
    #     so.SetStyle(self.myStyle)
    #     so.SetWidth(self.myWidth)
    #     self.data.append(so)

    def GetTypeOfMethod(self):
        raise NotImplementedError()

    def Action(self):
        raise NotImplementedError()

    def MouseInputEvent(self, xPix, yPix):
        raise NotImplementedError()

    def MouseMoveEvent(self, xPix, yPix):
        raise NotImplementedError()

    def CancelEvent(self):
        raise NotImplementedError()

    def SetPolylineFirstPnt(self, p1):
        pass

    def GetPolylineFirstPnt(self, p1):
        pass

    def SetPolylineMode(self, mode):
        pass

    def SelectObject(self, xPix, yPix) -> AIS_InteractiveObject:
        self.myDisplay.MoveTo(xPix, yPix)
        self.myContext.Select(True)
        self.myContext.InitSelected()
        if self.myContext.MoreSelected():
            selectedObject = self.myContext.SelectedInteractive()
            return selectedObject

    def DetectObject(self, xPix, yPix) -> AIS_InteractiveObject:
        self.myDisplay.MoveTo(xPix, yPix)
        self.myContext.InitDetected()
        if self.myContext.HasDetected():
            detectedObject = self.myContext.DetectedInteractive()
            return detectedObject

    def FindGeometry(self, object: AIS_InteractiveObject):
        if object.Type() == AIS_KOI_Shape:
            shape = self.myContext.SelectedShape()
            if shape.ShapeType() == TopAbs_VERTEX:
                pass
            elif shape.ShapeType() == TopAbs_EDGE:
                curve = BRepAdaptor_Curve(shape)
                curve_type = curve.GetType()
                if curve_type == GeomAbs_BezierCurve:
                    return curve.Bezier()
                elif curve_type == GeomAbs_BSplineCurve:
                    return curve.BSpline()
                elif curve_type == GeomAbs_Circle:
                    return Geom_Circle(curve.Circle())
                elif curve_type==GeomAbs_Line:
                    return Geom_Line(curve.Line())
            elif shape.ShapeType() == TopAbs_FACE:
                pass

    def FindDatum(self, object: AIS_InteractiveObject):
        '''
        signature 0 - Shape
        signature 1 - Point
        signature 2 - Axis
        signature 3 - Trihedron
        signature 4 - PlaneTrihedron
        signature 5 - Line
        signature 6 - Circle
        signature 7 - Plane
        '''
        if object.Type() == AIS_KOI_Datum:
            if object.Signature() == 0:
                pass
            elif object.Signature() == 1:
                point = AIS_Point.DownCast(object)
                return point
            elif object.Signature() == 2:
                pass
            elif object.Signature() == 3:
                trihedron: AIS_Trihedron = AIS_Trihedron.DownCast(object)
                dir = trihedron.Component().Ax2().Direction()
                return trihedron
            elif object.Signature() == 4:
                pass
            elif object.Signature() == 5:
                line = AIS_Line.DownCast(object)
                return line
            elif object.Signature() == 6:
                circle = AIS_Circle.DownCast(object)
                return circle
            elif object.Signature() == 7:
                pass
