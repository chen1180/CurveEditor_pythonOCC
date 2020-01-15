
from OCC.Core.Quantity import Quantity_Color,Quantity_TOC_RGB
from OCC.Display.SimpleGui import init_display
from OCC.Display.OCCViewer import Viewer3d
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
display, start_display, add_menu, add_function_to_menu = init_display()
assert isinstance(display,Viewer3d)
from OCC.Core.AIS import *
from OCC.Core.Graphic3d import *
from OCC.Core.gp import *
from OCC.Core.Aspect import *
from OCC.Core.Geom import *
from OCC.Core.Graphic3d import *
# #from original class
line=Geom_Line(gp_Pnt(0,0,0),gp_Dir(0,1,0))
ais_line=AIS_Line(line)

plane=Geom_Plane(0,0,1,0)
ais_plane=AIS_PlaneTrihedron(plane)

point=Geom_CartesianPoint(2,2,2)
position=str((point.X(),point.Y()))
display.DisplayMessage(point.Pnt(),position)
ais_point=AIS_Point(point)
ais_point.SetMarker(Aspect_TOM_BALL)

geom_circle=Geom_Circle(gp.XOY(),10)
ais_circle=AIS_Circle(geom_circle)

display.Context.Display(ais_line,True)
display.Context.Display(ais_plane,True)
display.Context.Display(ais_point,True)
display.Context.Display(ais_circle,False)

start_display()