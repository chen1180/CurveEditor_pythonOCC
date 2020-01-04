from OCC.Core.gp import gp_Pnt2d, gp_Pnt, gp_Pln, gp_Dir, gp_Ax3, gp_Ax2, gp_Vec, gp_Ax1, gp_Trsf, gp_Circ
from OCC.Core.Geom import Geom_BezierCurve, Geom_BSplineCurve, Geom_Circle, Geom_SurfaceOfRevolution, Geom_Curve, \
    Geom_CartesianPoint
from OCC.Core.GeomAPI import GeomAPI_PointsToBSpline
from OCC.Core.GeomAbs import *
from OCC.Core.AIS import *
from OCC.Core.Aspect import Aspect_GDM_Lines, Aspect_GT_Rectangular
from OCC.Core.TopAbs import *
from OCC.Core.TopoDS import *
from OCC.Core.TColgp import TColgp_Array1OfPnt
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Core.BRepAdaptor import BRepAdaptor_Curve
from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepBuilderAPI import *
from OCC.Core.TopoDS import topods_Edge
from PyQt5.QtCore import *
from controller.editorController import Sketch_NewSketchEditor
from data.node import *
from data.interactive import InteractiveEditor
from OCC.Core.V3d import *
from OCC.Core.ProjLib import *
from OCC.Core.ElSLib import *


