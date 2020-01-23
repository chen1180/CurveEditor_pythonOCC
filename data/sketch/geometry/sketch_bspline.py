from .sketch_geometry import *
from .sketch_point import Sketch_Point


class Sketch_Bspline(Sketch_Geometry):
    IndexCounter = 0

    def __init__(self, theContext, theAxis):
        super(Sketch_Bspline, self).__init__("Bspline", theContext, theAxis)
        Sketch_Bspline.IndexCounter += 1
        self.myName = "Bspline" + str(self.IndexCounter)
        self.myGeometry: Geom_BSplineCurve = None
        self.myGeometry2d: Geom2d_BSplineCurve = None
        self.myAIS_InteractiveObject: AIS_Shape = None
        self.myAIS_Lines = []
        self.myPoles = []
        self.myWeights = []
        self.myKnots = []
        self.myMultiplicities = []
        self.myDegree = 2
        self.myPeriodicFlag = False

    def AddPoles(self, thePnt2d, weight=1.0):
        # set poles
        sketch_point = Sketch_Point(self.myContext, self.curCoordinateSystem)
        sketch_point.Compute(thePnt2d)
        # auxiliry lines
        if len(self.myPoles) >= 1:
            ais_line: AIS_Line = AIS_Line(self.myPoles[-1].GetGeometry(), sketch_point.GetGeometry())
            ais_line.SetAttributes(self.myDrawer)
            self.myAIS_Lines.append(ais_line)
            self.myContext.Display(ais_line, True)
        # set weight
        self.myPoles.append(sketch_point)
        self.myWeights.append(weight)

    def RemoveDisplay(self):
        super(Sketch_Bspline, self).RemoveDisplay()
        for point in self.myPoles:
            point.RemoveDisplay()
        for line in self.myAIS_Lines:
            self.myContext.Remove(line, True)

    def Compute(self):
        arrayOfWeights = float_list_to_TColStd_Array1OfReal(self.myWeights)
        arrayOfKnots = float_list_to_TColStd_Array1OfReal(self.myKnots)
        arrayOfMulties = int_list_to_TColStd_Array1OfInteger(self.myMultiplicities)

        poles2d_list = [pole.GetGeometry2d().Pnt2d() for pole in self.myPoles]
        arrayOfPoles2d = point_list_to_TColgp_Array1OfPnt2d(poles2d_list)
        self.myGeometry2d = Geom2d_BSplineCurve(arrayOfPoles2d, arrayOfWeights, arrayOfKnots, arrayOfMulties,
                                                self.myDegree)

        poles_list = [pole.GetGeometry().Pnt() for pole in self.myPoles]
        arrayOfPoles = point_list_to_TColgp_Array1OfPnt(poles_list)
        self.myGeometry = Geom_BSplineCurve(arrayOfPoles, arrayOfWeights, arrayOfKnots, arrayOfMulties, self.myDegree)

        edge = BRepBuilderAPI_MakeEdge(self.myGeometry)
        if self.myAIS_InteractiveObject:
            self.myAIS_InteractiveObject.SetShape(edge.Edge())
            self.myAIS_InteractiveObject.Redisplay(True)
        else:
            self.myAIS_InteractiveObject = AIS_Shape(edge.Edge())
            self.myContext.Display(self.myAIS_InteractiveObject, True)

    def DragTo(self, index, newPnt2d):
        self.myPoles[index].DragTo(newPnt2d)
        pole2d = self.myPoles[index].GetGeometry2d().Pnt2d()
        pole = self.myPoles[index].GetGeometry().Pnt()
        self.myGeometry2d.SetPole(index + 1, pole2d, self.myWeights[index])
        self.myGeometry.SetPole(index + 1, pole, self.myWeights[index])
        self.myAIS_InteractiveObject.Redisplay(True)
        for line in self.myAIS_Lines:
            line.Redisplay(True)

    def Recompute(self):
        self.RemoveAIS_Lines()
        poles2d_list = [pole.GetGeometry2d().Pnt2d() for pole in self.myPoles]
        poles_list = [pole.GetGeometry().Pnt() for pole in self.myPoles]
        for index, pole2d in enumerate(poles2d_list):
            self.myGeometry2d.SetPole(index + 1, pole2d, self.myWeights[index])
            self.myGeometry.SetPole(index + 1, poles_list[index], self.myWeights[index])
        for index, knots in enumerate(self.myKnots):
            self.myGeometry2d.SetKnot(index + 1, knots, self.myMultiplicities[index])
            self.myGeometry.SetKnot(index + 1, knots, self.myMultiplicities[index])
        self.myAIS_InteractiveObject.Redisplay(True)

    def IncreaseDegree(self, theDegree):
        if theDegree < self.myGeometry2d.Degree():
            print("Degree elevation: degree can't be lower than 2 or lower than current degree")
        else:
            self.myGeometry2d.IncreaseDegree(theDegree)
            self.myGeometry.IncreaseDegree(theDegree)
            self.myDegree = theDegree
            self.updateGeomAttributes()
            self.myAIS_InteractiveObject.Redisplay(True)

    def IncreaseMultiplicity(self, theIndex, theMulti):
        self.myGeometry2d.IncreaseMultiplicity(theIndex, theMulti)
        self.myGeometry.IncreaseMultiplicity(theIndex, theMulti)
        self.myAIS_InteractiveObject.Redisplay(True)

    def updateGeomAttributes(self):
        poles2d_array = self.myGeometry2d.Poles()
        poles2d_list = TColgp_Array1OfPnt2d_to_point_list(poles2d_array)

        knots_array = self.myGeometry2d.Knots()
        multiplicity = self.myGeometry2d.Multiplicities()
        self.myKnots = TColStd_Array1OfNumber_to_list(knots_array)
        self.myMultiplicities = TColStd_Array1OfNumber_to_list(multiplicity)
        for p in self.myPoles:
            p.RemoveDisplay()
        self.myPoles.clear()
        self.myWeights.clear()
        for new_point in poles2d_list:
            self.AddPoles(new_point)

    def SetPeriodic(self):
        if self.myGeometry2d.IsPeriodic() == False:
            self.myGeometry2d.SetPeriodic()
            self.myGeometry.SetPeriodic()
        else:
            self.myGeometry2d.SetNotPeriodic()
            self.myGeometry.SetNotPeriodic()
        self.myContext.Remove(self.myAIS_Lines[-1], True)
        self.updateGeomAttributes()
        # display the last lines
        ais_line: AIS_Line = AIS_Line(self.myPoles[-1].GetGeometry(), self.myPoles[0].GetGeometry())
        ais_line.SetAttributes(self.myDrawer)
        self.myAIS_Lines.append(ais_line)
        self.myContext.Display(ais_line, True)
        self.myAIS_InteractiveObject.Redisplay(True)

    def RemoveAIS_Lines(self):
        # remove auxiliry line
        for line in self.myAIS_Lines:
            self.myContext.Remove(line, True)

    def GetGeometryType(self):
        return Sketch_GeometryType.CurveSketchObject

    def GetTypeOfMethod(self):
        return Sketch_ObjectTypeOfMethod.BSpline_Method

    def ChangeWeights(self, index, weight):
        self.myWeights[index] = weight

    def SetWeights(self, weights):
        self.myWeights = weights

    def GetWeights(self):
        return self.myWeights

    def SetMultiplicities(self, theMulti):
        self.myMultiplicities = theMulti

    def SetKnots(self, theKnots):
        self.myKnots = theKnots

    def GetKnots(self):
        return self.myKnots

    def SetMulties(self, theMulties):
        self.myMultiplicities = theMulties

    def ChangeMulties(self, index, multi):
        self.myMultiplicities[index] = multi

    def GetMulties(self):
        return self.myMultiplicities

    def GetPoles(self):
        return self.myPoles

    def SetDegree(self, theDegree):
        self.myDegree = theDegree

    def SetKnotsType(self, theType: int):
        # Non uniform type
        if theType == 0:
            pass
        # Uniform: if all the knots are of multiplicity 1,
        elif theType == 1:
            self.myMultiplicities, self.myKnots = setUniformKnots(len(self.myPoles), self.myDegree)
        # QuasiUniform: if all the knots are of multiplicity 1 except for the first and last knot which are of multiplicity Degree + 1,
        elif theType == 2:
            self.myMultiplicities, self.myKnots = setQuasiUniformKnots(len(self.myPoles), self.myDegree)
        # PiecewiseBezier: if the first and last knots have multiplicity Degree + 1 and if interior knots have multiplicity Degree A piecewise Bezier with only two knots is a BezierCurve. else the curve is non uniform.
        elif theType == 3:
            if len(self.myPoles) < 5:
                raise ValueError
            else:
                self.myMultiplicities, self.myKnots = setPiecewiseBezierKnots(len(self.myPoles), self.myDegree)
        self.Compute()
