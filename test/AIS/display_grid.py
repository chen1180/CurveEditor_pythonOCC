
from OCC.Core.Quantity import Quantity_Color,Quantity_TOC_RGB
from OCC.Display.SimpleGui import init_display
from OCC.Display.OCCViewer import Viewer3d
display, start_display, add_menu, add_function_to_menu = init_display()
assert isinstance(display,Viewer3d)
# #from original class
from OCC.Core.V3d import V3d_RectangularGrid,V3d_View,V3d_Plane,V3d_Viewer
# grid=V3d_RectangularGrid(display.Viewer,Quantity_Color(0.2,0.2,0.2,Quantity_TOC_RGB),Quantity_Color(1,1,1,Quantity_TOC_RGB))
# grid.Display()
# #View class
# view=V3d_View(display.Viewer,display.View)
# #plane
# plane=V3d_Plane(1.0,0.0,0.0,10)
# plane.Display(display.View)
viewer=display.Viewer
assert isinstance(viewer,V3d_Viewer)
from OCC.Core.Aspect import *
from OCC.Core.Graphic3d import Graphic3d_Vertex
def coordinate_clicked(shp, *kwargs):
    """ This function is called whenever a vertex is selected
    """
    for shape in shp:
        print("Shape selected: ", shape)
    point_2d = kwargs
    X,Y,Z=display.View.ConvertToGrid(kwargs[0], kwargs[1])
    print(X,Y,Z)
    viewer.ShowGridEcho(display.View, Graphic3d_Vertex(X, Y, Z))
    viewer.RedrawImmediate()
#viwer https://www.opencascade.com/doc/occt-7.4.0/refman/html/class_v3d___viewer.html#aea2c2ae246f1c951cf99529734cdb219
#view  https://www.opencascade.com/doc/occt-7.4.0/refman/html/class_v3d___view.html#a9f0abb65a86d59b3816745a4bbe24744
viewer.ActivateGrid(Aspect_GT_Rectangular,Aspect_GDM_Lines)
viewer.SetGridEcho(True)
print(viewer.Grid().IsActive())
display.register_select_callback(coordinate_clicked)

start_display()