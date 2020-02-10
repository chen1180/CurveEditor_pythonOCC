
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

axis=Geom_Axis2Placement(gp.XOY())
plane=AIS_Trihedron(axis)
display.SetSelectionModeFace()
display.Context.Display(plane,True)
display.SetSelectionModeEdge()
start_display()