
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
# #from original class
my_box = BRepPrimAPI_MakeBox(10., 20., 30.).Shape()
cube=AIS_ViewCube()
cube.SetTransformPersistence (Graphic3d_TMF_TriedronPers,gp_Pnt (1,1,100))
display.DisplayShape(my_box)
display.Context.Display(cube,True)

start_display()