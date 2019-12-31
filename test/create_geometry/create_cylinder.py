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
from OCC.Core.Geom import Geom_Circle,Geom_SurfaceOfLinearExtrusion,Geom_BezierCurve,Geom_CylindricalSurface
from OCC.Core.TColgp import TColgp_Array1OfPnt
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox,BRepPrimAPI_MakeCylinder
from OCC.Display.SimpleGui import init_display
display, start_display, add_menu, add_function_to_menu = init_display()


def beziercurve():
    # axe=gp_Ax3()
    # cyliner=gp_Cylinder(axe,5.0)
    # c=Geom_CylindricalSurface(cyliner)
    c=BRepPrimAPI_MakeCylinder(1.0,10).Shape()
    display.DisplayShape(c,update=True)
if __name__ == '__main__':
    beziercurve()
    start_display()