class SketchController(QObject):
    modelUpdate = pyqtSignal(object)
    DRAW_END = 0
    DRAW_START = 1
    CURVE_BEZIER = 10
    CURVE_BSPLINE = 11
    CURVE_CIRCLE = 12
    SURFACE_BEZIER = 20
    SURFACE_BSPLINE = 21
    SURFACE_REVOLUTION = 30

    def __init__(self, display):
        super(SketchController, self).__init__()
        self._display = display
        self._currentPos = None
        self._clicked = []
        self._state = None
        self._shape_type = None
        self._selectedShape = None
        self._tmp_geometry = None
        self.interactive = InteractiveEditor(self._display)

    def action_bezierCurve(self):
        self._state = self.DRAW_START
        self._shape_type = self.CURVE_BEZIER

    def action_bSpline(self):
        self._state = self.DRAW_START
        self._shape_type = self.CURVE_BSPLINE

    def action_circle(self):
        self._state = self.DRAW_START
        self._shape_type = self.CURVE_CIRCLE

    def action_revolutedSurface(self):
        self._state = self.DRAW_START
        self._shape_type = self.SURFACE_REVOLUTION

    def action_bezierSurface(self):
        self._state = self.DRAW_START
        self._shape_type = self.SURFACE_BEZIER

    def makePoint(self, point):
        geom_point = Geom_CartesianPoint(point)
        ais_point = AIS_Point(geom_point)
        self._display.Context.Display(ais_point, True)

    def makeBezierCurve(self, point_array, last_point=None):
        if last_point:
            array = TColgp_Array1OfPnt(1, len(point_array) + 1)
            for i, p in enumerate(point_array):
                array.SetValue(i + 1, p)
            array.SetValue(len(point_array) + 1, last_point)
        else:
            array = TColgp_Array1OfPnt(1, len(point_array))
            for i, p in enumerate(point_array):
                array.SetValue(i + 1, p)
        bezier_curve = Geom_BezierCurve(array)
        if self._tmp_geometry:
            edge = BRepBuilderAPI_MakeEdge(bezier_curve)
            shapes = edge.Shape()
            self._tmp_geometry.SetShape(shapes)
            self._tmp_geometry.Redisplay(False)
        else:
            ais_bezier = self._display.DisplayShape(bezier_curve)
            self._tmp_geometry = ais_bezier

    def makeBSpline(self, point_array, last_point=None):
        if last_point:
            array = TColgp_Array1OfPnt(1, len(point_array) + 1)
            for i, p in enumerate(point_array):
                array.SetValue(i + 1, p)
            array.SetValue(len(point_array) + 1, last_point)
        else:
            array = TColgp_Array1OfPnt(1, len(point_array))
            for i, p in enumerate(point_array):
                array.SetValue(i + 1, p)
        try:
            bspline = GeomAPI_PointsToBSpline(array).Curve()
            if self._tmp_geometry:
                edge = BRepBuilderAPI_MakeEdge(bspline)
                shapes = edge.Shape()
                self._tmp_geometry.SetShape(shapes)
                self._tmp_geometry.Redisplay(False)
            else:
                ais_bspline = self._display.DisplayShape(bspline)
                self._tmp_geometry = ais_bspline
        except:
            pass

    def makeCircle(self, p1, p2):
        axe = gp_Ax2(p1, self.new_sketch.dir)
        radius = p1.Distance(p2)
        circle = gp_Circ(axe, radius)
        edge = BRepBuilderAPI_MakeEdge(circle)
        if self._tmp_geometry is None:
            shape = AIS_Shape(TopoDS_Edge())
            shape.Set(edge.Edge())
            self._tmp_geometry = shape
            self._display.Context.Display(self._tmp_geometry, True)
        else:
            self._tmp_geometry.Set(edge.Edge())
            self._tmp_geometry.Redisplay(False)

    def makeSurfaceOfRevolution(self, axis):
        pass

    def makeSurfaceBezier(self):
        pass

    def EnterDrawingMode(self):
        if self._state == self.DRAW_START:
            if self._shape_type == self.CURVE_BEZIER:
                if self._currentPos:
                    self._display.DisplayShape(self._currentPos)
            elif self._shape_type == self.CURVE_BSPLINE:
                if self._currentPos:
                    self._display.DisplayShape(self._currentPos)
            elif self._shape_type == self.CURVE_CIRCLE:
                if self._currentPos:
                    self._display.DisplayShape(self._currentPos)
            elif self._shape_type == self.SURFACE_REVOLUTION:
                self.interactive.prepareContext_find_edge()
            elif self._shape_type == self.SURFACE_BEZIER:
                self.interactive.prepareContext_find_edge()
        else:
            try:
                if self._shape_type == self.CURVE_BEZIER:
                    self.makeBezierCurve(self._clicked)
                elif self._shape_type == self.CURVE_BSPLINE:
                    self.makeBSpline(self._clicked)
                elif self._shape_type == self.CURVE_CIRCLE:
                    self.makeCircle(self._clicked[0], self._clicked[1])
                elif self._shape_type == self.SURFACE_REVOLUTION:
                    self.interactive.terminateContext()
                elif self._shape_type == self.SURFACE_BEZIER:
                    self.interactive.terminateContext()
            except Exception as e:
                print(e)
            finally:
                self.resetState()

    def ExitDrawingMode(self):
        self._state = self.DRAW_END
        self._currentPos = None
        self.interactive.terminateContext()

    def resetState(self):
        self._currentPos = None
        self._shape_type = None
        self._clicked.clear()
        self._tmp_geometry = None

    def convertScreenPos(self, xPos, yPos):
        x, y, z = self._display.View.ConvertToGrid(xPos, yPos)
        return x, y, z

    def convertClickToPoint(self, x, y):
        view: V3d_View = self._display.View
        xEye, yEye, zEye = view.Eye()
        xAt, yAt, zAt = view.At()
        eyePoint = gp_Pnt(xEye, yEye, zEye)
        atPoint = gp_Pnt(xAt, yAt, zAt)
        eyeVec = gp_Vec(eyePoint, atPoint)
        eyeDir = gp_Dir(eyeVec)
        planeOfView = gp_Pln(atPoint, eyeDir)
        X, Y, Z = view.Convert(x, y)
        convertedPoint = gp_Pnt(X, Y, Z)
        ConvertedPointOnPlane = projlib.Project(planeOfView, convertedPoint)
        resultPoint = elslib.Value(ConvertedPointOnPlane.X(), ConvertedPointOnPlane.Y(), planeOfView)
        print(resultPoint.X(),resultPoint.Y(),resultPoint.Z())
        return resultPoint

    def mousePress(self, xPix, yPix):
        x, y, z = self.convertScreenPos(xPix, yPix)
        pos = gp_Pnt(x, y, z)
        if self._state == self.DRAW_START:
            self._currentPos = pos
            self._clicked.append(pos)
            if self._shape_type == self.SURFACE_REVOLUTION:
                self.interactive.interaction_revolvedSurface(xPix, yPix)
            elif self._shape_type == self.SURFACE_BEZIER:
                self.interactive.interaction_bezierSurface(xPix, yPix)

    def mouseMove(self, xPix, yPix):
        x, y, z = self.convertScreenPos(xPix, yPix)
        pos = gp_Pnt(x, y, z)
        if self._state == self.DRAW_START and self._clicked:
            if self._shape_type == self.CURVE_BEZIER:
                self.makeBezierCurve(self._clicked, pos)
            elif self._shape_type == self.CURVE_BSPLINE:
                self.makeBSpline(self._clicked, pos)
            elif self._shape_type == self.CURVE_CIRCLE:
                self.makeCircle(self._clicked[0], pos)
                if len(self._clicked) == 2:
                    self.ExitDrawingMode()

    def mouseRelease(self, x, y):
        pass

    def recognize_clicked(self, shp, *kwargs):
        """ This is the function called every time
        a face is clicked in the 3d view
        """
        x, y, z = self.convertScreenPos(kwargs[0], kwargs[1])
        point = gp_Pnt(x, y, z)
        for shape in shp:
            if shape.ShapeType() == TopAbs_SOLID:
                pass
            if shape.ShapeType() == TopAbs_EDGE:
                self.recognize_edge(topods_Edge(shape))
            if shape.ShapeType() == TopAbs_FACE:
                pass
            if shape.ShapeType()==TopAbs_VERTEX:
                point = BRep_Tool.Pnt(shape)
                print(shape.ShapeType(), point.X(), point.Y(), point.Z())
        if self._state == self.DRAW_START:
            self._currentPos = point
            self._clicked.append(point)
            if self._shape_type == self.SURFACE_REVOLUTION:
                self.interactive.interaction_revolvedSurface(kwargs[0], kwargs[1])
            elif self._shape_type == self.SURFACE_BEZIER:
                self.interactive.interaction_bezierSurface(kwargs[0], kwargs[1])

    def recognize_edge(self, a_edge):
        """ Takes a TopoDS shape and tries to identify its nature
        whether it is a plane a cylinder a torus etc.
        if a plane, returns the normal
        if a cylinder, returns the radius
        """
        curve = BRepAdaptor_Curve(a_edge)
        curve_type = curve.GetType()
        if curve_type == GeomAbs_BezierCurve:
            print("--> Bezier")
            self._selectedShape = curve.Bezier()
        elif curve_type == GeomAbs_BSplineCurve:
            print("--> BSpline")
            self._selectedShape = curve.BSpline()
        elif curve_type == GeomAbs_Circle:
            print("--> Circle")
            self._selectedShape = Geom_Circle(curve.Circle())
        else:
            # TODO there are plenty other type that can be checked
            # see documentation for the BRepAdaptor class
            # https://www.opencascade.com/doc/occt-6.9.1/refman/html/class_b_rep_adaptor___surface.html
            print("not implemented")

    def getMousePositionWithObjects(self, xPix, yPix):
        if self._display._context.HasDetected():
            self._display._context.InitDetected()
            object = self._display.Context.SelectedInteractive()
            if object:
                ais_shape = AIS_Shape.DownCast(object)
                if ais_shape:
                    shape = ais_shape.Shape()
                    line = self.createLineFromViewEye(xPix, yPix, self._display.View)
                    intersectPoint = self.intersectLineThroughShape(shape, line)
                    return intersectPoint

    def createNewSketch(self):
        self.new_sketch = Sketch_NewSketchEditor(None, self._display)
        self.new_sketch.ui.uiOk.accepted.connect(self.createSketchNode)

    def createSketchNode(self):
        self.new_sketch.constructGrid()
        self._sketch = SketchNode("Sketch")
        self.modelUpdate.emit(self._sketch)


