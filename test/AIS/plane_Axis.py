
from OCC.Core.Quantity import *
from OCC.Display.SimpleGui import init_display
from OCC.Display.OCCViewer import Viewer3d
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.Prs3d import *
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
display.Context.Display(plane,True)
display.SetSelectionModeFace()
# plane=Geom_Plane(gp_Pnt(0.0,0.0,0.0),gp_Dir(0.0,0.0,1.0))
# ais_plane=AIS_Plane(plane,True)
# drawer=Prs3d_Drawer()
# datum=Prs3d_DatumAspect()
# for i in range(10):
#     print(datum. DrawDatumPart(i))
# drawer.SetDatumAspect(datum)
# ais_plane.SetAttributes(drawer)
# display.Context.Display(ais_plane,True)
start_display()