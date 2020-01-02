
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

controller=AIS_ViewController()

point=Geom_CartesianPoint(2,2,2)
ais_point=AIS_Point(point)

display.Context.Display(ais_point,True)
start_display()