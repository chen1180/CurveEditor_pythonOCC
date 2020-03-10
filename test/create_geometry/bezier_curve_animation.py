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

from OCC.Core.gp import *
from OCC.Core.Geom import Geom_BezierCurve
from OCC.Core.TColgp import TColgp_Array1OfPnt
from OCC.Display.SimpleGui import init_display
from OCC.Core.AIS import *
from OCC.Core.TCollection import *

display, start_display, add_menu, add_function_to_menu = init_display()


def beziercurve():
    # the first bezier curve
    array = TColgp_Array1OfPnt(1, 5)
    array.SetValue(1, gp_Pnt(0, 0, -5))
    array.SetValue(2, gp_Pnt(1, 2, 1))
    array.SetValue(3, gp_Pnt(2, 3, 2))
    array.SetValue(4, gp_Pnt(4, 3, -2))
    array.SetValue(5, gp_Pnt(100, 5, -2))
    beziercurve = Geom_BezierCurve(array)
    poles = beziercurve.Poles()
    for p in poles:
        print(p.X(), p.Y(), p.Z())
    beziercurve.Increase(5)
    poles = beziercurve.Poles()
    for p in poles:
        print(p.X(), p.Y(), p.Z())
    print(beziercurve.Continuity(), beziercurve.Degree(), beziercurve.Continuity(), poles)

    for j in range(array.Lower(), array.Upper() + 1):
        p = array.Value(j)
        display.DisplayShape(p)
    ais_curve = display.DisplayShape(beziercurve, color='RED')
    start_pnt = gp_Trsf()
    start_pnt.SetValues(1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0)
    end_pnt = gp_Trsf()
    end_pnt.SetValues(1, 0, 0, 100, 0, 1, 0, 100, 0, 0, 1, 100)
    animation = AIS_Animation(TCollection_AsciiString("obj1"))
    animation_obj = AIS_AnimationObject(TCollection_AsciiString("obj1"), display.Context, ais_curve, start_pnt, end_pnt)
    animation_obj.SetOwnDuration(2)
    animation_obj.SetStartPts(0)
    animation.Add(animation_obj)

    duration = animation.Duration()
    animation.StartTimer(0, 1.0, True)
    while not animation.IsStopped():
        animation.UpdateTimer()
        display.Context.UpdateCurrentViewer()


if __name__ == '__main__':
    beziercurve()
    start_display()
