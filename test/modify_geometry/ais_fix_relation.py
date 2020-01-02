#!/usr/bin/env python

##Copyright 2009-2014 Jelle Feringa (jelleferinga@gmail.com)
##
##This file is part of pythonOCC.
##
##pythonOCC is free software: you can redistribute it and/or modify
##it under the terms of the GNU Lesser General Public License as published by
##the Free Software Foundation, either version 3 of the License, or
##(at your option) any later version.
##
##pythonOCC is distributed in the hope that it will be useful,
##but WITHOUT ANY WARRANTY; without even the implied warranty of
##MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##GNU Lesser General Public License for more details.
##
##You should have received a copy of the GNU Lesser General Public License
##along with pythonOCC.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function

from OCC.Core.gp import gp_Pnt2d,gp_Pnt,gp_Dir
from OCC.Core.Geom import Geom_BezierCurve,Geom_BezierSurface,Geom_Plane
from OCC.Core.TColgp import TColgp_Array1OfPnt,TColgp_Array2OfPnt
from OCC.Display.SimpleGui import init_display
from OCC.Core.GeomFill import (GeomFill_BSplineCurves,
                               GeomFill_StretchStyle,
                               GeomFill_CoonsStyle,
                               GeomFill_CurvedStyle,GeomFill_BezierCurves)
from OCC.Core.AIS import AIS_FixRelation
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace
display, start_display, add_menu, add_function_to_menu = init_display()


def beziercurve():

    # the first bezier curve
    array = TColgp_Array1OfPnt(1, 5)
    array.SetValue(1, gp_Pnt(0, 0,-5))
    array.SetValue(2, gp_Pnt(1, 2,1))
    array.SetValue(3, gp_Pnt(2, 3,2))
    array.SetValue(4, gp_Pnt(4, 3,-2))
    array.SetValue(5, gp_Pnt(10, 5,-2))
    beziercurve = Geom_BezierCurve(array)
    # the first bezier curve
    array1 = TColgp_Array1OfPnt(1, 5)
    array1.SetValue(1, gp_Pnt(0, 0, -5))
    array1.SetValue(2, gp_Pnt(2, -2, 1))
    array1.SetValue(3, gp_Pnt(2, -3, 2))
    array1.SetValue(4, gp_Pnt(-4, 1, -2))
    array1.SetValue(5, gp_Pnt(1, 5, -2))
    beziercurve1 = Geom_BezierCurve(array1)

    array2 = TColgp_Array1OfPnt(1, 5)
    array2.SetValue(1, gp_Pnt(0, 0, -5))
    array2.SetValue(2, gp_Pnt(-2, 2, 1))
    array2.SetValue(3, gp_Pnt(2, -2, 2))
    array2.SetValue(4, gp_Pnt(-4, 8, -2))
    array2.SetValue(5, gp_Pnt(1, 5, -9))
    beziercurve2 = Geom_BezierCurve(array2)

    plane = Geom_Plane(gp_Pnt(0.0, 0.0, 0.0), gp_Dir(0, 1, 1))
    display.DisplayShape(plane, color='RED')

    surface1=GeomFill_BezierCurves(beziercurve,beziercurve1,beziercurve2,GeomFill_CurvedStyle)
    surface2 = GeomFill_BezierCurves(beziercurve, beziercurve1, GeomFill_StretchStyle)
    surface3 = GeomFill_BezierCurves(beziercurve, beziercurve1, GeomFill_CoonsStyle)

    bounds = True
    toldegen = 1e-6
    face = BRepBuilderAPI_MakeFace()
    face.Init(surface1.Surface(), bounds, toldegen)
    face.Build()

    shapes = face.Shape()

    fix=AIS_FixRelation(shapes,plane)
    display.Context.Display(fix, True)
    display.DisplayShape(shapes, color="RED")
    # display.DisplayShape(surface2.Surface(), color='GREEN')
    # display.DisplayShape(surface3.Surface(), color='BLUE')
if __name__ == '__main__':
    beziercurve()
    start_display()
