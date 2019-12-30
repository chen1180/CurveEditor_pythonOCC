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
from OCC.Core.Geom import *
from OCC.Core.TColgp import *
from OCC.Core.Interface import *
from OCC.Display.SimpleGui import init_display
from OCC.Core.StepData import *
display, start_display, add_menu, add_function_to_menu = init_display()


# the first bezier curve
array = TColgp_Array1OfPnt(1, 5)
array.SetValue(1, gp_Pnt(0, 0,-5))
array.SetValue(2, gp_Pnt(1, 2,1))
array.SetValue(3, gp_Pnt(2, 3,2))
array.SetValue(4, gp_Pnt(4, 3,-2))
array.SetValue(5, gp_Pnt(5, 5,-2))
circle = Geom_Circle(gp_Ax2(),100.0)
surface=Geom_SurfaceOfLinearExtrusion(circle,gp_Dir(0.0,0.0,1.0))

model_a=StepData_StepModel()
model_a.AddEntity(circle)
model_a.AddEntity(surface)
tree=model_a.Entities()
assert isinstance(tree,Interface_EntityIterator)
check_tree=Interface_CheckTool (model_a)

display.DisplayShape(surface,update=True, color='Blue')

start_display()
