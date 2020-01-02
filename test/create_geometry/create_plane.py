from __future__ import print_function

from OCC.Core.gp import gp_Pnt2d,gp_Pnt,gp_Ax3,gp_Dir
from OCC.Core.Geom import Geom_BezierCurve,Geom_Plane,Geom_Axis2Placement
from OCC.Core.TColgp import TColgp_Array1OfPnt
from OCC.Display.SimpleGui import init_display
from OCC.Core.AIS import AIS_Plane, AIS_TOPL_XYPlane
from OCC.Core.Quantity import Quantity_Color,Quantity_TOC_RGB
display, start_display, add_menu, add_function_to_menu = init_display()

plane=Geom_Plane(gp_Pnt(0.0,0.0,0.0),gp_Dir(0,1,0))
axes=Geom_Axis2Placement(gp_Pnt(0,0,0),gp_Dir(0,0,1),gp_Dir(1,0,0))

ais_plane=AIS_Plane(plane,True)
ais_plane.SetColor(Quantity_Color(1,0,0.5,Quantity_TOC_RGB))
print(ais_plane.Type())

display.Context.Display(ais_plane, True)
start_display()