from OCC.Core.AIS import AIS_Manipulator, AIS_Shape, AIS_InteractiveContext, AIS_InteractiveObject


class ViewController(QObject):
    modelUpdate = pyqtSignal(object)

    def __init__(self, display):
        super(ViewController, self).__init__()
        self._manipulator = AIS_Manipulator()
        self._manipulator.SetModeActivationOnDetection(True)
        self._display = display
        self._selectedShape = None
        self._active = False

    def setActive(self):
        self._active = True

    def setDeactive(self):
        self._active = False
        self._manipulator.Detach()

    def selectAIS_Shape(self, x, y):
        ##object selection
        if self._active == True:
            self._display.MoveTo(x, y)
            assert isinstance(self._display.Context, AIS_InteractiveContext)
            try:
                if self._display.Context.HasDetected():
                    self._display.Context.InitDetected()
                    if self._display.Context.MoreDetected():
                        detected_object = self._display.Context.DetectedInteractive()
                        assert isinstance(detected_object, AIS_InteractiveObject)
                        if detected_object.Type() == AIS_KOI_Shape:
                            self._selectedShape = detected_object
                            self._manipulator.Attach(self._selectedShape)
                            self._display.Context.NextDetected()
            except Exception as e:
                print(e)

    def startTransform(self, x, y):
        if self._manipulator.HasActiveMode() and self._active == True:
            self._manipulator.StartTransform(x, y, self._display.View)

    def transform(self, x, y):
        if self._manipulator.HasActiveMode() and self._active == True:
            self._manipulator.Transform(x, y, self._display.View)
            self._display.View.Redraw()

    def finishTransform(self, x, y):
        if self._manipulator.HasActiveMode() and self._active == True:
            self.setDeactive()
