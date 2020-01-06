from data.sketch.commands.sketch_command import *
from data.sketch.geometry.geom2d_edge import Geom2d_Edge
from OCC.Core.ElCLib import elclib
from OCC.Core.AIS import AIS_Point
from OCC.Core.Geom2d import Geom2d_CartesianPoint, Geom2d_BSplineCurve
from OCC.Core.Geom import  Geom_BSplineCurve
from OCC.Core.GeomAPI import GeomAPI_PointsToBSpline
from enum import Enum
from OCC.Core.TopoDS import TopoDS_Edge
from OCC.Core.TColgp import TColgp_Array1OfPnt2d, TColgp_Array1OfPnt
from OCC.Core.TColStd import TColStd_Array1OfReal,TColStd_Array1OfInteger
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge,BRepBuilderAPI_MakeEdge2d
from OCC.Display.SimpleGui import init_display
display, start_display, add_menu, add_function_to_menu = init_display()

myFirstgp_Pnt2d=gp.Origin2d()
mySecondgp_Pnt2d=gp_Pnt2d(-10,2)
myThirdgp_Pnt2d=gp_Pnt2d(5,7)
myFourthgp_Pnt2d=gp_Pnt2d(5,15)
myDegree=2

curgp_Array1CurvePoles2d = TColgp_Array1OfPnt2d(1, 4)
curgp_Array1CurvePoles2d.SetValue(1, myFirstgp_Pnt2d)
curgp_Array1CurvePoles2d.SetValue(2, mySecondgp_Pnt2d)
curgp_Array1CurvePoles2d.SetValue(3, myThirdgp_Pnt2d)
curgp_Array1CurvePoles2d.SetValue(4, myFourthgp_Pnt2d)

curgp_Array1CurveWeights2d = TColStd_Array1OfReal(1, 4)
curgp_Array1CurveWeights2d.SetValue(1, 1.0)
curgp_Array1CurveWeights2d.SetValue(2, 1.0)
curgp_Array1CurveWeights2d.SetValue(3, 1.0)
curgp_Array1CurveWeights2d.SetValue(4, 1.0)

curgp_Array1CurveMulti2d = TColStd_Array1OfInteger(1, 3)
curgp_Array1CurveMulti2d.SetValue(1, 3)
curgp_Array1CurveMulti2d.SetValue(2, 1)
curgp_Array1CurveMulti2d.SetValue(3, 3)

curgp_Array1CurveKnots2d = TColStd_Array1OfReal(1, 3)
curgp_Array1CurveKnots2d.SetValue(1, 0.0)
curgp_Array1CurveKnots2d.SetValue(2, 1.0)
curgp_Array1CurveKnots2d.SetValue(3, 2.0)



myGeom2d_BSplineCurve = Geom2d_BSplineCurve(curgp_Array1CurvePoles2d, curgp_Array1CurveKnots2d, curgp_Array1CurveMulti2d, myDegree)

knots:TColStd_Array1OfReal=myGeom2d_BSplineCurve.Knots()
mults:TColStd_Array1OfInteger=myGeom2d_BSplineCurve.Multiplicities()
for i in range(1,knots.Length()):
    print(knots.Value(i),end=",")
for i in range(1,mults.Length()):
    print(mults.Value(i),end=",")
edge=BRepBuilderAPI_MakeEdge2d(myGeom2d_BSplineCurve)
if edge.IsDone():
    myGeom2d_BSplineCurve.SetPole(2, gp.Origin2d())
    print("edge done")
    curEdge = edge.Edge()
    ais_shape=AIS_Shape(curEdge)
    display.Context.Display(ais_shape,True)
start_display()