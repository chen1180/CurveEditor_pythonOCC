from __future__ import print_function

from OCC.Core.gp import *
from OCC.Core.Geom import Geom_BezierCurve, Geom_Plane, Geom_Axis2Placement
from OCC.Core.TColgp import TColgp_Array1OfPnt
from OCC.Display.SimpleGui import init_display
from OCC.Core.AIS import AIS_Plane, AIS_PlaneTrihedron, AIS_TextLabel, AIS_Trihedron, AIS_InteractiveContext
from OCC.Core.Quantity import *
from OCC.Core.Select3D import *
from OCC.Core.TCollection import TCollection_ExtendedString
from OCC.Core.Prs3d import *

display, start_display, add_menu, add_function_to_menu = init_display()

axis = Geom_Axis2Placement(gp.ZOX())
triehedron = AIS_Trihedron(axis)
triehedron.SetXAxisColor(Quantity_Color(Quantity_NOC_RED))
triehedron.SetYAxisColor(Quantity_Color(Quantity_NOC_GREEN))
triehedron.SetAxisColor(Quantity_Color(Quantity_NOC_BLUE1))

context: AIS_InteractiveContext = display.Context
drawer = triehedron.Attributes()
context.Display(triehedron, 0, 3, True)

plane = Geom_Plane(gp_Pnt(0.0, 0.0, 0.0), gp_Dir(0, 1, 0))
ais_plane1 = AIS_Plane(plane, True)
ais_plane1.SetColor(Quantity_Color(Quantity_NOC_GRAY))
ais_plane1.SetTypeOfSensitivity(Select3D_TOS_INTERIOR)

asp = Prs3d_LineAspect(Quantity_Color(Quantity_NOC_GREEN), 1, 10)
ais_plane1.SetAspect(asp)
display.Context.Display(ais_plane1, True)

text = AIS_TextLabel()
text.SetText(TCollection_ExtendedString("ARE YOUR SURE"))
text.SetPosition(gp_Pnt(0, 10, 0))
text.SetColor(Quantity_Color(Quantity_NOC_GREEN))
display.Context.Display(text, True)
start_display()
