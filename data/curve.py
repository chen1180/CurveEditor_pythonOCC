import resources.icon.icon
import resources.shaders.shaders
import numpy as np
from data.node import *
from data.model import *
class CurveNode(MeshNode):
    def __init__(self, name, parent=None):
        super(CurveNode, self).__init__(name, parent)
        self._vertices=np.array([],dtype="float32")
        self._size=0
        self._order=2
        self._clamped=True
        self._subdivision = 20
    def toNumpyArray(self,vertices):
        return np.array(vertices,dtype="float32")
    def setVertices(self,vertices):
        self._vertices=self.toNumpyArray(vertices)
        self._size=self._vertices.shape[0] * self._vertices.itemsize
        self._readyForRendering=True
    def typeInfo(self):
        return "Curve"
    def data(self, column):
        r = super(CurveNode, self).data(column)
        if column == 2:
            r = self._order
        elif column == 3:
            r = self._subdivision
        elif column == 4:
            r = self._clamped
        return r
    def setData(self, column, value):
        super(CurveNode, self).setData(column, value)
        if column == 2:
            self._order = value
        elif column == 3:
            self._subdivision = value
        elif column == 4:
            self._clamped = value
    def resource(self):
        return ":/bezier.png"
class BezierCurve(CurveNode):
    def __init__(self, name, parent=None):
        super(BezierCurve, self).__init__(name, parent)
    def resource(self):
        return ":/bezier.png"
    def initializeShader(self):
        self._shader.InitShader(":/bezier.vert", ":/bezier.frag", None, ":/bezier.tese", None)
        self._shader.BindShader()
        self._shader.InitBuffer(self._vertices, self._size)
        self._shaderDirty=False
    def runShader(self):
        self._shader.DrawBezierCurve(self._subdivision, self._vertices.shape[0] // 3)
class Nurbs(CurveNode):
    def __init__(self, name, parent=None):
        super(Nurbs, self).__init__(name,parent)
        self._knots=[0.0,0.0,0.0,1.0,1.0,1.0]
        self._weights=[0.5,1.0,0.5]
    def initializeShader(self):
        self._shader.InitShader(":/nurbs.vert", ":/nurbs.frag", None, ":/nurbs.tese", None)
        self._shader.BindShader()
        self._shader.InitBuffer(self._vertices, self._size)
        self._shaderDirty=False
    def runShader(self):
        self._shader.DrawNurbsCurve(self._subdivision,self._vertices.shape[0]//3,self._knots,self._weights,self._clamped,self._order)

    def data(self, column):
        r = super(Nurbs, self).data(column)
        if column == 5:
            r =','.join(str(e) for e in self._knots)
        elif column == 6:
            r =','.join(str(e) for e in self._weights)
        return r
    def setData(self, column, value):
        super(Nurbs, self).setData(column, value)
        if column == 5:
            self._knots=[float(i) for i in value.split(',')]
        elif column == 6:
            self._weights=[float(i) for i in value.split(',')]


