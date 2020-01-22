class Node(object):

    def __init__(self, name, parent=None):
        '''
        Args:
            name: name of the node
            parent: parent pointer
        '''
        self._name = name
        self._parent = parent
        self._children = []
        if parent is not None:
            parent.addChild(self)

    def typeInfo(self):
        return "Node"

    def addChild(self, child):
        self._children.append(child)
        child._parent = self

    def name(self):
        return self._name

    def setName(self, name):
        self._name = name

    def child(self, row):
        if self._children:
            return self._children[row]
        return None

    def children(self):
        return self._children

    def insertChild(self, position, child):
        if position < 0 or position > len(self._children):
            return False
        self._children.insert(position, child)
        child._parent = self
        return True

    def removeChild(self, position):
        if position < 0 or position > len(self._children):
            return False
        child = self._children.pop(position)
        child._parent = None
        return True

    def childCount(self):
        return len(self._children)

    def parent(self):
        return self._parent

    def row(self):
        if self._parent is not None:
            return self._parent._children.index(self)

    def log(self, tabLevel=-1):
        output = ""
        tabLevel += 1
        for i in range(tabLevel):
            output += "\t"
        output += "|------" + self._name + "\n"
        for child in self._children:
            output += child.log(tabLevel)
        tabLevel -= 1
        return output

    def __repr__(self):
        return self.log()

    def data(self, column):
        if column == 0:
            return self._name
        elif column == 1:
            return self.typeInfo()

    def setData(self, column, value):
        if column == 0:
            self._name = value
        elif column == 1:
            pass

    def resource(self):
        return None


class TransformNode(Node):
    def __init__(self, name, parent=None):
        super(TransformNode, self).__init__(name, parent)
        self._x = 0
        self._y = 0
        self._z = 0

    def typeInfo(self):
        return "Transform"

    def x(self):
        return self._x

    def y(self):
        return self._y

    def z(self):
        return self._z

    def setX(self, x):
        self._x = x

    def setY(self, y):
        self._y = y

    def setZ(self, z):
        self._z = z

    def data(self, column):
        r = super(TransformNode, self).data(column)

        if column == 2:
            r = self._x
        elif column == 3:
            r = self._y
        elif column == 4:
            r = self._z

        return r

    def setData(self, column, value):
        super(TransformNode, self).setData(column, value)

        if column == 2:
            self._x = value
        elif column == 3:
            self._y = value
        elif column == 4:
            self._z = value

    def resource(self):
        return ":/transform.png"


class CameraNode(Node):
    def __init__(self, name, parent=None):
        super(CameraNode, self).__init__(name, parent)
        self._motionBlur = True
        self._shakeIntensity = 50.0

    def typeInfo(self):
        return "Camera"

    def motionBlur(self):
        return self._motionBlur

    def setMotionBlur(self, blur):
        self._motionBlur = blur

    def shakeIntensity(self):
        return self._shakeIntensity

    def setShakeIntensity(self, intensity):
        self._shakeIntensity = intensity

    def data(self, column):
        r = super(CameraNode, self).data(column)

        if column == 2:
            r = self._motionBlur
        elif column == 3:
            r = self._shakeIntensity

        return r

    def setData(self, column, value):
        super(CameraNode, self).setData(column, value)

        if column == 2:
            self._motionBlur = value
        elif column == 3:
            self._shakeIntensity = value

    def resource(self):
        return ":/camera.png"


class LightNode(Node):
    def __init__(self, name, parent=None):
        super(LightNode, self).__init__(name, parent)
        self._lightIntensity = 1.0
        self._nearRange = 40.0
        self._farRange = 80.0
        self._castShadows = True

    def typeInfo(self):
        return "Light"

    def lightIntensity(self):
        return self._lightIntensity

    def nearRange(self):
        return self._nearRange

    def farRange(self):
        return self._farRange

    def castShadows(self):
        return self._castShadows

    def setLightIntensity(self, intensity):
        self._lightIntensity = intensity

    def setNearRange(self, range):
        self._nearRange = range

    def setFarRange(self, range):
        self._farRange = range

    def setCastShadows(self, cast):
        self._castShadows = cast

    def data(self, column):
        r = super(LightNode, self).data(column)

        if column == 2:
            r = self._lightIntensity
        elif column == 3:
            r = self._nearRange
        elif column == 4:
            r = self._farRange
        elif column == 5:
            r = self._castShadows
        return r

    def setData(self, column, value):
        super(LightNode, self).setData(column, value)
        if column == 2:
            self._lightIntensity = value
        elif column == 3:
            self._nearRange = value
        elif column == 4:
            self._farRange = value
        elif column == 5:
            self._castShadows = value

    def resource(self):
        return ":/light.png"


class SketchNode(Node):
    def __init__(self, name, parent=None):
        super(SketchNode, self).__init__(name, parent)
        self.sketch_plane: gp_Ax3 = None

    def setSketchPlane(self, thePlane):
        self.sketch_plane = thePlane

    def typeInfo(self):
        return "Sketch"


from OCC.Core.gp import *

from data.sketch.geometry import *
from data.sketch.sketch_object import Sketch_Object


