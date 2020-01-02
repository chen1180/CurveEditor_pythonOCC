from controller.openglWindowController import *

from OCC.Core.Quantity import *
from OCC.Core.Graphic3d import *
from OCC.Core.Aspect import *
from OCC.Core.TCollection import *
from OCC.Core.Geom import *
from OCC.Core.gp import *
from OCC.Core.V3d import *
from OCC.Core.AIS import *
from OCC.Core.BRepPrimAPI import *
from OCC.Display.OCCViewer import Viewer3d
from OCC.Core.TopAbs import *
from OCC.Core.TopoDS import *
from OCC.Core.StdSelect import *


class InteractiveEditor(object):
    def __init__(self,context:AIS_InteractiveContext,view:V3d_View):
        self._context=context
        self._view=view
        self.prepareContext()
        self.points=[]
        self.First_Point=True
    def prepareContext(self):
        self._context.Deactivate()

        self.f1=AIS_SignatureFilter(AIS_KOI_Datum,AIS_SD_Axis) #AIS_KindOfInteractive #AIS_StandardDatum
        self.f3=StdSelect_FaceFilter(StdSelect_AnyEdge)
        self.f2=StdSelect_ShapeTypeFilter(TopAbs_VERTEX)
        self._context.AddFilter(self.f2)
        self._context.Activate(AIS_Shape.SelectionMode(TopAbs_EDGE))
        self._context.Activate(AIS_Shape.SelectionMode(TopAbs_FACE))
        self._context.Activate(AIS_Shape.SelectionMode(TopAbs_VERTEX))
        #Allows you to add the filter aFilter to Neutral Point or to a local context if one or more selection modes have been activated.
        #Only type filters may be active in Neutral Point.


        #at  this point, you can call the selection/detection function
    # def selection(self,xPix,yPix):
    #     try:
    #         if self._display.Context.HasDetected():
    #             self._display.Context.InitDetected()
    #             while (self._display.Context.MoreDetected()):
    #                 detected_object = self._display.Context.DetectedInteractive()
    #                 assert isinstance(detected_object, AIS_InteractiveObject)
    #                 self.setObject(detected_object)
    #                 self._display.Context.NextDetected()
    #     except Exception as e:
    #         print(e)
    def moveTo(self,xPix,yPix):
        detect=self._context.MoveTo(xPix,yPix,self._view,True)
        self._context.Select(True)
        self._context.InitSelected()
        if self._context.MoreSelected():
            if self._context.HasSelectedShape():
                shape:TopoDS_Shape=self._context.SelectedShape()
                '''
                TopAbs_COMPOUND 	
                TopAbs_COMPSOLID 	
                TopAbs_SOLID 	
                TopAbs_SHELL 	
                TopAbs_FACE 	
                TopAbs_WIRE 	
                TopAbs_EDGE 	
                TopAbs_VERTEX 	
                TopAbs_SHAPE 
                '''
                if shape.ShapeType() == TopAbs_VERTEX:
                    if self.First_Point==True:
                        self.points.append(shape)
                        self._context.RemoveFilters()


                        self._context.AddFilter(self.f3)
                        self.First_Point=False
                        return True
                    else:
                        self.points.append(shape)
                        print(self.points)


    def terminate(self):
        # deactivate Local Selection
        self._context.Deactivate()
        self._context.Activate(0)

def Test():
    application = QtWidgets.QApplication([])
    window = OpenGLEditor()  # Opengl window creation
    window.showMaximized()

    shape = BRepPrimAPI_MakeBox(10, 20, 30).Solid()
    line = Geom_Line(gp_Pnt(0, 0, 0), gp_Dir(0, 1, 0))
    ais_line = AIS_Line(line)

    plane = Geom_Plane(0, 0, 1, 0)
    ais_plane = AIS_PlaneTrihedron(plane)

    point = Geom_CartesianPoint(2, 2, 2)
    ais_point = AIS_Point(point)

    c = BRepPrimAPI_MakeCylinder(1.0, 10).Shape()

    viewer: V3d_Viewer = window._display.Viewer
    view: V3d_View = window._display.View
    context: AIS_InteractiveContext = window._display.Context
    display=window._display
    assert isinstance(display, Viewer3d)
    display.DisplayShape(shape)
    display.DisplayShape(c, update=True)

    context.Display(ais_line, True)
    context.Display(ais_plane, True)
    context.Display(ais_point, True)

    editor = InteractiveEditor(context,view)
    window.register_mousePress_callback(editor.moveTo)

    window.show()
    application.exec_()


sys._excepthook = sys.excepthook
def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)
sys.excepthook = my_exception_hook
Test()
