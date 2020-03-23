from .sketch_geometry import *
from .sketch_point import Sketch_Point


class Sketch_BezierCurve(Sketch_Geometry):
    IndexCounter = 0

    def __init__(self, theContext, theAxis):
        super(Sketch_BezierCurve, self).__init__("Bezier curve", theContext, theAxis)
        Sketch_BezierCurve.IndexCounter += 1
        self.myGeometry: Geom_BezierCurve = None
        self.myGeometry2d: Geom2d_BezierCurve = None
        self.myAIS_InteractiveObject: AIS_Shape = None
        self.myAIS_Lines = []
        self.myPoles = []
        self.myWeights = []
        self.myName = "Bezier curve" + str(self.IndexCounter)

    def ChangeWeights(self, index, weight):
        self.myWeights[index] = weight

    def SetWeights(self, weights):
        self.myWeights = weights

    def GetWeights(self):
        return self.myWeights

    def AddPoles(self, thePnt2d):
        sketch_point = Sketch_Point(self.myContext, self.curCoordinateSystem)
        sketch_point.Compute(thePnt2d)
        # auxiliry lines
        if len(self.myPoles) >= 1:
            ais_line: AIS_Line = AIS_Line(self.myPoles[-1].GetGeometry(), sketch_point.GetGeometry())
            ais_line.SetAttributes(self.myDrawer)
            self.myAIS_Lines.append(ais_line)
            self.myContext.Display(ais_line, True)
        self.myPoles.append(sketch_point)
        self.myWeights.append(1.0)

    def GetPoles(self):
        return self.myPoles

    def DragTo(self, index, newPnt2d):
        self.myPoles[index].DragTo(newPnt2d)
        pole2d = self.myPoles[index].GetGeometry2d().Pnt2d()
        pole = self.myPoles[index].GetGeometry().Pnt()
        self.myGeometry2d.SetPole(index + 1, pole2d, self.myWeights[index])
        self.myGeometry.SetPole(index + 1, pole, self.myWeights[index])
        self.myAIS_InteractiveObject.Redisplay(True)
        for line in self.myAIS_Lines:
            line.Redisplay(True)

    def Compute(self):
        arrayOfWeights = float_list_to_TColStd_Array1OfReal(self.myWeights)

        poles2d_list = [pole.GetGeometry2d().Pnt2d() for pole in self.myPoles]
        arrayOfPoles2d = point_list_to_TColgp_Array1OfPnt2d(poles2d_list)
        self.myGeometry2d = Geom2d_BezierCurve(arrayOfPoles2d, arrayOfWeights)

        poles_list = [pole.GetGeometry().Pnt() for pole in self.myPoles]
        arrayOfPoles = point_list_to_TColgp_Array1OfPnt(poles_list)
        self.myGeometry = Geom_BezierCurve(arrayOfPoles, arrayOfWeights)

        edge = BRepBuilderAPI_MakeEdge(self.myGeometry)
        shape = edge.Edge()
        self.myAIS_InteractiveObject = AIS_Shape(edge.Edge())
        self.myAIS_InteractiveObject.SetAttributes(self.myDrawer)
        self.myContext.Display(self.myAIS_InteractiveObject, True)

    def Recompute(self):
        poles2d_list = [pole.GetGeometry2d().Pnt2d() for pole in self.myPoles]
        for index, pole2d in enumerate(poles2d_list):
            self.myGeometry2d.SetPole(index + 1, pole2d, self.myWeights[index])
        poles_list = [pole.GetGeometry().Pnt() for pole in self.myPoles]
        for index, pole in enumerate(poles_list):
            self.myGeometry.SetPole(index + 1, pole, self.myWeights[index])
        self.myAIS_InteractiveObject.Redisplay(True)

    def IncreaseDegree(self, theDegree):
        if theDegree <= 2 or theDegree < self.myGeometry2d.Degree():
            print("Degree elevation: degree can't be lower than 2 or lower than current degree")
        else:
            self.RemoveLabel()
            self.myGeometry2d.Increase(theDegree)
            self.myGeometry.Increase(theDegree)
            poles2d_array = self.myGeometry2d.Poles()
            poles2d_list = TColgp_Array1OfPnt2d_to_point_list(poles2d_array)

            self.myPoles.clear()
            self.myWeights.clear()
            self.myAIS_Lines.clear()
            for new_point in poles2d_list:
                self.AddPoles(new_point)
            self.DisplayName()
            self.DisplayCoordinate()
            self.DisplayAuxiliryLine()
            self.myAIS_InteractiveObject.Redisplay(True)

    def GetGeometryType(self):
        return Sketch_GeometryType.CurveSketchObject

    def GetTypeOfMethod(self):
        return Sketch_ObjectTypeOfMethod.BezierCurve_Method

    def RemoveDisplay(self):
        super(Sketch_BezierCurve, self).RemoveDisplay()
        self.RemoveLabel()

    def RemoveLabel(self):
        for point in self.myPoles:
            point.RemoveDisplay()
            point.RemoveLabel()
        for line in self.myAIS_Lines:
            self.myContext.Remove(line, True)

    def DisplayName(self):
        if self.showViewportName:
            for point in self.myPoles:
                self.myContext.Display(point.myAIS_Name, True)
        else:
            for point in self.myPoles:
                self.myContext.Erase(point.myAIS_Name, True)

    def DisplayCoordinate(self):
        if self.showViewportCoordinate:
            for point in self.myPoles:
                self.myContext.Display(point.myAIS_Coordinate, True)
        else:
            for point in self.myPoles:
                self.myContext.Erase(point.myAIS_Coordinate, True)

    def DisplayAuxiliryLine(self):
        if self.showVieportAuxilirayLine:
            for point in self.myPoles:
                self.myContext.Display(point.GetAIS_Object(), True)
            for line in self.myAIS_Lines:
                self.myContext.Display(line, True)
        else:
            for point in self.myPoles:
                self.myContext.Erase(point.GetAIS_Object(), True)
            for line in self.myAIS_Lines:
                self.myContext.Erase(line, True)

    def GetStyle(self):
        return self.myWireStyle

    def SetStyle(self, theStyle):
        self.myWireStyle = theStyle
        self.myWireAspect.SetTypeOfLine(theStyle)

    def GetWidth(self):
        return self.myWireWidth

    def SetWidth(self, theWidth):
        self.myWireWidth = theWidth
        self.myWireAspect.SetWidth(theWidth)

    def GetColor(self):
        return self.myWireColor

    def SetColor(self, theColor):
        self.myWireColor = theColor
        self.myWireAspect.SetColor(Quantity_Color(theColor))
