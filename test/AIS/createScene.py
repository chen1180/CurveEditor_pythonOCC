from OCC.Display.SimpleGui import init_display
display, start_display, add_menu, add_function_to_menu = init_display()
from OCC.Core.Quantity import *
from OCC.Core.Graphic3d import *
from OCC.Core.Aspect import *
from OCC.Core.TCollection import *
from OCC.Core.V3d import *
from OCC.Core.AIS import *
from OCC.Core.BRepPrimAPI import *

#Create color
MyColor=Quantity_Color(0.99, 0.65, 0.31,  Quantity_TOC_RGB)
Firebrick=Quantity_Color(Quantity_NOC_FIREBRICK)
#Create line attributes.
line=Graphic3d_AspectLine3d()
line.SetColor(MyColor)
#Create marker attributes
marker=Graphic3d_AspectMarker3d()
marker.SetColor(Firebrick)
marker.SetScale(1.0)
marker.SetType(Aspect_TOM_BALL)
#Create facet attributes.
facet=Graphic3d_AspectFillArea3d()
BrassMaterial=Graphic3d_MaterialAspect(Graphic3d_NOM_BRASS)
GoldMaterial=Graphic3d_MaterialAspect(Graphic3d_NOM_GOLD)
facet.SetInteriorStyle(Aspect_IS_SOLID)
facet.SetInteriorColor(MyColor)
facet.SetDistinguishOn()
facet.SetFrontMaterial(BrassMaterial)
facet.SetBackMaterial(GoldMaterial)
facet.SetEdgeOn()
#Use current view and viewer
viewer:V3d_Viewer=display.Viewer
view:V3d_View=display.View
#Create an interactive context
context=AIS_InteractiveContext(viewer)
shape=BRepPrimAPI_MakeBox(10,20,30).Solid()
ais_shape=AIS_Shape(shape)
ais_shape.SetColor(Firebrick)
ais_shape.SetMaterial(GoldMaterial)
context.Display(ais_shape,True)

# shape_2=BRepPrimAPI_MakeBox(130,30,30).Solid()
# # ais_shape_2=AIS_Shape(shape_2)

start_display()