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

from OCC.Core.gp import gp_Pnt2d,gp_Pnt,gp_Circ,gp_Ax2
from OCC.Core.Geom import Geom_Circle,Geom_BSplineCurve
from OCC.Core.TColgp import TColgp_Array1OfPnt
from OCC.Core.TColStd import TColStd_Array1OfReal,TColStd_Array1OfInteger
from OCC.Display.SimpleGui import init_display
display, start_display, add_menu, add_function_to_menu = init_display()

# the first bezier curve
array = TColgp_Array1OfPnt(1, 4)
array.SetValue(1, gp_Pnt(0, 0,0))
array.SetValue(2, gp_Pnt(1, 0,0))
array.SetValue(3, gp_Pnt(1, 1,0))
array.SetValue(4, gp_Pnt(3, 3,0))
weights=TColStd_Array1OfReal(1,4)
knots=TColStd_Array1OfReal(1,3)
multiplicities=TColStd_Array1OfInteger(1,3)
multiplicities.SetValue(1,3)
multiplicities.SetValue(2,1)
multiplicities.SetValue(3,3)
knots.SetValue(1,0.0)
knots.SetValue(2,0.5)
knots.SetValue(3,1.0)
weights.SetValue(1,1.0)
weights.SetValue(2,1.0)
weights.SetValue(3,1.0)
weights.SetValue(4,1.0)

nurbs = Geom_BSplineCurve(array,weights,knots,multiplicities,2,False,True  )
print(nurbs.Period())
display.DisplayShape(nurbs, update=True, color='RED')
start_display()