class SketchObjectNode(Node):
    def __init__(self, name, parent=None):
        super(SketchObjectNode, self).__init__(name, parent)
        self.sketchObject: Sketch_Geometry = None

    def setSketchObject(self, theObject: Sketch_Object):
        self.sketchObject = theObject

    def getSketchObject(self):
        return self.sketchObject

    def typeInfo(self):
        return "SketchObject"


class PointNode(SketchObjectNode):
    def __init__(self, name, parent=None):
        super(PointNode, self).__init__(name, parent)
        self.sketchObject: Sketch_Point = None

    def data(self, column):
        r = super(PointNode, self).data(column)
        self.myGeometry = self.sketchObject.GetGeometry2d()
        if column == 2:
            r = self.myGeometry.Pnt2d().X()
        elif column == 3:
            r = self.myGeometry.Pnt2d().Y()
        return r

    def setData(self, column, value):
        super(PointNode, self).setData(column, value)
        if column == 2:
            self.myGeometry.SetX(value)
        elif column == 3:
            self.myGeometry.SetY(value)
        self.sketchObject.DragTo(self.myGeometry.Pnt2d())

    def typeInfo(self):
        return "Point"


class LineNode(SketchObjectNode):
    def __init__(self, name, parent=None):
        super(LineNode, self).__init__(name, parent)
        self.sketchObject: Sketch_Line = None

    def data(self, column):
        r = super(LineNode, self).data(column)
        self.myGeometry: list = self.sketchObject.GetPoints()
        self.startPnt2d: gp_Pnt2d = self.myGeometry[0].GetGeometry2d().Pnt2d()
        self.endPnt2d: gp_Pnt2d = self.myGeometry[1].GetGeometry2d().Pnt2d()
        if column == 2:
            r = str((round(self.startPnt2d.X(), 1), round(self.startPnt2d.Y(), 1)))
        elif column == 3:
            r = self.startPnt2d.X()
        elif column == 4:
            r = self.startPnt2d.Y()
        elif column == 5:
            r = str((round(self.endPnt2d.X(), 1), round(self.endPnt2d.Y(), 1)))
        elif column == 6:
            r = self.endPnt2d.X()
        elif column == 7:
            r = self.endPnt2d.Y()
        elif column == 8:
            r = self.startPnt2d.Distance(self.endPnt2d)
        return r

    def setData(self, column, value):
        super(LineNode, self).setData(column, value)
        if column == 3:
            self.startPnt2d.SetX(value)
        elif column == 4:
            self.startPnt2d.SetY(value)
        elif column == 6:
            self.endPnt2d.SetX(value)
        elif column == 7:
            self.endPnt2d.SetY(value)
        elif column == 8:
            pass
        self.myGeometry[0].DragTo(self.startPnt2d)
        self.myGeometry[1].DragTo(self.endPnt2d)
        self.sketchObject.Recompute()

    def typeInfo(self):
        return "Line"


from OCC.Core.Geom2d import Geom2d_BezierCurve


class BezierNode(SketchObjectNode):
    def __init__(self, name, parent=None):
        super(BezierNode, self).__init__(name, parent)
        self.sketchObject: Sketch_BezierCurve = None

    def data(self, column):
        r = super(BezierNode, self).data(column)
        if self.sketchObject:
            self.myGeometry2d: Geom2d_BezierCurve = self.sketchObject.GetGeometry2d()
            self.degree = self.myGeometry2d.Degree()
            self.continuity = self.myGeometry2d.Continuity()
            self.closed_flag = self.myGeometry2d.IsClosed()
            self.rational_flag = self.myGeometry2d.IsRational()
            self.weights = self.sketchObject.GetWeights()
            self.poles = self.sketchObject.GetPoles()
            if column == 2:
                r = self.degree
            elif column == 3:
                r = self.rational_flag
            elif column == 4:
                r = self.closed_flag
            elif column == 5:
                r = self.continuity
            for i in range(1, len(self.weights) + 1):
                if column == 5 + i:
                    r = self.weights[i - 1]

        return r

    def setData(self, column, value):
        if column == 2:
            self.degree = value
        elif column == 3:
            self.rational_flag = value
        elif column == 4:
            self.closed_flag = value
        elif column == 5:
            self.continuity = value
        super(BezierNode, self).setData(column, value)
        for i in range(1, len(self.weights) + 1):
            if column == 5 + i:
                self.weights[i - 1] = value
        self.sketchObject.Recompute()

    def typeInfo(self):
        return "Bezier curve"


class BsplineNode(SketchObjectNode):
    def __init__(self, name, parent=None):
        super(BsplineNode, self).__init__(name, parent)

    def data(self, column):
        r = super(BsplineNode, self).data(column)

        return r

    def setData(self, column, value):
        super(BsplineNode, self).setData(column, value)

    def typeInfo(self):
        return "BSpline"


class BezierSurfaceNode(SketchObjectNode):
    def __init__(self, name, parent=None):
        super(BezierSurfaceNode, self).__init__(name, parent)

    def data(self, column):
        r = super(BezierSurfaceNode, self).data(column)

        return r

    def setData(self, column, value):
        super(BezierSurfaceNode, self).setData(column, value)

    def typeInfo(self):
        return "Bezier Surface"
